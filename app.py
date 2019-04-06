from flask import render_template
import connexion

# Create the application instance
app = connexion.App(__name__, specification_dir='./swagger/')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
