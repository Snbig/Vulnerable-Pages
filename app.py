from flask import Flask, request, jsonify, render_template, redirect, render_template_string
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS, cross_origin
import os
import xml.etree.ElementTree as ET
import xmlschema
from jsonschema import validate, ValidationError
import uuid
import pyzipper
from io import BytesIO
import shutil
import urllib
from pathlib import Path
from urllib.parse import urlparse
import requests

app = Flask(__name__, template_folder='.')

# ASVS 14.5.2
@app.route('/protected', methods=['GET'])
@cross_origin(origins=['https://snbig.github.io'], methods=['GET', 'POST'])
def protected_route():
    origin = request.headers.get('Origin')
    if origin == 'http://localhost':
        response = jsonify({'message': 's3cR3t'})
        return response
    else:
        response = jsonify({'message': 'Forbidden. Bad Origin.'})
        return response, 403


# ASVS 14.5.3
@app.route('/accounts/<account_id>', methods=['GET'])
@cross_origin(send_wildcard=True, methods=['GET'])
def delete_account(account_id):
    accounts = ['victim_123']
    if account_id in accounts:
        return 's3cR3t: ASVS{Th3_Secret_Code_Is_4n_E4sy_T1me}', 200
    else:
        return jsonify({'error': 'Account not found'}), 404


# ASVS 13.3.1
@app.route('/submit-xml', methods=['GET', 'POST'])
@cross_origin(origins=['https://snbig.github.io'], methods=['GET', 'POST'])
def checkXSD():
    xsd_schema = """
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="user">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="username" type="xs:string"/>
                <xs:element name="email">
                    <xs:simpleType>
                        <xs:restriction base="xs:string">
                            <!-- Add a pattern for email validation -->
                            <xs:pattern value="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"/>
                        </xs:restriction>
                    </xs:simpleType>
                </xs:element>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
    </xs:schema>
    """
    error_message = None

    if request.method == 'POST':
        xml_data = request.data.decode('utf-8')

        try:
            # Validate XML against the XSD schema
            schema = xmlschema.XMLSchema(xsd_schema)
            schema.validate(xml_data)

            # Parse XML data using xml.etree.ElementTree
            xml_tree = ET.fromstring(xml_data)

            # Extract data from the validated XML
            username = xml_tree.find('.//username').text
            email = xml_tree.find('.//email').text

            # Process the data (you can perform further processing here)
            return '', 200  # Successful response

        except xmlschema.XMLSchemaValidationError as e:
            error_message = f'Error validating XML against XSD schema: {str(e)}'
        except ET.ParseError as e:
            error_message = f'Error parsing XML: {str(e)}'

        return error_message, 400  # Bad request response

    return render_template('ASVS_13_3_1/index.html', error_message=error_message)


# ASVS 13.2.2
@app.route('/submit-json', methods=['POST'])
@cross_origin(origins=['https://snbig.github.io'], methods=['POST'])
def checkJSONSchema():
    json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0, "maximum": 150}
    },
    "required": ["name", "age"]
    }
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate JSON data against the defined schema
        validate(data, json_schema)

        # If validation is successful, process the data
        result = f"Data received: {data}"
        return jsonify({"status": "success", "result": result})

    except ValidationError as e:
        # Handle validation errors
        error_message = f"Invalid input. {e.message}"
        return jsonify({"status": "error", "message": error_message}), 400


# ASVS 12.1.1
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'docx', 'zip']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@cross_origin(origins=['https://snbig.github.io'], methods=['POST'])
def upload_file():
    MAX_FILE_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Check file size during upload
        if request.content_length > MAX_FILE_SIZE_BYTES:
            raise RequestEntityTooLarge(f'File size ({request.content_length / 1024 / 1024} MB) exceeds the maximum allowed size ({MAX_FILE_SIZE_BYTES} bytes)')
        
        # Save the file to disk or perform further processing
        if file and allowed_file(file.filename):
            if file.filename.rsplit('.', 1)[1].lower() == 'zip':
                  tmp_folder = f'/tmp/{str(uuid.uuid4())}/'
                  file_in_memory = BytesIO(file.read())
                  # Open the ZIP file from the in-memory stream
                  try:
                    with pyzipper.AESZipFile(file_in_memory, 'r') as zip_ref:
                      # Process the ZIP file contents here (e.g., iterate through files, extract specific files)
                      file_names = zip_ref.namelist()
                      content = {'files': file_names}
                      zip_ref.extractall(path=tmp_folder)
                      shutil.rmtree(tmp_folder, ignore_errors=True)
                      return jsonify(content), 200
                  except Exception as e:
                    shutil.rmtree(tmp_folder, ignore_errors=True)
                    return jsonify({'error': f'Error processing ZIP file: {str(e)}'}), 500
            else:
                return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'error': 'File type not allowd.'}), 415
    
    except RequestEntityTooLarge as e:
        return jsonify({'error': str(e)}), 413
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ASVS 12.6.1
@app.route('/admin', methods=['GET'])
def admin():
    if request.remote_addr == '127.0.0.1' or request.remote_addr == 'localhost':
        return 'Welcom to Admin Panel'
    else:
        return 'Access denied. This route is only accessible locally.'

@app.route('/ssrf/<id>', methods=['POST','GET'])
@cross_origin(origins=['https://snbig.github.io'], methods=['POST'])

def ssrf(id):

    WHITELIST = ('oast.pro', 'oast.live', 'oast.site', 'oast.online', 'oast.fun', 'oast.me','google.com')

    if id == '1' and request.method == 'POST':

        url = request.json.get('url', '')
        if url:
            try:
                schema = urlparse(url).scheme
                path = urlparse(url).path
                if schema.lower() == "file":
                    if path == "/etc/passwd":
                        with open('./static/etc.txt', 'r') as file:
                            etc = file.read()
                        return etc
                    else:
                        return jsonify({"error":"Forbidden Path"}), 403
                else:
                    return jsonify({"error":"Just 'file' schema is allowed."}), 403       
            except Exception as e:
                return str(e), 500

        return jsonify({"error":"Bad URL"}), 400
    
    elif id == '2' :
        try:

            url = request.json.get('url', '')
            if url:
                schema = urlparse(url).scheme
                hostname = urlparse(url).hostname
                
                if schema.lower() in ['http', 'https']:
                    
                    if hostname:
                        
                        if hostname.endswith(WHITELIST):
                            response = requests.get(url).text
                            return response
                    
                        else:
                           return jsonify({"error": "forbidden hostname", "allowed hostnames": WHITELIST}) , 403
                    
                    else:
                        return jsonify({"error": "Enter a valid hostname"})
                
                else:
                    return jsonify({"error": "Just 'http' or 'https' schemas are allowed."})
                
            else:
                return jsonify({"error": "Enter a valid URL."})
                
        except Exception as e:
            return str(e), 500
        

    elif id == '3':
        try:
            url =request.json.get('url', '')
            if url:
                schema = urlparse(url).scheme
                hostname = urlparse(url).hostname
                path = urlparse(url).path
                port = urlparse(url).port

                if schema.lower() in ['http', 'https']:
                    
                    if hostname:
                        if hostname in ['127.1', '017700000001', '2130706433'] and path == '/admin' and not port :
                            return 'Welcom to Admin Panel'
                        
                        else:
                           return jsonify({"error": "forbidden PORT, PATH or HOSTNAME"}) , 403
                        
                    else:
                        return jsonify({"error": "Enter a valid hostname or port"})
                else:
                    return jsonify({"error": "Just 'http' or 'https' schemas are allowed."})
            else:
                return jsonify({"error": "Enter a valid URL."})
                
        except Exception as e:
            return str(e), 500

    
    else:
        return jsonify({"error":"Route Not Found"}), 404

# ASVS 5.1.5

@app.route('/redirect', methods=['GET'])
def open_redirect():
    try:
        redirect_url = request.args.get('url')
        if redirect_url:
            return redirect(redirect_url, code=302)
        else:
            return jsonify({"error":"url param is required"}), 400
    except Exception as e:
        return str(e), 500

# ASVS 12.3.3

@app.route('/rfi', methods=['GET', 'POST'])
def rfi():
    url = request.args.get('url')
    try:
        if url:
            response = requests.get(url)
            return render_template_string(response.text)
        else:
            return jsonify({"error":"NO URL Provided."}), 400
    except Exception as e:
        return str(e), 500            

# ASVS 5.3.3

@app.route('/xss')
def index():
    name = request.args.get('name', '')

    return '''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Greeting</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
          <link rel="stylesheet" href="https://snbig.github.io/Vulnerable-Pages/ASVS_5_3_3/style.css">
        </head>
        <body>
            <div class="container">
                <h1><i class="fas fa-smile icon"></i> Welcome!</h1>
                <form method="get">
                    <input type="text" name="name" placeholder="Enter your name" value="" required>
                    <button type="submit">Submit</button>
                </form>

                    <h2>Hello,%s!</h2>

            </div>
        </body>
        </html>
    ''' % name

# ASVS 5.2.5

@app.route('/ssti', methods=['GET', 'POST'])
@cross_origin(origins=['https://snbig.github.io'], methods=['POST','GET'])
def ssti():
    payload = request.args.get('c')
    if payload:
        return render_template_string(payload)
    else:
        return "Hello, send something inside the param 'c'!"

# ASVS 5.3.9

@app.route('/lfi', methods=['GET', 'POST'])
@cross_origin(origins=['*'], methods=['POST','GET'])
def lfi():
    page = request.args.get('page', 'home')
    try:
        return open(page).read()
    except FileNotFoundError:
        return 'Error'


@app.route('/')
def redirectToGitPage():
    return redirect("https://snbig.github.io/Vulnerable-Pages/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
