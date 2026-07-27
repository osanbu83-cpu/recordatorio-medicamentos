from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_from_directory
import os
import json
from pywebpush import webpush
from pywebpush import WebPushException

app = Flask(__name__)

VAPID_PUBLIC_KEY = 'BEl62iUYgUivxIkv69yViEuiBIa-Ib9-SkvMeAtA3LFgDzkrxZJjSgSnfckjBJuBkr3qBUYIHBQFLXYUW5NxhAI'
VAPID_PRIVATE_KEY = 'TU_LLAVE_PRIVADA_VAPID'
VAPID_CLAIMS = {
    "sub": "mailto:tu-correo@example.com"
}

push_subscriptions = []

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(
        '.',
        'manifest.json'
    )

@app.route('/pwabuilder-sw.js')
def serve_sw():
    return send_from_directory(
        '.',
        'pwabuilder-sw.js'
    )

@app.route('/subscribe', methods=['POST'])
def subscribe():
    sub = request.get_json(silent=True)
    if sub:
        if sub not in push_subscriptions:
            push_subscriptions.append(sub)
        return jsonify(
            {"status": "success"}
        ), 200
    return jsonify(
        {"status": "ignored"}
    ), 200

@app.route('/send-notification', methods=['POST'])
def send_notification():
    datos = request.get_json(silent=True)
    if datos is None:
        datos = {}
    
    mensaje = datos.get(
        'message',
        'Toma tu medicina'
    )
    results = []
    
    for sub in push_subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=mensaje,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            results.append(
                {"status": "success"}
            )
        except WebPushException as ex:
            results.append(
                {
                    "status": "error",
                    "message": str(ex)
                }
            )
            
    final = {
        "status": "completed",
        "results": results
    }
    return jsonify(final)

if __name__ == '__main__':
    app.run(debug=True)
