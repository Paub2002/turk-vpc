import pathlib
import textwrap

import google.generativeai as genai



from IPython.display import display
from IPython.display import Markdown
MAX_TOKENS = 50

genai.configure(api_key="AIzaSyBkOZdm6YCL9JyD7eahYcm8GIlYU5C2rIw")


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def get_models():
  for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)

model = genai.GenerativeModel('gemini-1.5-flash')

#print("\n |||||||||||||||||||||||||||||\n" + question)
model.max_output_tokens = MAX_TOKENS

def make_a_question(question):
  model.max_output_tokens = MAX_TOKENS
  while True:
    response = model.generate_content(question)
    try:        
        response_text = response.text  # Esto puede lanzar un ValueError
        break  # Si no se lanza una excepción, salimos del bucle
    except ValueError:
        # Si se lanza un ValueError, imprimimos los candidates y continuamos el bucle
        print("\nLoading.")
        print("Loading..")
        print("Loading...\n")
  print(response_text)
  return response_text

def chess_question(fen_string,player_move_alg,best_move_alg):
  model.max_output_tokens = MAX_TOKENS
  question = "Estado inicial de la partida es este: " + fen_string + " \n El jugador ha hecho este movimiento: " + player_move_alg + "\n Stockfish dice que este es el mejor movimiento: " + best_move_alg + "\n Explica porque la jugada que propone Stockfish es mejor que la jugada del jugador."
  while True:
    response = model.generate_content(question)
    try:        
        response_text = response.text  # Esto puede lanzar un ValueError
        break  # Si no se lanza una excepción, salimos del bucle
    except ValueError:
        # Si se lanza un ValueError, imprimimos los candidates y continuamos el bucle
        print("\nLoading.")
        print("Loading..")
        print("Loading...\n")
  print(response_text)
  return response_text

#make_a_question(question)
#chess_question()
#get_models()