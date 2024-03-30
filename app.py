import random
def reset_board():
    board = {}
    for i in range(9):
        board[i] = " "
    return board

winning_condition = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

def check_condition(player, board):
    condition = {"message": "", "status": ""} 
    # Loop all conditions to check
    for conditions in winning_condition:
        counter = 0
        for pos in conditions:
            if pos in board:
                if board[pos] == player:
                    counter += 1
        if counter == 3:
            condition["message"] = f'Player {player} has won!'
            condition["status"] = player
            return condition 
    all_taken = len([key for key, value in board.items() if value == " "]) == 0
    if all_taken:
        condition["message"] = f'Game over, Draw!'
        condition["status"] = "DRAW"
        return condition
    return condition

def AI_decision_turn(winning_condition, board, player_turn, game_history):
    MIX_POS = 5
    ONE_ENEMY_POS = 1
    TWO_ENEMY_POS = 30
    ONE_PLAYER_POS = 2
    TWO_PLAYER_POS = 100
    
    pos_taken = {key: True for key, value in board.items() if value != " "}

    all_pos = {key: 0 for key in board}
    for conditions in winning_condition:
        player_counter = 0
        enemy_counter = 0
        # Check existing player and enemy on win conditions
        for pos in conditions:
            if pos in pos_taken:
                all_pos[pos] = -100
                if board[pos] == player_turn:
                    player_counter += 1
                else:
                    enemy_counter += 1
        # Add rewards to every position for AI decision
        for pos in conditions:
            if pos not in pos_taken:
                # No need to defend against 1 enemy pos, so lesser attention
                if enemy_counter == 1 and player_counter == 1:
                    all_pos[pos] -= MIX_POS
                elif enemy_counter == 1:
                    all_pos[pos] += ONE_ENEMY_POS
                # Prioritise in defending winning enemy
                elif enemy_counter == 2:
                    all_pos[pos] += TWO_ENEMY_POS
                # Let AI have higher priority to put 2 in a line
                if player_counter == 1:
                    all_pos[pos] += ONE_PLAYER_POS
                # Highest priority for AI to win
                elif player_counter == 2:
                    all_pos[pos] += TWO_PLAYER_POS
    # Shuffle all keys for equal move reward for unpredictable AI moves
    all_pos_keys = list(all_pos.keys())
    random.shuffle(all_pos_keys)
    shuffled_pos = {key: all_pos[key] for key in all_pos_keys}
    # Sort reward move list and let AI choose the highest reward move
    sorted_pos = [pos for pos, value in sorted(shuffled_pos.items(), key=lambda item: item[1], reverse=True)]
    #print(f'AllPos: {all_pos}, Sorted: {sorted_pos}')
    # Change board to AI
    board[sorted_pos[0]] = player_turn
    game_history.append({"player": player_turn, "pos": sorted_pos[0]})

def rdr(player, index):
    return player if player != " " else index

def render_board(board):
    print(f' {rdr(board[0], 0)} | {rdr(board[1], 1)} | {rdr(board[2], 2)} ')
    print(f'   |   |   ')
    print(f'-----------')
    print(f' {rdr(board[3], 3)} | {rdr(board[4], 4)} | {rdr(board[5], 5)} ')
    print(f'   |   |   ')
    print(f'-----------')
    print(f' {rdr(board[6], 6)} | {rdr(board[7], 7)} | {rdr(board[8], 8)} ')
    print(f'   |   |   ')

def user_turn(player, board):
    print(f'Please input your position (0-8) for Player {player}:')
    player_pos = int(input())
    if player_pos < 0 or player_pos > 8:
        return False
    board[player_pos] = player
    return True
def player_vs_AI():
    game_completed = False
    player_turn = "X"
    board = reset_board()
    game_history = []

    while not game_completed:
        render_board(board)
        if player_turn == "X":
           user_turn(player_turn, board)
        else:
           AI_decision_turn(winning_condition, board, player_turn, game_history)
           print("AI has made a move")
        print("-------------------------------------------------------------------------------------------")
        game_status = check_condition(player_turn, board)
        if game_status["message"] != "":
            print(game_status["message"])
            game_completed = True
            break
        else:
            if player_turn == "X":
                player_turn = "O"
            else:
                player_turn = "X"
    render_board(board)
    return {"board": board, "game_status": game_status}

def AI_vs_AI():
    game_completed = False
    player_turn = "X"
    board = reset_board()
    game_history = []

    while not game_completed:
        AI_decision_turn(winning_condition, board, player_turn, game_history)
        game_status = check_condition(player_turn, board)
        if game_status["message"] != "":
            print(game_status["message"])
            game_completed = True
            break
        else:
            if player_turn == "X":
                player_turn = "O"
            else:
                player_turn = "X"
    print(f"game_history: {game_history}")
    render_board(board)
    return {"board": board, "game_status": game_status}

def AI_games():
    games_board = []
    print("Specify number of AI games:")
    game_count = int(input())

    for i in range(game_count):
        games_board.append(AI_vs_AI())

    # Show statistics for the number of AI games
    X_win = 0
    O_win = 0
    draw_counter = 0
    for i in range(game_count):
        if games_board[i]["game_status"]["status"] == "X":
            X_win += 1
        elif games_board[i]["game_status"]["status"] == "O":
            O_win += 1
        else:
            draw_counter += 1
    print(f'{game_count} Games Played, Status: X Win: {X_win}, O Wins: {O_win}, Draw: {draw_counter}')

print("Specify which mode to play\n(1) player vs AI \n(2) AI vs AI:")
mode = input()
if mode == "1":
    player_vs_AI()
elif mode == "2":
    AI_games()
else:
    print("Invalid mode")
