from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# ASVS 14.5.2
@app.route('/protected')
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
@app.route('/accounts/<account_id>')
@cross_origin(send_wildcard=True, methods=['DELETE'])
def delete_account(account_id):
    accounts = ['victim_123']
    if request.method == "DELETE":
        if account_id in accounts:
            return jsonify({'message': f'Account {account_id} successfully deleted'}), 204
        else:
            return jsonify({'error': 'Account not found'}), 404

@app.route('/')
def redirectToGitPage():
    return redirect("https://snbig.github.io/Vulnerable-Pages/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
