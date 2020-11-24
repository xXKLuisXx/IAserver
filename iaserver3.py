from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from io import BytesIO
import stanza
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

stanza.download('es') # download English model
nlp = stanza.Pipeline('es') # initialize English neural pipeline


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        jsonObject = json.loads(body)
        doc = nlp(jsonObject["text"]) # run annotation over a sentence
        words = []
        responseDicc = {'permited':False,'words':[]}
        for sent in doc.sentences:
            for word in sent.words:
                if word.upos == "ADJ":
                    words.append(word.text)
        
        df = pd.read_excel('dataset.xlsx')
        for word in words:
            if word in df['Insultos'].values:
                responseDicc['permited'] = True
        
        responseDicc['words'] = words

        response = BytesIO()
        response.write(json.dumps(responseDicc).encode('utf-8'))
        
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('0.0.0.0', 8100), SimpleHTTPRequestHandler)
httpd.serve_forever()