import sys

from .server import ASGIServer
from .monitor import print_data, print_dict

def main():

    server = ASGIServer()
    options = {'ssl': {}}

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

    daemon_mode = False

    for i in range(len(sys.argv)):
        if sys.argv[i - 1] == '--help':
            print('Usage: python3 -m netix [OPTIONS] APP')
            print()
            print('Example:')
            print('  python3 -m netix example:app')
            print('  python3 -m netix /path/to/example.py')
            print('  python3 -m netix /path/to/example.py:myapp')
            print('  python3 -m netix --debug --port 8080 example:app')
            print('  python3 -m netix --daemon example:app')
            print('  --------------- or -----------------')
            print('  netix example:app')
            print('  netix /path/to/example.py')
            print('  netix /path/to/example.py:myapp')
            print('  netix --debug --port 8080 example:app')
            print('  netix --daemon example:app')
            print()
            print('Options:')
            print('  --host                    Listen host. Defaults to "127.0.0.1"')  # noqa: E501
            print('  --daemon                  Start the deamon more to run the server in backgroung')
            print('                            Use --daemon main:app @app module to daemonised')
            print('  monitor                   Monitor all the daemon process.')
            print('  monitor-console           Monitor the daemon process in a console view with more details.')
            print('  --port                    Listen port. Defaults to 8000')
            print('  --bind                    Address to bind.')
            print('                            Instead of using --host or --port')
            print('                            E.g. "127.0.0.1:8000" or "/tmp/file.sock"')  # noqa: E501
            print('  --reuse-port              Use SO_REUSEPORT when available')
            print('  --worker-num              Number of worker processes. Defaults to 1')  # noqa: E501
            print('  --backlog                 Maximum number of pending connections')  # noqa: E501
            print('                            Defaults to 100')
            print('  --ssl-cert                SSL certificate location')
            print('                            E.g. "/path/to/fullchain.pem"')
            print('  --ssl-key                 SSL private key location')
            print('                            E.g. "/path/to/privkey.pem"')
            print('  --debug                   Enable debug mode.')
            print('                            Intended for development')
            print('  --reload                  Enable auto reload on code changes.') 
            print('  --no-ws                   Disable built-in WebSocket support.')  # noqa: E501
            print('  --log-level               Defaults to "DEBUG". See')
            print('                            https://docs.python.org/3/library/logging.html#levels')  # noqa: E501
            print('  --download-rate           Limits the sending speed to the client')  # noqa: E501
            print('                            Defaults to 1048576, which means 1MiB/s')  # noqa: E501
            print('  --upload-rate             Limits the upload / POST speed')
            print('                            Defaults to 1048576, which means 1MiB/s')  # noqa: E501
            print('  --buffer-size             Defaults to 16384, or 16KiB')
            print('  --client-max-body-size    Defaults to 2 * 1048576, or 2MiB')
            print('  --client-max-header-size  Defaults to 8192, or 8KiB')
            print('  --request-timeout         Defaults to 30 (seconds)')
            print('  --keepalive-timeout       Defaults to 30 (seconds)')
            print('  --keepalive-connections   Maximum number of keep-alive connections')  # noqa: E501
            print('                            Defaults to 512 (connections/worker)')  # noqa: E501
            print('  --root-path               Set the ASGI root_path. Defaults to ""')  # noqa: E501
            print('  --help                    Show this help and exit')
            sys.exit()
        elif sys.argv[i - 1] == '--no-ws':
            options['ws'] = False
        elif sys.argv[i - 1] == '--daemon':
            daemon_mode = True
        elif sys.argv[i - 1] in ('--debug', '--reload'):
            options[sys.argv[i - 1].lstrip('-').replace('-', '_')] = True
        elif sys.argv[i - 1] in ('--host',
                                '--log-level',
                                '--root-path'):
            options[sys.argv[i - 1].lstrip('-').replace('-', '_')] = sys.argv[i]
        elif sys.argv[i - 1] in ('--port',
                                '--worker-num',
                                '--backlog',
                                '--download-rate',
                                '--upload-rate',
                                '--buffer-size',
                                '--client-max-body-size',
                                '--client-max-header-size',
                                '--request-timeout',
                                '--keepalive-timeout',
                                '--keepalive-connections'):
            try:
                options[sys.argv[i - 1].lstrip('-').replace('-', '_')] = int(sys.argv[i])  # noqa: E501
            except ValueError:
                print(
                    'Invalid {:s} value "{:s}". It must be a number'.format(
                        sys.argv[i - 1], sys.argv[i])
                )
                sys.exit(1)
        elif sys.argv[i - 1] == '--bind':
            try:
                if ':\\' not in sys.argv[i] and ':' in sys.argv[i]:
                    options['host'], port = sys.argv[i].split(':', 1)
                    options['port'] = int(port)
                else:
                    options['host'] = sys.argv[i]
            except ValueError:
                print('Invalid --bind value "{:s}"'.format(sys.argv[i]))
                sys.exit(1)
        elif sys.argv[i - 1] == '--ssl-cert':
            options['ssl']['cert'] = sys.argv[i]
        elif sys.argv[i - 1] == '--ssl-key':
            options['ssl']['key'] = sys.argv[i]
        elif sys.argv[i - 1].startswith('-'):
            print('Unrecognized option "{:s}"'.format(sys.argv[i - 1]))
            sys.exit(1)
        elif sys.argv[i - 1] == 'monitor':
            monitoring_data = server.get_monitoring_data()
            print_data(monitoring_data)
            sys.exit()
        elif sys.argv[i - 1] == 'status':
            print(f'{CYAN}Netix 1.11 (ASGI) Server{RESET} \nVersion: {YELLOW}1.11{RESET} \nStatus: {GREEN}(Active){RESET} \nBooting: {GREEN}sys.{YELLOW}argv{RESET}')
            sys.exit()
        elif sys.argv[i - 1] == 'monitor-console':
            data = server.get_monitoring_data()
            print_dict(data)
            sys.exit()

    if sys.argv[-1] != sys.argv[0] and not sys.argv[-1].startswith('-'):
        options['app'] = sys.argv[-1]

    if 'app' not in options:
        print('You must specify APP. Use "--help" for help')
        sys.exit(1)

    if 'host' not in options:
        options['host'] = '127.0.0.1'

    if 'port' not in options:
        options['port'] = 8000

    if daemon_mode:
        # Run the server in daemon mode
        server.daemon(**options)
    else:
        # Run the server using the _ctxrun function
        server._ctxrun(**options)

if __name__ == '__main__':
    main()