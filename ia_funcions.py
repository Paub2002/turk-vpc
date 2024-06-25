from stockfish import Stockfish
import chess
import request
import speech

LEVE_ERROR = 20
ERROR = 50
GRAVE_ERROR = 150

stockfish = Stockfish(path="turk-vpc\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe", depth=7)



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
            text = request.chess_question(fen_string, player_move_alg, best_move_alg)
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
            text = request.chess_question(fen_string, player_move_alg, best_move_alg)
            speech.text_to_speech(text)
    else : 
        print ("Good Move")
    return stockfish.get_best_move()

#fen_string = "r1bqkb1r/pp1ppppp/2n2n2/2p5/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 0 4"
# fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# main_loop("f6d5",fen_string,1)






    

