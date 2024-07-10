from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

@app.route('/move', methods=['GET'])
def move():
    # Lógica para manejar la acción "move"
    return jsonify({'message': 'Move action executed successfully'})

@app.route('/hint', methods=['GET'])
def hint():
    # Lógica para manejar la acción "hint"
    return jsonify({'message': 'Hint action executed successfully'})

@app.route('/undo', methods=['GET'])
def undo():
    # Lógica para manejar la acción "undo"
    return jsonify({'message': 'Undo action executed successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
