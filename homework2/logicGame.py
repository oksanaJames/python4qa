import random
import datetime
import traceback


def drawGameboard(board):
    # This function prints out the board that it was passed
    print("-------------")
    for i in range(3):
        print("|", board[0 + i * 3], "|", board[1 + i * 3], "|", board[2 + i * 3], "|")
    print("-------------")


def inputPlayerLetter():
    # Lets the player type which letter they want to be
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        letter = input('Player 1, Choose O or X to play!\n').upper()
    if letter == 'X':
        return ["Player 1: X", "Player 2: O"]
    else:
        return ["Player 2: X", "Player 1: O"]


def winnerCheck(board, letter):
    # Given a board and a player’s letter, this function returns True if that player has won
    return ((board[6] == letter and board[7] == letter and board[8] == letter) or  # across the bottom
            (board[3] == letter and board[4] == letter and board[5] == letter) or  # across the middle
            (board[0] == letter and board[1] == letter and board[2] == letter) or  # across the top
            (board[6] == letter and board[3] == letter and board[0] == letter) or  # down the left side
            (board[7] == letter and board[4] == letter and board[1] == letter) or  # down the middle
            (board[8] == letter and board[5] == letter and board[2] == letter) or  # down the right side
            (board[6] == letter and board[4] == letter and board[2] == letter) or  # diagonal
            (board[8] == letter and board[4] == letter and board[0] == letter))  # diagonal


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False
    return input('Do you want to play again? (yes or no)\n').lower().startswith('y')


def playerChoice(board):
    # Let the player type in their move
    while True:
        try:
            position = int(input('Choose number input 1-9\n'))
            if position in range(1, 10) and type(board[position - 1]) != str:
                return position
            else:
                print("Field isn't empty!")
        except ValueError:
            pass


def chooseFirstPlayer(players):
    # Randomly choose the player who goes first
    playerLetter = ''
    random_player = 'Player {}'.format(random.randint(1, 2))
    for player in players:
        if random_player in player:
            playerLetter = player.replace(random_player, '').replace(': ', '')
    return random_player, playerLetter


def fullBoardCheck(board):
    # Return True if every space on the board has been taken, otherwise return False
    return all(type(b) != int for b in board)


def gamePlay():
    board = list(range(1, 10))
    players = inputPlayerLetter()
    name, player_marker = chooseFirstPlayer(players)
    print('{} with marker {} will go first.'.format(name, player_marker))
    drawGameboard(board)
    while True:
        position = playerChoice(board)
        board[position - 1] = player_marker
        drawGameboard(board)
        if winnerCheck(board, player_marker):
            print('Congratulations {}! You won the game!\n'.format(name))
            break
        else:
            if fullBoardCheck(board):
                print('The game is a tie!')
                break

        name = 'Player 1' if name == 'Player 2' else 'Player 2'
        for player in players:
            if name in player:
                player_marker = player.replace(name, '').replace(': ', '')
        print(name, player_marker)


if __name__ == '__main__':
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        start = datetime.datetime.now()
        print('Welcome to Tic Tac Toe Game!\n')
        while True:
            gamePlay()
            if not playAgain():
                break
    except Exception as e:
        print("\nError")
        print(e)
        traceback.print_exc()
    finally:
        duration = str(datetime.datetime.now() - start)  # print the time taken for script execution
        print('\n')
        print('game complete in duration: %s' % duration)
        print('-----end-----')
