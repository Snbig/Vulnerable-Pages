from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# ASVS 14.5.2
@app.route('/protected')
@cross_origin(origins=['http://localhost'], methods=['GET'])
def protected_route():
    response = jsonify({'message': 's3cR3t'})
    return response

# ASVS 14.5.3
@app.route('/CORS')
@cross_origin(send_wildcard=True)
def CORS():
    response = jsonify({'message': 's3cR3t'})
    return response

@app.route('/')
def redirect():
    return redirect("https://github.com/Snbig/Vulnerable-Pages", code=302)

if __name__ == '__main__':
    app.run(debug=True)
