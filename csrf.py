from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

# Simula una base de datos de usuarios con sus saldos
user_balances = {
    "user1": 1000,
    "user2": 500
}

@app.route('/transfer', methods=['POST'])
def transfer():
    # Parámetros de la transferencia
    sender = request.form.get("sender")
    recipient = request.form.get("recipient")
    amount = float(request.form.get("amount"))

    # Verificar si los usuarios existen y el remitente tiene fondos suficientes
    if sender in user_balances and recipient in user_balances and user_balances[sender] >= amount:
        user_balances[sender] -= amount
        user_balances[recipient] += amount
        return jsonify({"message": "Transferencia realizada con éxito"}), 200
    else:
        return jsonify({"message": "Error en la transferencia"}), 400

# Inicio del servidor en el puerto 5000
if __name__ == "__main__":
    app.run(debug=True)