import random
import datetime
import traceback


def drawGameboard(board):
    # This function prints out the board that it was passed
    transformed = [item for sublist in board for item in sublist]
    print("-------------")
    for i in range(3):
        print("|", transformed[0 + i * 3], "|", transformed[1 + i * 3], "|", transformed[2 + i * 3], "|")
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


def winIndices(boardLength):
    # Generates set of all the possible index combinations to check for the win
    # Raws
    for r in range(boardLength):
        yield [(r, c) for c in range(boardLength)]
    # Columns
    for c in range(boardLength):
        yield [(r, c) for r in range(boardLength)]
    # Diagonal top left to bottom right
    yield [(i, i) for i in range(boardLength)]
    # Diagonal top right to bottom left
    yield [(i, boardLength - 1 - i) for i in range(boardLength)]


def winnerCheck(board, letter):
    # Given a board and a player’s letter, this function returns True if that player has won
    boardLength = len(board)
    for indexes in winIndices(boardLength):
        if all(board[firstIndex][secondIndex] == letter for firstIndex, secondIndex in indexes):
            return True
    return False


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False
    return input('Do you want to play again? (yes or no)\n').lower().startswith('y')


def playerChoice(board):
    # Let the player type in their move
    transformedBoard = [item for sublist in board for item in sublist]
    while True:
        try:
            position = int(input('Choose number input 1-9\n'))
            if position in range(1, 10) and type(transformedBoard[position - 1]) != str:
                return position
            elif type(transformedBoard[position - 1]) == str:
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
    return all(type(item) != int for sublist in board for item in sublist)


def gamePlay():
    board = [list(range(1,4)), list(range(4,7)), list(range(7,10))]
    players = inputPlayerLetter()
    name, playerMarker = chooseFirstPlayer(players)
    print('{} with marker {} will go first.'.format(name, playerMarker))
    drawGameboard(board)
    while True:
        position = playerChoice(board)
        board = [[playerMarker if element == position else element for element in item] for item in board]
        drawGameboard(board)
        if winnerCheck(board, playerMarker):
            print('Congratulations {}! You won the game!\n'.format(name))
            break
        else:
            if fullBoardCheck(board):
                print('The game is a tie!')
                break

        name = 'Player 1' if name == 'Player 2' else 'Player 2'
        for player in players:
            if name in player:
                playerMarker = player.replace(name, '').replace(': ', '')
        print(name, playerMarker)


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
