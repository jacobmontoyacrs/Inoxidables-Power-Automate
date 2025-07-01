from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/sendLead', methods=['POST'])
def send_lead():
    incoming = request.get_json()

    # Extraer los campos requeridos
    nombre = incoming.get("nombre")
    telefono = incoming.get("telefono")
    email = incoming.get("email")
    producto_interes = incoming.get("productoInteres")
    sucursal = incoming.get("sucursal")
    resumen = incoming.get("resumen")

    # Validación básica del campo obligatorio
    if not nombre:
        return jsonify({"error": "Falta el campo 'nombre' en el cuerpo"}), 400

    # URL del flujo de Power Automate
    power_url = "https://2f0b93c9f2c7e3aab1073bf70c3bd6.1d.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/3c29ed8fa88740d184f929fff41605d7/triggers/manual/paths/invoke/?api-version=1&tenantId=tId&environmentName=2f0b93c9-f2c7-e3aa-b107-3bf70c3bd61d&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=a7aXGkNgNViwySteff2pfqxSixcN3Lp6ecqHYCYYuL0"

    headers = {
        "Content-Type": "application/json"
    }

    # Cuerpo que se enviará al flujo
    data = {
        "nombre": nombre,
        "telefono": telefono,
        "email": email,
        "productoInteres": producto_interes,
        "sucursal": sucursal,
        "resumen": resumen
    }

    # Llamar al flujo
    response = requests.post(power_url, headers=headers, data=json.dumps(data))

    return jsonify({
        "status": response.status_code,
        "flow_response": response.text
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
