import mailparser
import re
import hashlib
import glob
import base64
import string
from datetime import datetime
from urllib.parse import unquote
from html import unescape

# URLDefenseDecoder class to handle URL decoding
class URLDefenseDecoder(object):
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
            version = match.group(1)
            if version == 'v1':
                return self.decode_v1(rewritten_url)
            elif version == 'v2':
                return self.decode_v2(rewritten_url)
            elif version == 'v3':
                return self.decode_v3(rewritten_url)
            else:
                raise ValueError('Unrecognized version in: ', rewritten_url)
        else:
            raise ValueError('Does not appear to be a URL Defense URL')

    def decode_v1(self, rewritten_url):
        match = self.v1_pattern.search(rewritten_url)
        if match:
            url_encoded_url = match.group('url')
            html_encoded_url = unquote(url_encoded_url)
            url = unescape(html_encoded_url)
            return url
        else:
            raise ValueError('Error parsing URL')

    def decode_v2(self, rewritten_url):
        match = self.v2_pattern.search(rewritten_url)
        if match:
            special_encoded_url = match.group('url')
            url_encoded_url = special_encoded_url.replace('-', '%').replace('_', '/')
            html_encoded_url = unquote(url_encoded_url)
            url = unescape(html_encoded_url)
            return url
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
            enc_bytes = match.group('enc_bytes') + '=='
            self.dec_bytes = base64.urlsafe_b64decode(enc_bytes).decode('utf-8')
            self.current_marker = 0
            return substitute_tokens(encoded_url)
        else:
            raise ValueError('Error parsing URL')

# Main processing script
def main():
    output_html_file = f'C:\\Temp\\PHISH_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'

    with open(output_html_file, 'w', encoding='utf-8') as html_file:
        # Write HTML header
        html_file.write("""
        <html>
        <head>
            <title>YAEA</title>
            <style>
                body {
                    background-color: #f0f0f0; /* Light grey background */
                    color: black; /* Black text */
                    font-family: Arial, sans-serif;
                    white-space: pre-wrap;
                }
                h1 {
                    color: #00FF00; /* Bright green for main title */
                }
                h2, h3 {
                    color: red; /* Red for section headers */
                    cursor: pointer; /* Change cursor to pointer for headers */
                }
                pre {
                    background-color: #222; /* Dark background for preformatted text */
                    color: white; /* White text in preformatted text */
                    padding: 10px;
                    border-radius: 5px;
                }
                .output {
                    display: none; /* Hidden by default */
                    margin-top: 10px;
                }
            </style>
            <script>
                function toggleOutput(id) {
                    var output = document.getElementById(id);
                    if (output.style.display === "none") {
                        output.style.display = "block";
                    } else {
                        output.style.display = "none";
                    }
                }
            </script>
        </head>
        <body>
            <h1>Yet Another Email Analyzer</h1>
        """)

        urldefense_decoder = URLDefenseDecoder()

        # Process each .eml file in the specified directory
        for email_file in glob.glob(r'C:\Temp\PHISH\*.eml'):
            html_file.write(f"<h2>Processing file: {email_file}</h2>")
            mail = mailparser.parse_from_file(email_file)
            
            # Section 1: ADDRESSES
            addresses_content = (
                f"Sender: {mail.from_}\n"
                f"To: {mail.to}\n"
                f"Subject: {mail.subject}\n"
                f"Cc: {mail.cc}\n"
                f"Bcc: {mail.bcc}\n"
                f"Reply-To: {mail.reply_to}\n"
            )
            html_file.write(f"<h3 onclick=\"toggleOutput('addresses_{email_file}')\">ADDRESSES & SUBJECT</h3><pre id='addresses_{email_file}' class='output'>{addresses_content}</pre>")

            # Section 2: SECURITY
            auth_results = mail.headers.get('Authentication-Results', '')
            dkim_result = re.search(r'dkim=(\w+)', auth_results)
            dkim_result = dkim_result.group(1) if dkim_result else 'N/A'
            dmarc_result = re.search(r'dmarc=(\w+)', auth_results)
            dmarc_result = dmarc_result.group(1) if dmarc_result else 'N/A'
            spf_result = re.search(r'spf=(\w+)', auth_results)
            spf_result = spf_result.group(1) if spf_result else 'N/A'

            security_content = (
                f"DKIM: {dkim_result}\n"
                f"DMARC: {dmarc_result}\n"
                f"SPF: {spf_result}\n"
            )
            html_file.write(f"<h3 onclick=\"toggleOutput('security_{email_file}')\">SECURITY</h3><pre id='security_{email_file}' class='output'>{security_content}</pre>")

            # Section 3: ARTIFACTS
            urls = re.findall(r'https://urldefense\.com/[^\s]+', mail.body)
            decoded_urls = []

            for url in urls:
                try:
                    decoded_url = urldefense_decoder.decode(url)
                    decoded_urls.append(decoded_url)
                except ValueError as e:
                    html_file.write(f"<p>Error decoding URL: {e}</p>")

            if decoded_urls:
                html_file.write(f"<h3 onclick=\"toggleOutput('decoded_urls_{email_file}')\">Decoded URLs</h3><pre id='decoded_urls_{email_file}' class='output'>{chr(10).join(decoded_urls)}</pre>")

            # Section 4: BODY
            body_content = mail.body
            body_text = unescape(body_content)  # Convert HTML to text
            html_file.write(f"<h3 onclick=\"toggleOutput('body_{email_file}')\">BODY</h3><pre id='body_{email_file}' class='output'>{body_text}</pre>")

            # Section 5: HOPS
            hops_content = []
            for index, received_header in enumerate(mail.headers.get('Received', []), start=1):
                hops_content.append(f"Hop{index}: {received_header.strip()}")
            
            hops_section = "\n".join(hops_content) if hops_content else "No hop information available."
            html_file.write(f"<h3 onclick=\"toggleOutput('hops_{email_file}')\">HOPS</h3><pre id='hops_{email_file}' class='output'>{hops_section}</pre>")

            # Section 6: OUTPUT
            output_content = "\n".join(f"{key}: {value}" for key, value in mail.headers.items())
            html_file.write(f"<h3 onclick=\"toggleOutput('output_{email_file}')\">OUTPUT</h3><pre id='output_{email_file}' class='output'>{output_content}</pre>")

        # Write HTML footer
        html_file.write("</body></html>")

    print(f"Report generated: {output_html_file}")

if __name__ == '__main__':
    main()
