from flask import Flask, jsonify
from flask_cors import CORS
import os
from time import sleep 

def runApp():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para toda la aplicación

    @app.route('/move', methods=['GET'])
    def move():
        """Funcion per a manejar la acción move"""
        # Genera la peticio per a la logica
        f = open("move_req.txt","w",encoding='utf-8')
        f.write("m")
        f.close()

        # Espera fins que el fitxer de resposta es generat
        response = False
        while ( not response): 
            if "move_res.txt" in os.listdir(): response = True  
            sleep(2)
        # Llegeix el fitxer de resposta i construeix el missatge de retorn
        res = open("move_res.txt",'r')
        move = res.read() 
        res.close()
        os.remove("move_res.txt")
        message  ='Move action executed successfully, move sent: ' + move 

        return jsonify({'message': message })

    @app.route('/hint', methods=['GET'])
    def hint():
        """Funcion per a manejar la acción hint"""
        # Genera la peticio per a la logica
        f = open("hint_req.txt","w",encoding='utf-8')
        f.write("h")
        f.close()


        # Espera fins que el fitxer de resposta es generat
        response = False
        while ( not response): 
            if "hint_res.txt" in os.listdir(): response = True  
            sleep(2)
        
        # Llegeix el fitxer de resposta i construeix el missatge de retorn
        res = open("hint_res.txt",'r')
        move = res.read() 
        res.close()
        os.remove("hint_res.txt")
        message  ='Hint action executed successfully, hint: ' + move 

        return jsonify({'message': message })

    @app.route('/undo', methods=['GET'])
    def undo():
        """Funcion per a manejar la acción undo"""
        # Genera la peticio per a la logica
        f = open("undo_req.txt","w",encoding='utf-8')
        f.write("u")
        f.close()

        # Espera fins que el fitxer de resposta es generat
        response = False
        while ( not response): 
            if "undo_res.txt" in os.listdir(): response = True  
            sleep(2)
        # Llegeix el fitxer de resposta i construeix el missatge de retorn
        res = open("undo_res.txt",'r')
        move = res.read() 
        res.close()
        os.remove("undo_res.txt")
        message  ='Undo action executed successfully.'

        return jsonify({'message': message })

    app.run('0.0.0.0',5000)
if __name__ == '__main__':
    runApp()
   
