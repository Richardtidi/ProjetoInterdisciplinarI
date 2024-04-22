from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import threading


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    pass


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        if path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("Projeto/index.html", "rb") as file:
                self.wfile.write(file.read())
                
        if path == "/centralDeAjuda.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("Projeto/centralDeAjuda.html", "rb") as file:
                self.wfile.write(file.read())

        if path == "/gerenciarEstoque.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("Projeto/gerenciarEstoque.html", "rb") as file:
                self.wfile.write(file.read())

        if path == "/novoEstoque.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("Projeto/novoEstoque.html", "rb") as file:
                self.wfile.write(file.read())

        if path == "/quemSomos.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("Projeto/quemSomos.html", "rb") as file:
                self.wfile.write(file.read())

        else:
            
            if path.endswith('.jpeg'):
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                with open("Projeto/imagem1.jpeg", "rb") as file:
                    self.wfile.write(file.read())

            if path.endswith('.jpg'):
                self.send_response(200)
                self.send_header("Content-type", "image/jpg")
                self.end_headers()
                with open("Projeto/imagem2.jpg", "rb") as file:
                    self.wfile.write(file.read())

            if path.endswith('.css'):
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("Projeto" + path, "rb") as file:
                    self.wfile.write(file.read())


    def do_POST(self):
        if self.path == "/submit":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            params = parse_qs(post_data)

            username = params.get("username", [""])[0]

            self.send_response(302)
            self.send_header("Location", f"/welcome?username={username}")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("not_found.html", "rb") as file:
                self.wfile.write(file.read())


def run():
    port = 8000
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Servidor rodando na porta {port}. Use Ctrl+C para encerrar.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Servidor encerrado.")

if __name__ == "__main__":
    run()
