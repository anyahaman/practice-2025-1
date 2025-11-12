"""
Basic HTTP/1.0 Server from scratch in Python
"""

import socket
import os


class SimpleHTTPServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.HTDOCS_DIR = 'htdocs'

    def create_response(self, status_code, content=''):
        """Create HTTP response string"""
        status_messages = {
            200: 'OK',
            404: 'NOT FOUND'
        }
        return f'HTTP/1.0 {status_code} {status_messages.get(status_code, "")}\n\n{content}'

    def handle_request(self, request):
        """Handle incoming HTTP request and return response"""
        try:
            # Parse HTTP headers
            headers = request.split('\n')
            if not headers or not headers[0]:
                return self.create_response(404, 'File Not Found')

            # Extract filename from request line (e.g., "GET /index.html HTTP/1.1")
            request_line = headers[0].split()
            if len(request_line) < 2:
                return self.create_response(404, 'File Not Found')

            filename = request_line[1]

            # Default to index.html for root path
            if filename == '/':
                filename = '/index.html'

            # Build file path
            file_path = os.path.join(self.HTDOCS_DIR, filename.lstrip('/'))

            # Check if file exists and read its content
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as fin:
                    content = fin.read()
                return self.create_response(200, content)
            else:
                return self.create_response(404, 'File Not Found')

        except Exception as e:
            print(f"Error handling request: {e}")
            return self.create_response(404, 'File Not Found')

    def start(self):
        """Start the HTTP server"""
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.SERVER_HOST, self.SERVER_PORT))
        server_socket.listen(1)

        print(f'Listening on port {self.SERVER_PORT} ...')
        print(f'Open http://localhost:{self.SERVER_PORT} in your browser')

        try:
            while True:
                # Wait for client connections
                client_connection, client_address = server_socket.accept()
                print(f"New connection from {client_address}")

                # Get the client request
                request = client_connection.recv(1024).decode()
                print("=" * 50)
                print(f"Request received:\n{request}")
                print("=" * 50)

                # Handle request and send response
                response = self.handle_request(request)
                client_connection.sendall(response.encode())

                # Close connection
                client_connection.close()
                print(f"Connection with {client_address} closed\n")

        except KeyboardInterrupt:
            print("\nShutting down server...")
        finally:
            # Close socket
            server_socket.close()
            print("Server closed")


def create_sample_files():
    """Create sample HTML files for testing"""
    # Create htdocs directory if it doesn't exist
    if not os.path.exists('htdocs'):
        os.makedirs('htdocs')

    # Create index.html
    index_content = """<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello World!</h1>
    <p>Welcome to the index.html web page..</p>
    <p>Here's a link to <a href="ipsum.html">Ipsum</a></p>
    <p>Try a <a href="nonexistent.html">non-existent page</a> to see 404 error</p>
</body>
</html>"""

    with open('htdocs/index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)

    # Create ipsum.html
    ipsum_content = """<html>
<head>
    <title>Ipsum</title>
</head>
<body>
    <h1>Ipsum!</h1>
    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Pellentesque tincidunt libero diam, nec imperdiet libero
        sodales quis. Nulla in pulvinar sem. Vivamus placerat
        ullamcorper sagittis. Proin varius, erat sed egestas semper,
        enim lectus viverra diam, id placerat est augue et turpis.
    </p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>"""

    with open('htdocs/ipsum.html', 'w', encoding='utf-8') as f:
        f.write(ipsum_content)


def main():
    """Main function to run the HTTP server"""
    print("Building a basic HTTP Server from scratch in Python")
    print("=" * 60)

    # Create sample files
    create_sample_files()
    print("Sample HTML files created in 'htdocs' directory")

    # Start server
    server = SimpleHTTPServer()
    server.start()


if __name__ == "__main__":
    main()
