from flask import Flask, jsonify
from flask_cors import CORS
import io 
import os
import time

def runApp():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para toda la aplicación

    @app.route('/move', methods=['GET'])
    def move():
        # Lógica para manejar la acción "move"
        f = open("move_req.txt","w",encoding='utf-8')
        f.write("m")
        f.close()

        response = False
        while ( not response): 
            if "move_res.txt" in os.listdir(): response = True  
            time.sleep(2)
        res = open("move_res.txt",'r')
        move = res.read() 
        message  ='Move action executed successfully, move sent: ' + move 

        return jsonify({'message': message })

    @app.route('/hint', methods=['GET'])
    def hint():
        f = open("hint_req.txt","w",encoding='utf-8')
        f.write("h")
        f.close()

        response = False
        while ( not response): 
            if "hint_res.txt" in os.listdir(): response = True  
            time.sleep(2)
        res = open("hitnt_res.txt",'r')
        move = res.read() 
        message  ='Hint action executed successfully, hint: ' + move 

        return jsonify({'message': message })

    @app.route('/undo', methods=['GET'])
    def undo():
        f = open("undo_req.txt","w",encoding='utf-8')
        f.write("u")
        f.close()

        response = False
        while ( not response): 
            if "undo_res.txt" in os.listdir(): response = True  
            time.sleep(2)
        res = open("undo_res.txt",'r')
        move = res.read() 
        message  ='Undo action executed successfully.'

        return jsonify({'message': message })

    app.run('0.0.0.0',5000)
if __name__ == '__main__':
    runApp()
   
