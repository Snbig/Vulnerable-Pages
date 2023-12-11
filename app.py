from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
import xmlschema
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
def checkXSD():
    xsd_schema = """
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="user">
        <xs:complexType>
        <xs:sequence>
            <xs:element name="username" type="xs:string"/>
            <xs:element name="email" type="xs:string"/>
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
            schema.validate(xml_data)

            # Parse XML data using xml.etree.ElementTree
            xml_tree = ET.fromstring(xml_data)

            # Extract data from the validated XML
            username = xml_tree.find('.//username').text
            email = xml_tree.find('.//email').text

            # Process the data (you can perform further processing here)
            # For demonstration purposes, we just print the data
            print(f"Username: {username}, Email: {email}")
            return '', 200  # Successful response

        except xmlschema.XMLSchemaValidationError as e:
            error_message = f'Error validating XML against XSD schema: {str(e)}'
        except ET.ParseError as e:
            error_message = f'Error parsing XML: {str(e)}'

        return error_message, 400  # Bad request response

    return render_template('ASVS_13_3_1/index.html', error_message=error_message)


@app.route('/')
def redirectToGitPage():
    return redirect("https://snbig.github.io/Vulnerable-Pages/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
