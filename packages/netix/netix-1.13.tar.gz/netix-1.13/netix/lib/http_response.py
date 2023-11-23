
import os
import time

from datetime import datetime, timedelta
from urllib.parse import quote

from .http_exception import (
    BadRequest, ExpectationFailed, InternalServerError, RangeNotSatisfiable
)
from .response import Response

KEEPALIVE_OR_CLOSE = {
    True: b'keep-alive',
    False: b'close'
}
KEEPALIVE_OR_UPGRADE = {
    False: b'keep-alive',
    True: b'upgrade'
}


class HTTPResponse(Response):
    __slots__ = ('headers',
                 'http_chunked',
                 '_request',
                 '_status',
                 '_content_type')

    def __init__(self, request):
        super().__init__(request)

        self.headers = {}
        self.http_chunked = False

        self._request = request
        self._status = []
        self._content_type = []

    def headers_sent(self, sent=False):
        if sent:
            self.headers = None

        return self.headers is None

    def append_header(self, name, value):
        if isinstance(name, str):
            name = name.encode('latin-1')

        if isinstance(value, str):
            value = value.encode('latin-1')

        _name = name.lower()

        if _name in self.headers:
            self.headers[_name].append(name + b': ' + value)
        else:
            self.headers[_name] = [name + b': ' + value]

    def set_base_header(self):
        if self.headers_sent() or self.headers:
            return

        self.set_header(
            b'Date',
            self._request.protocol.options['server_info']['date']
        )
        self.set_header(
            b'Server',
            self._request.protocol.options['server_info']['name']
        )

    def set_header(self, name, value=''):
        if isinstance(name, str):
            name = name.encode('latin-1')

        if isinstance(value, str):
            value = value.encode('latin-1')

        if b'\n' in name or b'\n' in value:
            raise InternalServerError

        self.headers[name.lower()] = [name + b': ' + value]

    def set_status(self, status=200, message=b'OK'):
        if isinstance(message, str):
            message = message.encode('latin-1')

        if not isinstance(status, int) or b'\n' in message:
            raise InternalServerError

        if b'_line' in self.headers:
            self.headers[b'_line'][1] = b'%d' % status
            self.headers[b'_line'][2] = message
        else:
            self._status.append((status, message))

    def get_status(self):
        try:
            return self._status.pop()
        except IndexError:
            return 200, b'OK'

    def set_content_type(self, content_type=b'text/html; charset=utf-8'):
        if isinstance(content_type, str):
            content_type = content_type.encode('latin-1')

        if b'\n' in content_type:
            raise InternalServerError

        if b'content-type' in self.headers:
            self.headers[b'content-type'] = [b'Content-Type: ' + content_type]
        else:
            self._content_type.append(content_type)

    def get_content_type(self):
        try:
            return self._content_type.pop()
        except IndexError:
            return b'text/html; charset=utf-8'

    def close(self, keepalive=False):
        if not keepalive:
            # this will force the TCP connection to be terminated
            self._request.http_keepalive = False

        super().close()

    async def send_continue(self):
        if self._request.http_continue:
            if (self._request.content_length >
                    self._request.protocol.options['client_max_body_size']):
                raise ExpectationFailed

            await self.send(
                b'HTTP/%s 100 Continue\r\n\r\n' % self._request.version,
                throttle=False
            )
            self.close(keepalive=True)

    async def end(self, data=b'', keepalive=True, **kwargs):
        if self.headers_sent():
            await self.write(data, throttle=False)
        else:
            self.set_base_header()

            status = self.get_status()
            content_length = len(data)

            if content_length > 0 and (
                        self._request.method == b'HEAD' or
                        status[0] in (204, 205, 304) or 100 <= status[0] < 200
                    ):
                data = b''

            await self.send(
                b'HTTP/%s %d %s\r\nContent-Type: %s\r\nContent-Length: %d\r\n'
                b'Connection: %s\r\n%s\r\n\r\n%s' % (
                    self._request.version,
                    *status,
                    self.get_content_type(),
                    content_length,
                    KEEPALIVE_OR_CLOSE[
                        keepalive and self._request.http_keepalive],
                    b'\r\n'.join(
                        b'\r\n'.join(v) for v in self.headers.values()),
                    data), throttle=False, **kwargs
            )

            self.headers_sent(True)

        self.close(keepalive=keepalive)

    async def write(self, data, buffer_size=16 * 1024, **kwargs):
        kwargs['buffer_size'] = buffer_size

        if not self.headers_sent():
            if b'_line' not in self.headers:
                # this block is executed when write() is called outside the
                # handler/middleware. e.g. ASGI server
                self.set_base_header()

                status = self.get_status()
                no_content = (status[0] in (204, 205, 304) or
                              100 <= status[0] < 200)
                chunked = kwargs.get('chunked')

                if chunked is None:
                    self.http_chunked = (self._request.version == b'1.1' and
                                         self._request.http_keepalive and
                                         not no_content)
                else:
                    self.http_chunked = chunked

                if self.http_chunked:
                    self.set_header(b'Transfer-Encoding', b'chunked')

                self.headers[b'_line'] = [b'HTTP/%s' % self._request.version,
                                          b'%d' % status[0],
                                          status[1]]

                if no_content and status[0] not in (101, 426):
                    self.set_header(b'Connection', b'close')
                else:
                    if chunked is None and not self.http_chunked and not (
                            self._request.version == b'1.1' and (
                                status[0] in (101, 426) or
                                b'range' in self._request.headers)):
                        self._request.http_keepalive = False

                    if status[0] == 101:
                        self._request.upgraded = True
                    elif not no_content:
                        self.set_header(b'Content-Type',
                                        self.get_content_type())

                    self.set_header(
                        b'Connection',
                        KEEPALIVE_OR_UPGRADE[status[0] in (101, 426)]
                    )

                if self._request.method == b'HEAD' or no_content:
                    if status[0] not in (101, 426):
                        self._request.http_keepalive = False

                    data = None
                else:
                    self._request.protocol.set_watermarks(
                        high=buffer_size * 4,
                        low=kwargs.get('buffer_min_size', buffer_size // 2)
                    )

            await self.send(
                b' '.join(self.headers.pop(b'_line')) + b'\r\n' +
                b'\r\n'.join(b'\r\n'.join(v) for v in self.headers.values()) +
                b'\r\n\r\n', throttle=False
            )
            self.headers_sent(True)

        if (self.http_chunked and not self._request.upgraded and
                data is not None):
            await self.send(b'%X\r\n%s\r\n' % (len(data), data), **kwargs)
        else:
            await self.send(data, **kwargs)

    