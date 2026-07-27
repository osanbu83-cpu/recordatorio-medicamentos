from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Almacenamiento temporal en memoria para las suscripciones push de los dispositivos
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

# Ruta para registrar el teléfono de tu mamá cuando acepte las notificaciones
@app.route('/subscribe', methods=['POST'])
def subscribe():
    subscription = request.get_json()
    if subscription and subscription not in push_subscriptions:
        push_subscriptions.append(subscription)
    return jsonify({"status": "success", "message": "Dispositivo registrado correctamente"})

# Ruta para simular o disparar el envío de la alarma del medicamento
@app.route('/send-notification', methods=['POST'])
def send_notification():
    # Aquí implementaremos el envío real con pywebpush en cuanto configuremos las llaves
    data = request.get_json()
    mensaje = data.get('message', '¡Es hora de tomar el medicamento!')
    
    return jsonify({"status": "sent", "total_subscribers": len(push_subscriptions), "message": mensaje})

if __name__ == '__main__':
    app.run(debug=True)
