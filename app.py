from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
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
def index():
    error_message = None

    if request.method == 'POST':
        xml_data = request.data.decode('utf-8')

        try:
            # Parse XML data
            xml_tree = etree.fromstring(xml_data)

            # Validate XML against the XSD schema
            if schema.validate(xml_tree):
                # Extract data from the validated XML
                username = xml_tree.find('.//username').text
                email = xml_tree.find('.//email').text

                # Process the data (you can perform further processing here)
                # For demonstration purposes, we just print the data
                print(f"Username: {username}, Email: {email}")
                return '', 200  # Successful response

            else:
                error_message = 'Invalid XML format. Please check your input.'

        except etree.XMLSyntaxError as e:
            error_message = f'Error parsing XML: {str(e)}'

        return error_message, 400  # Bad request response

    return render_template('ASVS_13_3_1/index.html', error_message=error_message)


@app.route('/')
def redirectToGitPage():
    return redirect("https://snbig.github.io/Vulnerable-Pages/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
