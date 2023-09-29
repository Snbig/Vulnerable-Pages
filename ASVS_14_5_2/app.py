from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/protected', methods=['GET'])
def protected_route():
    # Retrieve the 'Origin' header from the request
    origin = request.headers.get('Origin')

    # Define a list of allowed origins
    allowed_origins = ['http://localhost:5151']  # Update with your allowed origins

    # Check if the provided origin is in the allowed origins
    if origin in allowed_origins:
        # If it matches, create a response with a JSON message
        response = jsonify({'message': 'This is a protected route!'})
        
        # Set the 'Access-Control-Allow-Origin' header to the provided origin
        response.headers['Access-Control-Allow-Origin'] = origin
        
        # Return the response
        return response
    else:
        # If the origin is not allowed, return a JSON error response with a 403 status code
        return jsonify({'error': 'Origin not allowed.'}), 403

@app.route('/')
def serve_html():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
