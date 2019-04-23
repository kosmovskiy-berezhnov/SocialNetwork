from flask import render_template
from api.__init__ import app


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
