
import asyncio

from http import HTTPStatus
from urllib.parse import unquote

from .lib.http_exception import (
    InternalServerError,
    WebSocketException,
    WebSocketClientClosed,
    WebSocketServerClosed
)
from .lib.contexts import ServerContext
from .lib.http_protocol import HTTPProtocol
from .lib.websocket import WebSocket
from .utils import log_date

_HTTP_OR_HTTPS = {
    False: 'http',
    True: 'https'
}
_WS_OR_WSS = {
    False: 'ws',
    True: 'wss'
}

# Define color codes
BG_YELLOW = "\033[35m"
BLUE = "\033[34m"  # Blue color
GREEN = "\033[32m"  # Green color
RED = "\033[31m"  # Red color
YELLOW = "\033[33m"  # Yellow color
MAGENTA = "\033[35m"  # Magenta color
CYAN = "\033[36m"  # Cyan color
WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m"  # Reset color


class ASGIServer(HTTPProtocol):
    __slots__ = ('_app',
                 '_scope',
                 '_read',
                 '_task',
                 '_timer',
                 '_timeout',
                 '_websocket',
                 '_http_chunked')

    def __init__(self, _app=None, **kwargs):
        self._app = _app
        self._scope = None
        self._read = None
        self._task = None
        self._timer = None
        self._timeout = 30
        self._websocket = None
        self._http_chunked = None

        super().__init__(ServerContext(), **kwargs)

    def _handle_websocket(self):
        self._websocket = WebSocket(self.request, self.response)

        self._scope['type'] = 'websocket'
        self._scope['scheme'] = _WS_OR_WSS[self.request.is_secure]
        self._scope['subprotocols'] = [
            value.decode('utf-8') for value in
            self.request.headers.getlist(b'sec-websocket-protocol')]

    async def _handle_http(self):
        self._scope['type'] = 'http'
        self._scope['method'] = self.request.method.decode('utf-8')
        self._scope['scheme'] = _HTTP_OR_HTTPS[self.request.is_secure]

        if not self.request.has_body and self.queue[0] is not None:
            # avoid blocking on initial receive() due to empty Queue
            # in the case of bodyless requests, e.g. GET
            self.queue[0].put_nowait(b'')

    async def header_received(self):
        self._scope = {
            'asgi': {'version': '3.0'},
            'http_version': self.request.version.decode('utf-8'),
            'path': unquote(self.request.path.decode('utf-8'), 'utf-8'),
            'raw_path': self.request.path,
            'query_string': self.request.query_string,
            'root_path': self.options['_root_path'],
            'headers': self.request.header.getheaders(),
            'client': self.request.client,
            'server': self.request.socket.getsockname()
        }

        if (self.options['ws'] and b'upgrade' in self.request.headers and
                b'connection' in self.request.headers and
                b'sec-websocket-key' in self.request.headers and
                self.request.headers[b'upgrade'].lower() == b'websocket'):
            self._handle_websocket()
        else:
            await self._handle_http()
            self._read = self.request.stream()

        self._task = self.loop.create_task(self.app())

    def connection_lost(self, exc):
        if (self._task is not None and not self._task.done() and
                self._timer is None):
            self._timer = self.loop.call_at(self.loop.time() + self._timeout,
                                            self._task.cancel)

        super().connection_lost(exc)

    async def app(self):
        try:
            await self._app(self._scope, self.receive, self.send)

            if self._timer is not None:
                self._timer.cancel()
        except asyncio.CancelledError:
            self.logger.warning(
                'task: ASGI application is cancelled due to timeout'
            )
        except Exception as exc:
            if (self.request is not None and self.request.upgraded and
                    self._websocket is not None):
                exc = WebSocketServerClosed(cause=exc)

            await self.handle_exception(exc)

    def _set_app_timeout(self):
        if self._timer is None:
            self._timer = self.loop.call_at(
                self.loop.time() + self._timeout, self._task.cancel
            )

    async def receive(self):
        if self._scope['type'] == 'websocket':
            # initially, the Request.upgraded value is False
            # it will become True later
            # after the response status is set to 101:
            # Response.set_status(101) in WebSocket.accept()
            if not self.request.upgraded:
                return {'type': 'websocket.connect'}

            try:
                payload = await self._websocket.receive()

                if isinstance(payload, str):
                    return {
                        'type': 'websocket.receive',
                        'text': payload
                    }

                return {
                    'type': 'websocket.receive',
                    'bytes': payload
                }
            except WebSocketException as exc:
                code = 1005

                if isinstance(exc, WebSocketClientClosed):
                    code = exc.code

                if self.request is not None:
                    self.print_exception(exc)

                self._set_app_timeout()
                return {
                    'type': 'websocket.disconnect',
                    'code': code
                }

        if self._scope['type'] != 'http':
            await self.handle_exception(
                InternalServerError('unsupported scope type %s' %
                                    self._scope['type'])
            )
            return

        try:
            data = await self._read.__anext__()

            return {
                'type': 'http.request',
                'body': data,
                'more_body': (
                    (data != b'' and self.request.content_length == -1) or
                    self.request.body_size < self.request.content_length
                )
            }
        except Exception as exc:
            if not (self.request is None or
                    isinstance(exc, StopAsyncIteration)):
                self.print_exception(exc)

            self._set_app_timeout()
            return {'type': 'http.disconnect'}

    async def send(self, data):
        try:
            if data['type'] in ('http.response.start', 'websocket.accept'):
                # websocket doesn't have this
                if 'status' in data:
                    self.response.set_status(data['status'],
                                             HTTPStatus(data['status']).phrase)

                self.response.set_base_header()

                if 'status' in data:
                    self.http_logger(data)

                if 'headers' in data:
                    for header in data['headers']:
                        if b'\n' in header[0] or b'\n' in header[1]:
                            await self.handle_exception(
                                InternalServerError(
                                    'name or value cannot contain '
                                    'illegal characters')
                            )
                            return

                        name = header[0].lower()

                        if name == b'content-type':
                            self.response.set_content_type(header[1])
                            continue

                        if name in (b'date',
                                    b'server',
                                    b'transfer-encoding',
                                    b'sec-websocket-protocol'):
                            # disallow apps from changing them,
                            # as they are managed by Netix
                            continue

                        if name == b'connection':
                            if header[1].lower() == b'close':
                                # this does not necessarily set
                                # "Connection: close" in the response header.
                                # but it guarantees that the TCP connection
                                # will be terminated
                                self.request.http_keepalive = False
                            continue

                        if name == b'content-length':
                            # will disable http chunked in the
                            # self.response.write()
                            self._http_chunked = False

                        if isinstance(header, list):
                            header = tuple(header)

                        self.response.append_header(*header)

                # websocket has this
                if 'subprotocol' in data and data['subprotocol']:
                    if '\n' in data['subprotocol']:
                        await self.handle_exception(
                            InternalServerError(
                                'subprotocol value cannot contain '
                                'illegal characters')
                        )
                        return

                    self.response.set_header(
                        b'Sec-WebSocket-Protocol',
                        data['subprotocol'].encode('utf-8')
                    )

            if data['type'] == 'http.response.body':
                if 'body' in data and data['body'] != b'':
                    await self.response.write(
                        data['body'],
                        chunked=self._http_chunked,
                        throttle=self.response.headers_sent(),
                        buffer_size=self.options['buffer_size']
                    )

                if 'more_body' not in data or data['more_body'] is False:
                    await self.response.write(b'', throttle=False)
                    self.response.close(keepalive=True)
            elif data['type'] == 'websocket.send':
                if 'bytes' in data and data['bytes']:
                    await self._websocket.send(data['bytes'])
                elif 'text' in data and data['text']:
                    await self._websocket.send(data['text'], opcode=1)
            elif data['type'] == 'websocket.accept':
                self.logger.info(f"{GREEN}Websocket Connection Opened{RESET}")
                await self._websocket.accept()
            elif data['type'] == 'websocket.close':
                print(data)
                self.logger.info(f"{RED}Websocket Connection Closed{RESET}")
                await self._websocket.close(data.get('code', 1000))
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            if not (self.request is None or self.response is None):
                self.print_exception(exc)

    def http_logger(self, data):
        try:
            status_code = data['status']
            status_code_message = HTTPStatus(status_code).phrase

            success_status_codes = {200, 201, 302, 307, 304, 301, 305}  # Add more as needed
            error_status_codes = {404, 400, 405, 401, 403, 402, 500}  # Add more error status codes as needed

            status_color = GREEN if status_code in success_status_codes else (RED if status_code in error_status_codes else YELLOW)
            path_color = GREEN if status_code in {301, 302, 303, 304, 305, 306, 307} else BOLD

            log_message = (
                f"{log_date()} "
                f"{self.colorize(self._scope['client'][0], BOLD)}:{self.colorize(self._scope['client'][1], RESET)} "
                f"- {self.colorize(self._scope['method'], BOLD)} "
                f"{self.colorize(self._scope['path'], path_color)} "
                f"{self._scope['http_version']}\" "
                f"{self.colorize(status_code, status_color)}, {status_code_message}"
            )
            print(log_message)

        except Exception as e:
            print(f"Error in http_logger method: {e}")

    def colorize(self, text, color):
        return f"{color}{text}{RESET}"