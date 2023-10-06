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
    else:
        response = jsonify({'message': 'Forbidden. Bad Origin.'})
    return response

# ASVS 14.5.3
@app.route('/CORS')
@cross_origin(send_wildcard=True)
def CORS():
    response = jsonify({'message': 's3cR3t'})
    return response

@app.route('/')
def redirectToGitPage():
    return redirect("https://snbig.github.io/Vulnerable-Pages/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
