from flask import Flask, request, jsonify, render_template, redirect
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS, cross_origin
import xml.etree.ElementTree as ET
import xmlschema
from jsonschema import validate, ValidationError
import zipfile
import Libs.zipfile as vulnerable_zipfile
from io import BytesIO

app = Flask(__name__, template_folder='.')

# ASVS 14.5.2
@app.route('/protected', methods=['GET'])
@cross_origin(origins=['http://localhost'], methods=['GET'])
def protected_route():
    origin = request.headers.get('Origin')
    if origin == 'http://localhost':
        response = jsonify({'message': 's3cR3t'})
        return response
    else:
        response = jsonify({'message': 'Forbidden. Bad Origin.'})
        return response, 403


# ASVS 14.5.3
@app.route('/accounts/<account_id>', methods=['DELETE'])
@cross_origin(send_wildcard=True, methods=['DELETE'])
def delete_account(account_id):
    accounts = ['victim_123']
    if account_id in accounts:
        return jsonify({'message': f'Account {account_id} successfully deleted'}), 204
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
                  file_in_memory = BytesIO(file.read())
                  # Open the ZIP file from the in-memory stream
                  try:
                    with vulnerable_zipfile.ZipFile(file_in_memory, 'r') as zip_ref:
                      # Process the ZIP file contents here (e.g., iterate through files, extract specific files)
                      file_names = zip_ref.namelist()
                      content = {'files': file_names}
                      zip_ref.extractall(pwd="42")
                      return jsonify(content), 200
                  except Exception as e:
                    return jsonify({'error': f'Error processing ZIP file: {str(e)}'}), 500
            else:
                return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            return jsonify({'error': 'File type not allowd.'}), 415
    
    except RequestEntityTooLarge as e:
        return jsonify({'error': str(e)}), 413
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def redirectToGitPage():
    return redirect("https://snbig.github.io/Vulnerable-Pages/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
