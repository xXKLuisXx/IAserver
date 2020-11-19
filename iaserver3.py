from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from io import BytesIO
import stanza

stanza.download('es') # download English model
nlp = stanza.Pipeline('es') # initialize English neural pipeline


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        jsonObject = json.loads(body)
        doc = nlp(jsonObject["text"]) # run annotation over a sentence
        words = []
        for sent in doc.sentences:
            for word in sent.words:
                if word.upos == "ADJ":
                    words.append(word.text)

        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(json.dumps(words).encode('utf-8'))
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('0.0.0.0', 8100), SimpleHTTPRequestHandler)
httpd.serve_forever()