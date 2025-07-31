import mailparser
import re
import hashlib
import glob
import base64
from datetime import datetime

# Print tool name and author credit
print("=========================================")
print("        Yet Another Email Analyzer       ")
print("         Powered by Coffee Beans         ")
print("=========================================")

# Function to calculate MD5 checksum from binary data
def calculate_md5(data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()

# Function to print section with a banner
def create_section(title, content):
    return f"\n{'=' * 40}\n{title}\n{'=' * 40}\n{content}\n{'-' * 40}"

# Get current date for filenames
current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
markdown_file = f'C:\\Temp\\PHISH_REPORT_{current_date}.md'
html_file = f'C:\\Temp\\PHISH_REPORT_{current_date}.html'

# Prepare to write to files
with open(markdown_file, 'w') as md_file, open(html_file, 'w') as html_file:
    # Write HTML header with CSS for black background and white text
    html_file.write("""
    <html>
    <head>
        <title>Yet Another Email Analyzer</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                white-space: pre-wrap;
            }
            h1 {
                color: #00FF00; /* Bright green for main title */
            }
            h2, h3 {
                color: #00FF00; /* Bright green for headings */
            }
            pre {
                background-color: #222; /* Dark background for preformatted text */
                padding: 10px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>Yet Another Email Analyzer</h1>
    """)

    # Process each .eml file
    for file_path in glob.glob(r'C:\Temp\PHISH\*.eml'):
        md_file.write(f"\nProcessing file: {file_path}\n")
        html_file.write(f"<h2>Processing file: {file_path}</h2>")

        # Calculate MD5 of the email file
        with open(file_path, 'rb') as f:
            email_content = f.read()
            email_md5 = calculate_md5(email_content)

        mail = mailparser.parse_from_file(file_path)

        # Section 1: Addresses
        addresses_content = (
            f"Sender: {mail.from_}\n"
            f"To: {mail.to}\n"
            f"Cc: {mail.cc}\n"
            f"Bcc: {mail.bcc}\n"
            f"Reply-To: {mail.reply_to}\n"
        )
        section_md = create_section("ADDRESSES", addresses_content)
        md_file.write(section_md)
        html_file.write(f"<h3>ADDRESSES</h3><pre>{addresses_content}</pre>")

        # Section 2: Security - Extract DMARC, DKIM, and SPF results from headers
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
        section_md = create_section("SECURITY", security_content)
        md_file.write(section_md)
        html_file.write(f"<h3>SECURITY</h3><pre>{security_content}</pre>")

        # Section 3: ARTIFACTS
        urls = re.findall(r'(https?://[^\s]+)', mail.body)
        urls_content = "\n".join(urls)  # Simple copy/paste option for URLs
        artifacts_content = f"URLs:\n{urls_content}\n\nAttachments:\n"

        # Process attachments
        for attachment in mail.attachments:
            # Decode the base64 payload and calculate MD5
            if attachment['payload']:
                decoded_payload = base64.b64decode(attachment['payload'])
                attachment_md5 = calculate_md5(decoded_payload)
                vt_link = f"https://www.virustotal.com/gui/home/search/{attachment_md5}"
                artifacts_content += f"- {attachment['filename']}: <a href='{vt_link}' target='_blank'>MD5: {attachment_md5}</a>\n"

        section_md = create_section("ARTIFACTS", artifacts_content)
        md_file.write(section_md)
        html_file.write(f"<h3>ARTIFACTS</h3><pre>{artifacts_content}</pre>")

        # Section 4: HOPS
        hops_content = []
        for index, received_header in enumerate(mail.headers.get('Received', []), start=1):
            hops_content.append(f"Hop{index}: {received_header.strip()}")
        
        if hops_content:
            hops_section = "\n".join(hops_content)
        else:
            hops_section = "No hop information available."
        
        section_md = create_section("HOPS", hops_section)
        md_file.write(section_md)
        html_file.write(f"<h3>HOPS</h3><pre>{hops_section}</pre>")

        # Section 5: MD5-CHECKSUM
        section_md = create_section("EMAIL MD5-CHECKSUM", f"Checksum: {email_md5}")
        md_file.write(section_md)
        html_file.write(f"<h3>EMAIL MD5-CHECKSUM</h3><pre>Checksum: {email_md5}</pre>")

        # Section 6: OUTPUT
        output_content = "\n".join(f"{key}: {value}" for key, value in mail.headers.items())
        section_md = create_section("OUTPUT", output_content)
        md_file.write(section_md)
        html_file.write(f"<h3>OUTPUT</h3><pre>{output_content}</pre>")

    # Write HTML footer
    html_file.write("</body></html>")

print(f"Reports generated: {markdown_file}, {html_file.name}")
