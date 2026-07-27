from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from pywebpush import webpush, WebPushException

app = Flask(__name__)

# Llaves VAPID para firmar las notificaciones push
VAPID_PUBLIC_KEY = 'BEl62iUYgUivxIkv69yViEuiBIa-Ib9-SkvMeAtA3LFgDzkrxZJjSgSnfckjBJuBkr3qBUYIHBQFLXYUW5NxhAI'
VAPID_PRIVATE_KEY = 'TU_LLAVE_PRIVADA_VAPID'
VAPID_CLAIMS = {
    "sub": "mailto:tu-correo@example.com"
}

# Almacenamiento temporal en memoria para las suscripciones de los dispositivos
push_subscriptions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('.', 'manifest.json')

@app.route('/pwabuilder-sw.js')
def serve_sw():
    return send_from_directory('.', 'pwabuilder-sw.js')

# Ruta para registrar el teléfono
@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription = request.get_json()
    if subscription:
        if subscription not in push_subscriptions:
            push_subscriptions.append(subscription)
        return jsonify({"status": "success", "message": "Suscrito correctamente"})
    return jsonify({"status": "error", "message": "Suscripción inválida"}), 400

# Ruta para disparar la notificación push real hacia los dispositivos registrados
@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    mensaje = data.get('message', '¡Es hora de tomar tu medicina!')
    
    results = []
    for sub in push_subscriptions:
        try:
            response = webpush(
                subscription_info=sub,
                data=mensaje,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            results.append({"status": "success"})
        except WebPushException as ex:
            print(f"Error al enviar push: {ex}")
            results.append({"status": "error", "message": str(ex)})
            
    return jsonify({"status": "completed", "results": results})

if __name__ == '__main__':
    app.run(debug=True)
