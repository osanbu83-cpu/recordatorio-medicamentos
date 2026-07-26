from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(
        '.', 'manifest.json'
    )

@app.route('/pwabuilder-sw.js')
def serve_sw():
    return send_from_directory(
        '.', 'pwabuilder-sw.js'
    )

if __name__ == '__main__':
    app.run(debug=True)
