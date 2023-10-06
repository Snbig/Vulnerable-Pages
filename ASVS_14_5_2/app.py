from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/protected', methods=['GET', 'OPTIONS'])
def protected_route():
    # Retrieve the 'Origin' header from the request
    origin = request.headers.get('Origin')

    # Define a list of allowed origins
    allowed_origins = ['http://localhost', 'https://spotless-frog-wetsuit.cyclic.cloud']  # Update with your allowed origins

    # Check if the provided origin is in the allowed origins
    if origin in allowed_origins:
        # If it matches, create a response with a JSON message
        response = jsonify({'message': 'This is a protected route!'})
        
        # Set the 'Access-Control-Allow-Origin' header to the provided origin
        response.headers['Access-Control-Allow-Origin'] = origin
        
        # Return the response
        return response
    elif not origin:
        response = jsonify({'message': 'no Origin header.'})
        response.headers['Access-Control-Allow-Origin'] = "null"
        return response, 403
    else:
        # If the origin is not allowed, return a JSON error response with a 403 status code
        response = jsonify({'error': 'Origin not allowed.'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response, 403

@app.route('/')
def serve_html():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
