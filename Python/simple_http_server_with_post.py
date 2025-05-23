from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Log the GET request
            self.log_request('GET', self.path)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'GET request received')
        except Exception:
            pass  # Silencing any exceptions

    def do_POST(self):
        try:
            # Log the POST request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Output the POST data to the console
            print("Received POST data:", post_data.decode('utf-8'))

            # Log the POST request
            self.log_request('POST', post_data.decode('utf-8'))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'success', 'message': 'POST request received'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception:
            pass  # Silencing any exceptions

    def log_request(self, method, data):
        try:
            log_file_name = 'get_requests.log' if method == 'GET' else 'post_requests.log'
            with open(log_file_name, 'a') as log_file:
                log_file.write(f'{method}: {data}\n')
        except Exception:
            pass  # Silencing any exceptions

    def handle_error(self):
        try:
            self.send_response(405)  # Method Not Allowed
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'error', 'message': 'Method not allowed'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception:
            pass  # Silencing any exceptions

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_PUT(self):
        self.handle_error()

    def do_DELETE(self):
        self.handle_error()

    def do_PATCH(self):
        self.handle_error()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port {port}')
    try:
        httpd.serve_forever()
    except Exception:
        pass  # Silencing any exceptions

if __name__ == '__main__':
    run()
    
