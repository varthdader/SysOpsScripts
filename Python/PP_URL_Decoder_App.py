from flask import Flask, request, render_template_string
import re
import string
from base64 import urlsafe_b64decode
from urllib.parse import unquote
from html import unescape

app = Flask(__name__)

class URLDefenseDecoder:
    def __init__(self):
        self.ud_pattern = re.compile(r'https://urldefense(?:\.proofpoint)?\.com/(v[0-9])/')
        self.v1_pattern = re.compile(r'u=(?P<url>.+?)&k=')
        self.v2_pattern = re.compile(r'u=(?P<url>.+?)&[dc]=')
        self.v3_pattern = re.compile(r'v3/__(?P<url>.+?)__;(?P<enc_bytes>.*?)!')
        self.v3_token_pattern = re.compile(r"\*(\*.)?")
        self.v3_single_slash = re.compile(r"^([a-z0-9+.-]+:/)([^/].+)", re.IGNORECASE)
        self.v3_run_mapping = {}
        run_values = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-' + '_'
        run_length = 2
        for value in run_values:
            self.v3_run_mapping[value] = run_length
            run_length += 1

    def decode(self, rewritten_url):
        match = self.ud_pattern.search(rewritten_url)
        if match:
            if match.group(1) == 'v1':
                return self.decode_v1(rewritten_url)
            elif match.group(1) == 'v2':
                return self.decode_v2(rewritten_url)
            elif match.group(1) == 'v3':
                return self.decode_v3(rewritten_url)
            else:
                raise ValueError('Unrecognized version in: ' + rewritten_url)
        else:
            raise ValueError('Does not appear to be a URL Defense URL')

    def decode_v1(self, rewritten_url):
        match = self.v1_pattern.search(rewritten_url)
        if match:
            url_encoded_url = match.group('url')
            html_encoded_url = unquote(url_encoded_url)
            return unescape(html_encoded_url)
        else:
            raise ValueError('Error parsing URL')

    def decode_v2(self, rewritten_url):
        match = self.v2_pattern.search(rewritten_url)
        if match:
            special_encoded_url = match.group('url')
            trans = str.maketrans('-_', '%/')
            url_encoded_url = special_encoded_url.translate(trans)
            html_encoded_url = unquote(url_encoded_url)
            return unescape(html_encoded_url)
        else:
            raise ValueError('Error parsing URL')

    def decode_v3(self, rewritten_url):
        def replace_token(token):
            if token == '*':
                character = self.dec_bytes[self.current_marker]
                self.current_marker += 1
                return character
            if token.startswith('**'):
                run_length = self.v3_run_mapping[token[-1]]
                run = self.dec_bytes[self.current_marker:self.current_marker + run_length]
                self.current_marker += run_length
                return run

        def substitute_tokens(text, start_pos=0):
            match = self.v3_token_pattern.search(text, start_pos)
            if match:
                start = text[start_pos:match.start()]
                built_string = start
                token = text[match.start():match.end()]
                built_string += replace_token(token)
                built_string += substitute_tokens(text, match.end())
                return built_string
            else:
                return text[start_pos:len(text)]

        match = self.v3_pattern.search(rewritten_url)
        if match:
            url = match.group('url')
            singleSlash = self.v3_single_slash.findall(url)
            if singleSlash and len(singleSlash[0]) == 2:
                url = singleSlash[0][0] + "/" + singleSlash[0][1]
            encoded_url = unquote(url)
            enc_bytes = match.group('enc_bytes')
            enc_bytes += '=='
            self.dec_bytes = (urlsafe_b64decode(enc_bytes)).decode('utf-8')
            self.current_marker = 0
            return substitute_tokens(encoded_url)
        else:
            raise ValueError('Error parsing URL')

@app.route('/', methods=['GET', 'POST'])
def index():
    decoded_url = ''
    if request.method == 'POST':
        rewritten_url = request.form['url']
        decoder = URLDefenseDecoder()
        try:
            decoded_url = decoder.decode(rewritten_url)
        except ValueError as e:
            decoded_url = str(e)

    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <center>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>ProofPoint URL Defense Decoder</title>
            <style>
                body {
                    background-color: black;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                input[type=text], input[type=submit] {
                    padding: 10px;
                    margin: 5px;
                    border: none;
                    border-radius: 5px;
                }
                input[type=text] {
                    width: 300px;
                }
                input[type=submit] {
                    background-color: white;
                    color: black;
                    cursor: pointer;
                }
                button {
                    padding: 10px;
                    margin: 5px;
                    border: none;
                    border-radius: 5px;
                    background-color: white;
                    color: black;
                    cursor: pointer;
                }
            </style>
            <script>
                function copyToClipboard() {
                    const urlText = document.getElementById('decodedUrl');
                    navigator.clipboard.writeText(urlText.textContent)
                        .then(() => {
                            alert('Copied to clipboard!');
                        })
                        .catch(err => {
                            console.error('Error copying text: ', err);
                        });
                }
            </script>
        </head>
        <body>
            <h1>ProofPoint URL Defense Decoder</h1>
            <form method=post>
                <label for=url>Enter URL:</label>
                <input type=text name=url required>
                <input type=submit value=Decode>
            </form>
            {% if decoded_url %}
            <h2>Decoded URL:</h2>
            <p id="decodedUrl">{{ decoded_url }}</p>
            <button onclick="copyToClipboard()">Copy URL to Clipboard</button>
            {% endif %}
        </body>
        </center>
        </html>
    ''', decoded_url=decoded_url)

if __name__ == '__main__':
    app.run(debug=True)
