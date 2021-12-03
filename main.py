# -------- Global and configuration variables --------- #

# Default players score
score_player_x = 0
score_player_o = 0

# Game statistics
n_of_wins_player_x = 0
n_of_wins_player_o = 0
n_of_round = 0

# Configurations
n_of_round_limit = 10
point_limit = 50
payout_length_3 = 2
payout_length_4 = 10
payout_length_5 = 50
dimension = None


# Game variables
game_still_going = True
board = []
position_board = []
actual_player = "X"
diagonals_1 = []  # lower-left-to-upper-right diagonals
diagonals_2 = []  # upper-left-to-lower-right diagonals
input_pos_x = None  # reserved to hold the selected position of each shift
input_pos_y = None  # reserved to hold the selected position of each shift


# -------------- initialization functions --------------- #

# Create the game matrix that will be printed
def create_game_matrix():
    global dimension, board
    board = []
    for i in range(dimension):  # A for loop for row entries
        a = []
        for j in range(dimension):  # A for loop for column entries
            a.append("-")
        board.append(a)


# Create a matrix of position used to discover diagonals
def create_position_matrix():
    global dimension, position_board
    for i in range(dimension):  # A for loop for row entries
        a = []
        for j in range(dimension):  # A for loop for column entries
            a.append(str(i) + "," + str(j))
        position_board.append(a)


# Print the game matrix on the screen
def print_game_matrix():
    global dimension, board
    print()
    for i in range(dimension):
        for j in range(dimension):
            print("|", board[i][j], end=" | ")
        print()


# Fill diagonals_1 and diagonals_2 vector
def find_diagonals():
    global diagonals_1, diagonals_2, position_board

    n = len(position_board)
    for p in range(2 * n - 1):
        diagonals_1.append([position_board[p - q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
        diagonals_2.append([position_board[n - p + q - 1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])


# -------------- Game management functions -------------- #
def print_player_score():
    global score_player_x, score_player_o, actual_player
    print()
    print("Punteggio del giocatore X: " + str(score_player_x))
    print("Punteggio del giocatore Y: " + str(score_player_o))


def handle_turn():
    global input_pos_x, input_pos_y

    print()
    print("E' il turno del giocatore " + actual_player)

    input_pos_x = input("Sciegli una posizione sull'asse X da 1 a " + str(dimension) + ": ")
    input_pos_x = int(input_pos_x) - 1

    input_pos_y = input("Sciegli una posizione sull'asse Y da 1 a " + str(dimension) + ": ")
    input_pos_y = int(input_pos_y) - 1

    if dimension is not None:

        if 0 <= input_pos_x <= dimension - 1 and 0 <= input_pos_y <= dimension - 1:
            if board[input_pos_x][input_pos_y] == "-":
                board[input_pos_x][input_pos_y] = actual_player
            else:
                print("Posizione occupata da " + board[input_pos_x][input_pos_y] + ", hai perso il turno!")
                input_pos_x = input_pos_y = None
        else:
            print("E' stata inserita una posizione insesistente! hai perso il turno!")
    else:
        print("Errore: dimensione nulla.")


def flip_player_to_O():
    global actual_player
    actual_player = "O"


def flip_player_to_X():
    global actual_player
    actual_player = "X"


def handle_round():
    global score_player_x, score_player_o, n_of_wins_player_x, n_of_wins_player_o, \
        n_of_round, actual_player, input_pos_x, input_pos_y, n_of_round_limit, game_still_going

    if score_player_x >= 50 or score_player_o >= 50:
        print("\n------------------------------------------------------------ \nROUND TERMINATO")
        if score_player_x > score_player_o:
            n_of_wins_player_x += 1
            print("Ha vinto il giocatore X!")
        elif score_player_o > score_player_x:
            n_of_wins_player_o += 1
            print("Ha vinto il giocatore O!")
        # else Parity

        # Printing statistics
        print("------------------------------------------------------------")
        print_game_matrix()
        print("\n------------------------------------------------------------")
        print("Round numero: ", n_of_round)
        print("Vittorie di X: ", n_of_wins_player_x)
        print("Vittorie di O: ", n_of_wins_player_o)
        print("------------------------------------------------------------ \n")
        print("NUOVO ROUND: ", n_of_round+1)
        # Reset var for new round
        n_of_round += 1
        score_player_x = score_player_o = 0
        input_pos_x = input_pos_y = None
        create_game_matrix()

        # Checking if n_of_round > n_of_round_limit (configurable)
        if n_of_round >= n_of_round_limit:
            game_still_going = False
            print("GIOCO TERMINATO")
            exit()


def input_board_dimension():
    global dimension
    flag = True

    while flag:
        dimension = int(input("Inserisci la dimensione della matrice: "))
        if dimension >= 3:
            flag = False
        else:
            print("Inserisci una dimensione >= 3")


def score_assignment(counter):
    global score_player_x, score_player_o
    if counter >= 3:
        if counter == 3:
            if actual_player == "X":
                score_player_x = score_player_x + payout_length_3
            else:
                score_player_o = score_player_o + payout_length_3
        elif counter == 4:
            if actual_player == "X":
                score_player_x = score_player_x + payout_length_4
            else:
                score_player_o = score_player_o + payout_length_4
        elif counter == 5:
            if actual_player == "X":
                score_player_x = score_player_x + payout_length_5
            else:
                score_player_o = score_player_o + payout_length_5


# -------------- Score management functions -------------- #

def checking_row():
    global board, actual_player, score_player_x, score_player_o, input_pos_x, input_pos_y
    row_num = input_pos_x
    len_row = dimension
    counter = 0
    new_series = False

    if row_num is not None:
        if 0 <= row_num < len_row:

            for j in range(len_row):
                # Found the series
                if board[row_num][j] == actual_player:
                    counter += 1
                    # Is a new series?
                    if row_num == input_pos_x and j == input_pos_y:
                        new_series = True
                # Interrupted series or row
                if j == (len_row - 1) or board[row_num][j] != actual_player:
                    if counter >= 3 and new_series is True:
                        score_assignment(counter)
                    counter = 0
                    new_series = False


def checking_column():
    global board, actual_player, score_player_x, score_player_o, input_pos_x, input_pos_y
    column_num = input_pos_y
    len_column = dimension
    counter = 0
    new_series = False

    if column_num is not None:
        if 0 <= column_num < len_column:

            for i in range(len_column):
                # Found the series
                if board[i][column_num] == actual_player:
                    counter += 1
                    # Is a new series?
                    if column_num == input_pos_y and i == input_pos_x:
                        new_series = True
                # Interrupted series or column
                if i == (len_column - 1) or board[i][column_num] != actual_player:
                    if counter >= 3 and new_series is True:
                        score_assignment(counter)
                    counter = 0
                    new_series = False


def checking_diagonal():
    global board, actual_player, score_player_x, score_player_o, input_pos_x, input_pos_y, diagonals_1, diagonals_2
    finded_diagonal_1 = []
    finded_diagonal_2 = []
    counter = 0
    new_series = False

    # First diagonal
    for i in range(len(diagonals_1)):
        for j in range(len(diagonals_1[i])):
            temp = diagonals_1[i][j]
            pos_x = int(temp[0])
            pos_y = int(temp[2])
            if pos_x == input_pos_x and pos_y == input_pos_y:
                finded_diagonal_1 = diagonals_1[i]
                break

    for i in range(len(finded_diagonal_1)):
        temp = finded_diagonal_1[i]
        pos_x = int(temp[0])
        pos_y = int(temp[2])
        # Found the series
        if board[pos_x][pos_y] == actual_player:
            counter += 1
            # Is a new series?
            if pos_x == input_pos_x and pos_y == input_pos_y:
                new_series = True
        # Interrupted series or diagonal
        if i == len(finded_diagonal_1) - 1 or board[pos_x][pos_y] != actual_player:
            if counter >= 3 and new_series is True:
                score_assignment(counter)
            counter = 0
            new_series = False

    # Second diagonal
    for i in range(len(diagonals_2)):
        for j in range(len(diagonals_2[i])):
            temp = diagonals_2[i][j]
            pos_x = int(temp[0])
            pos_y = int(temp[2])
            if pos_x == input_pos_x and pos_y == input_pos_y:
                finded_diagonal_2 = diagonals_2[i]

    for i in range(len(finded_diagonal_2)):
        temp = finded_diagonal_2[i]
        pos_x = int(temp[0])
        pos_y = int(temp[2])
        # Found the series
        if board[pos_x][pos_y] == actual_player:
            counter += 1
            # Is a new series?
            if pos_x == input_pos_x and pos_y == input_pos_y:
                new_series = True
        # Interrupted series or diagonal
        if i == len(finded_diagonal_2) - 1 or board[pos_x][pos_y] != actual_player:
            if counter >= 3 and new_series is True:
                score_assignment(counter)
            counter = 0
            new_series = False


# ------------------- Main function ---------------------- #

def play_game():
    input_board_dimension()
    create_game_matrix()
    create_position_matrix()
    find_diagonals()
    print_game_matrix()
    print_player_score()

    while game_still_going:
        flip_player_to_X()
        handle_turn()
        checking_row()
        checking_column()
        checking_diagonal()
        handle_round()
        print_game_matrix()
        print_player_score()

        print("------------------------------------------------------------")

        flip_player_to_O()
        handle_turn()
        checking_row()
        checking_column()
        checking_diagonal()
        handle_round()
        print_game_matrix()
        print_player_score()

        print("------------------------------------------------------------")


# -------------------------------------------------------- #


play_game()
