from stockfish import Stockfish
import chess
import request
import speech
# import serial_com_python

LEVE_ERROR = 20
ERROR = 50
GRAVE_ERROR = 150

#stockfish = Stockfish(path="turk-vpc\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe", depth=7)
stockfish = Stockfish(path="stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe", depth=7)

board_indices = [
"h1","g1","f1","e1","d1","c1","b1","a1",
"h2","g2","f2","e2","d2","c2","b2","a2",
"h3","g3","f3","e3","d3","c3","b3","a3",
"h4","g4","f4","e4","d4","c4","b4","a4",
"h5","g5","f5","e5","d5","c5","b5","a5",
"h6","g6","f6","e6","d6","c6","b6","a6",
"h7","g7","f7","e7","d7","c7","b7","a7",
"h8","g8","f8","e8","d8","c8","b8","a8"
]

robot_indices = [
"00","01","02","03","04","05","06","07",
"10","11","12","13","14","15","16","17",
"20","21","22","23","24","25","26","27",
"30","31","32","33","34","35","36","37",
"40","41","42","43","44","45","46","47",
"50","51","52","53","54","55","56","57",
"60","61","62","63","64","65","66","67",
"70","71","72","73","74","75","76","77"    
]

def get_succession_of_best_moves(fen, depth):
    fen_succession = ""
    for _ in range(depth):
        best_move = stockfish.get_best_move()
        if not best_move:
            break
        stockfish.make_moves_from_current_position([best_move])
        fen_succession = fen_succession + stockfish.get_fen_position() + " ||| "
    stockfish.set_fen_position(fen)
    return fen_succession

def get_succession_of_best_moves_with_visuals(fen, depth):
    moves_with_visuals = []
    current_fen = fen
    for _ in range(depth):
        stockfish.set_position(current_fen)
        best_move = stockfish.get_best_move()
        if not best_move:
            break
        board_visual = stockfish.get_board_visual()
        moves_with_visuals.append((best_move, board_visual))
        stockfish.make_moves_from_current_position([best_move])
        current_fen = stockfish.get_fen_position()

    print("Succession of best moves with visuals:")
    for move, visual in moves_with_visuals:
        print(f"Move: {move}")
        print(visual)

def alg_to_alg(move, board):
    """
    Convert a move from algorithmic to algebraic notation.

    Parameters:
    move (str): The move in algorithmic notation, e.g., 'e2e4'.
    board (chess.Board): The current board state.

    Returns:
    str: The move in algebraic notation.
    """
    try:
        # Create a chess.Move object from the algorithmic move notation
        chess_move = chess.Move.from_uci(move)
        
        # Convert the move to algebraic notation using the board's state
        algebraic_move = board.san(chess_move)
        
        return algebraic_move
    except ValueError as e:
        print(f"Invalid move: {move} - {e}")
        return None
    
def es_negra(tablero, posicion):
    # Obtener el cuadrado de la posición
    cuadrado = chess.parse_square(posicion)
    
    # Obtener la pieza en ese cuadrado
    pieza = tablero.piece_at(cuadrado)
    # Verificar si la pieza es negra
    return pieza is not None and pieza.color == chess.BLACK

def getHintMove(fen_string):
    stockfish.set_fen_position(fen_string)
    posicion = stockfish.get_best_move()
    posicion = posicion[:2]
    text = "Si mueves la pieza en la posición " + posicion + " podrás hacer un muy buen movimiento, maestro"
    speech.text_to_speech(text)

    coords = [posicion,posicion]
    robotCoords = toRobotIndices(coords)
    print("DANI: ", str(robotCoords))
    #serial_com_python.movement(str(robotCoords))
    return posicion

def toRobotIndices(coords):
    for x in range(len(board_indices)):
        if board_indices[x] == coords[0]:
            break
    if len(coords) > 1:
        for y in range(len(board_indices)):
            if board_indices[y] == coords[1]:
                break
    result = str(x)+str(y)
    return result

def separateMove(ax):    
    coords = [ax[:2],ax[-2:]]
    return coords

def ilegalMove(move):    
    posicion = separateMove(move)
    robotCoords = toRobotIndices(posicion)
    print("DANI: ", str(robotCoords))
    #serial_com_python.movement(str(robotCoords))
    text = "Si mueves la pieza en la posición " + posicion[0] + " a la posición " + posicion[1] + " sería un movimiento ilegal, mameluco"
    speech.text_to_speech(text)




#/////////////////////////////////////////////////////////////////////////////////////////////////////////
def main_loop(board,move):
    bad_move = False
    #stockfish.set_skill_level(4)
    stockfish.set_elo_rating(2000)
    
    stockfish.set_fen_position(board.fen())
    #print(stockfish.get_board_visual())
    best_move = stockfish.get_best_move()

    initial_position = move[:2]
    final_position = move[-2:]

    #turn 1 = negras |turn 0 = blancas
    turn = es_negra(board, initial_position)

    if turn == player_color:
        initial_player = stockfish.get_evaluation()
        print("initial player: ", initial_player)
        print(move)

        stockfish.make_moves_from_current_position([move])
        print(stockfish.get_board_visual())

        initial_turk = stockfish.get_evaluation()
        print("initial turk: ", initial_turk)

        points = abs(initial_turk['value'] - initial_player['value'])
        print("initial_points: ", initial_player['value'], "final_points: ", initial_turk["value"])
        print("Points: ", points)
        
        if points >= GRAVE_ERROR:
            bad_move = True

        if bad_move:
            player_move_alg = alg_to_alg(move, board)
            best_move_alg = alg_to_alg(best_move, board)
            text = request.chess_question(board.fen(), player_move_alg, best_move_alg)
            speech.text_to_speech(text)
            print("Bad Move ma boy")
        else:
            print("Gooooooz cabrón")

        best_move = stockfish.get_best_move()
        #best_move="d6d8"
        #ROBOT best_move
        print(best_move)
        stockfish.make_moves_from_current_position([best_move])

        print(stockfish.get_board_visual())

        final_player = stockfish.get_evaluation()

        print("final player: ", final_player)
    return stockfish.get_fen_position()

def Player_moves(board,move): 

    stockfish.set_elo_rating(2000)
    stockfish.set_fen_position(board.fen())

    initial_player = stockfish.get_evaluation()
    best_move = stockfish.get_best_move()
    
    stockfish.make_moves_from_current_position([move])
    
    initial_turk = stockfish.get_evaluation()
    
    points = abs(initial_turk['value'] - initial_player['value'])

    if points >= GRAVE_ERROR:
            player_move_alg = alg_to_alg(move, board)
            best_move_alg = alg_to_alg(best_move, board)
            text = request.chess_question(board.fen(), player_move_alg, best_move_alg)
            speech.text_to_speech(text)
    else : 
        print ("Good Move")
    turk_move = stockfish.get_best_move()
    robot_move = separateMove(turk_move)
    robotCoords = toRobotIndices(robot_move)
    print("DANI: ", robotCoords)
    #serial_com_python.movement(str(robotCoords))

    return turk_move



scara = serial_com_python.SerialCom()
scara.startSerial()
scara.writeSerial("7007")
scara.endSerial()