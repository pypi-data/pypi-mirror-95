#!/usr/bin/env python3

""" Play the Chess in the terminal """

import pickle
import sys
import os
import copy
import time

try:
    from . import moves
except ImportError:
    import moves

VERSION = '0.0.10'

class Ansi:
    """ The terminal ansi chars """

    GREEN = '\033[32m'
    RED = '\033[31m'
    RESET = '\033[0m'
    GRAY = '\033[37m'
    CYAN = '\033[96m'

    @staticmethod
    def disable():
        """ Disables the ansi chars """
        Ansi.GREEN = ''
        Ansi.RED = ''
        Ansi.RESET = ''
        Ansi.GRAY = ''
        Ansi.CYAN = ''

class Piece:
    """ Each piece in the chess board """

    PAWN = 'pawn'
    KING = 'king'
    QUEEN = 'queen'
    KNIGHT = 'knight'
    BISHOP = 'bishop'
    ROCK = 'rock'

    ICONS = {
        'pawn': 'pawn',
        'king': 'king',
        'queen': 'queen',
        'knight': 'knight',
        'bishop': 'bishop',
        'rock': 'rock',
    }

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def __str__(self):
        return ('w' if self.color == 'white' else 'b') + '-' + self.ICONS[self.name]

    def allowed_moves(self, game, src, dst, return_locations=False):
        """ Returns the allowed targets for move for this piece

        Returned structure:
        [
            [x, y],
            [x, y],
            ...
        ]
        """
        x = src[0]
        y = src[1]
        result = []
        if self.name == Piece.PAWN:
            result = moves.pawn_move(self, game, src)
        elif self.name == Piece.ROCK:
            result = moves.rock_move(self, game, src)
        elif self.name == Piece.QUEEN:
            result = [*moves.rock_move(self, game, src)]
        elif self.name == Piece.KING:
            result = moves.king_move(self, game, src)
        elif self.name == Piece.KNIGHT:
            result = moves.knight_move(self, game, src)
        else:
            result = []
        if return_locations:
            return result
        if dst in result:
            return True
        if self.name == Piece.PAWN:
            return False
        return False

class Game:
    """ The running game handler """

    ROW_SEPARATOR = ('|-----------'*8) + '|\n'
    CELL_WIDTH = 10

    def __init__(self):
        self.turn = 'white'
        self.logs = []

        # this item is used to validate saved games versions
        # if we load a file that created with old version of the game,
        # we can check it using this property
        # if we made backward IN-compatible changes on this class,
        # this number should be bumped.
        self.version = 1

        # each cell location be in this list, will be highlighted in rendering
        self.highlight_cells = []

        # this item determines the selected piece using `s` command
        self.selected_cell = None

        # the player names
        self.white_player = 'White'
        self.black_player = 'Black'

        # initialize the board
        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
                # handle default pieces location
                if i in (1, 6):
                    self.board[-1].append(
                        Piece(
                            name=Piece.PAWN,
                            color=('white' if i == 1 else 'black'),
                        )
                    )
                elif i in (0, 7):
                    name = Piece.PAWN
                    if j in (0, 7):
                        name = Piece.ROCK
                    elif j in (0, 3):
                        name = Piece.KING
                    elif j in (3 ,7):
                        name = Piece.QUEEN
                    elif j in (0, 4):
                        name = Piece.QUEEN
                    elif j in (4, 7):
                        name = Piece.KING
                    elif j in (2, 5):
                        name = Piece.BISHOP
                    elif j in (1, 6):
                        name = Piece.KNIGHT
                    self.board[-1].append(
                        Piece(
                            name=name,
                            color=('white' if i == 0 else 'black'),
                        )
                    )
                else:
                    self.board[-1].append(None)

    def change_turn(self):
        """ Changes the turn.

        If currently is white turn, set turn to black and reverse
        """
        self.turn = 'black' if self.turn == 'white' else 'white'

    def move(self, src, dst):
        """ Moves src to dst """
        dst_p = copy.deepcopy(self.board[dst[0]][dst[1]])
        src_p = copy.deepcopy(self.board[src[0]][src[1]])

        if not src_p.allowed_moves(self, src, dst):
            return False, 'Error: Target location is not allowed. enter `s '+str(src[0]+1)+'.'+str(src[1]+1)+'` to see where you can go'

        if dst_p is not None:
            if dst_p.color == self.turn:
                # killing self!
                return False, 'Error: You cannot kill your self!'

        self.board[src[0]][src[1]] = None

        self.board[dst[0]][dst[1]] = src_p

        return True, ''

    def run_command(self, cmd: str) -> str:
        """ Gets a command as string and runs that on the game. Returns result message as string """
        cmd_parts = cmd.split()

        self.highlight_cells = []
        self.selected_cell = None

        invalid_msg = 'Invalid Command!'

        result_msg = 'Runed'

        if len(cmd_parts) == 1:
            if cmd_parts[0] == 'back':
                if not self.logs:
                    invalid_msg = 'Please move something first!'
                else:
                    # back
                    new_game = Game()
                    while self.logs:
                        if not self.logs[-1].startswith('m'):
                            self.logs.pop()
                        else:
                            self.logs.pop()
                            break
                    for cmd in self.logs:
                        new_game.run_command(cmd)
                    self.logs = new_game.logs
                    self.board = new_game.board
                    self.turn = new_game.turn
                    return 'OK! now you are one step back!'
        elif len(cmd_parts) == 2:
            # s <location>
            if cmd_parts[0] == 's':
                location = cmd_parts[1].replace('.', '-').split('-')
                if len(location) == 2:
                    try:
                        location[0] = int(location[0])-1
                        location[1] = int(location[1])-1

                        valid_range = list(range(0, 8))
                        if not (location[0] in valid_range and location[1] in valid_range):
                            return 'Error: Location is out of range!'

                        if self.board[location[0]][location[1]] is None:
                            return 'Error: selected cell is empty!'

                        allowed_moves = self.board[location[0]][location[1]].allowed_moves(self, (location[0], location[1]), (location[0], location[1]), return_locations=True)

                        # show allowed moves
                        self.highlight_cells = allowed_moves
                        self.selected_cell = location

                        return '' if self.highlight_cells else 'This piece cannot move!'
                    except:
                        return 'Error: Invalid location!'

        if len(cmd_parts) == 3:
            if cmd_parts[0] in ('move', 'mv'):
                cmd_parts.insert(2, 'to')

        if len(cmd_parts) == 4:
            # the move operation
            if cmd_parts[0] in ('move', 'mv') and cmd_parts[2] == 'to':
                src = cmd_parts[1].replace('.', '-').split('-')
                dst = cmd_parts[3].replace('.', '-').split('-')
                if len(src) == 2 and len(dst) == 2:
                    try:
                        src[0] = int(src[0])-1
                        src[1] = int(src[1])-1
                        dst[0] = int(dst[0])-1
                        dst[1] = int(dst[1])-1

                        valid_range = list(range(0, 8))
                        if not (src[0] in valid_range and src[1] in valid_range and dst[0] in valid_range and dst[1] in valid_range):
                            return 'Error: Locations are out of range!'
                    except:
                        return 'Error: Invalid locations!'
                    result_msg = cmd_parts[1] + ' Moved to ' + cmd_parts[3]
                else:
                    return invalid_msg

                if self.board[src[0]][src[1]] is not None:
                    pass
                else:
                    return 'Error: source location is empty cell!'
                if src == dst:
                    return 'Error: source and target locations are not different!'
                if self.board[src[0]][src[1]].color != self.turn:
                    return 'Error: its ' + self.turn + ' turn, you should move ' + self.turn + ' pieces!'
                result = self.move(src, dst)
                if not result[0]:
                    return result[1]
            else:
                return invalid_msg
        else:
            return invalid_msg

        # add command to the log
        self.logs.append(cmd)

        # change the turn
        self.change_turn()

        return result_msg

    def get_dead_items(self):
        """ Returns list of dead items like this:
        {
            "black": {
                "pawn": 3, # count
                "rock": 1
            },
            "white": {
                # ...
            }
        }
        """
        result = {
            "white": {},
            "black": {},
        }
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] is not None:
                    try:
                        result[self.board[i][j].color][self.board[i][j].name] += 1
                    except:
                        result[self.board[i][j].color][self.board[i][j].name] = 1

        # now, `result` contains live items.
        # we want dead items
        for team in result:
            for item in result[team]:
                if item == Piece.PAWN:
                    result[team][item] = 8 - result[team][item]
                elif item not in (Piece.QUEEN, Piece.KING):
                    result[team][item] = 2 - result[team][item]
                else:
                    result[team][item] = 1 - result[team][item]

        # delete items contains 0
        new_result = {
            "white": {},
            "black": {},
        }
        for team in result:
            for item in result[team]:
                if result[team][item] > 0:
                    new_result[team][item] = result[team][item]

        return new_result

    def render(self) -> str:
        """ Renders the board to show in the terminal """
        output = ''

        # render the player names
        white_player = 'B. ' + self.white_player
        black_player = 'W. ' + self.black_player
        white_space_len = (len(self.ROW_SEPARATOR) - (len(white_player)+len(black_player))) - 2
        white_space_len = int(white_space_len/2)
        player_names = Ansi.CYAN + white_player + Ansi.RESET + (' ' * white_space_len) + 'Vs' + (' ' * white_space_len) + Ansi.RED + black_player + Ansi.RESET

        output += player_names + '\n'
        output += ('_' * len(self.ROW_SEPARATOR)) + '\n'
        output += (' ' * len(self.ROW_SEPARATOR)) + '\n'

        for i in range(1, 9):
            output += (int(self.CELL_WIDTH/2) * ' ') + str(i) + (' ' * (int(self.CELL_WIDTH/2)+1))
        output += '\n'
        i = 0
        for row in self.board:
            output += '  ' + self.ROW_SEPARATOR + str(i+1) + ' '
            j = 0
            for column in row:
                if column is None:
                    column_str = ' ' + str(i+1) + '-' + str(j+1)
                    ansi_color = Ansi.GRAY
                    ansi_reset = Ansi.RESET
                else:
                    column_str = str(column)
                    ansi_color = Ansi.CYAN if column.color == 'white' else Ansi.RED
                    ansi_reset = Ansi.RESET
                if [i, j] in self.highlight_cells or self.selected_cell == [i, j]:
                    column_str = '*' + column_str.lstrip() + '*'
                output += '| ' + ansi_color + column_str + ansi_reset + (' ' * (self.CELL_WIDTH-len(column_str)))
                j += 1
            output += '|\n'
            i += 1
        output += '  ' + self.ROW_SEPARATOR
        lines = output.splitlines()
        output = ''
        for line in lines:
            output += ' ' + line + '\n'

        # show dead items
        dead_items = self.get_dead_items()
        dead_items_str = 'Deads:\n'
        for team in dead_items:
            if dead_items[team]:
                color = (Ansi.CYAN if team == 'white' else Ansi.RED)
                current_line = color + team + Ansi.RESET + ': '
                for item in dead_items[team]:
                    if item in (Piece.QUEEN, Piece.KING):
                        current_line += color + item + Ansi.RESET + ', '
                    else:
                        current_line += color + str(dead_items[team][item]) + ' ' + item + Ansi.RESET + ', '
                current_line = current_line.strip().strip(',')
                current_line += (' ' * (len(self.ROW_SEPARATOR) - len(current_line)))
                dead_items_str += current_line + '\n'

        if dead_items_str == 'Deads:\n':
            dead_items_str = ''

        output += dead_items_str.strip()

        return output

def show_help():
    """ Prints the help message """
    print('''tchess - Play the chess in terminal

SYNOPSIS
    $ '''+sys.argv[0]+''' [options...] [?game-file-name]

DESCRIPTION
    The TChess is a chess game in terminal.
    This software can handle saving the game in a file
    Then you can continue your game later by loading that file

OPTIONS
    --help: shows this help
    --version|-v: shows the version of tchess
    --no-ansi: disable terminal ansi colors
    --replay: play the saved game
    --replay-speed: delay between play frame (for example `3`(secound) or `0.5`)
    --dont-check-terminal: do not check terminal size
    --player-white=[name]: set name of white player
    --player-black=[name]: set name of black player

AUTHOR
    This software is created by Parsa Shahmaleki <parsampsh@gmail.com>
    And Licensed under MIT
''')

def load_game_from_file(path: str):
    """ Loads the game object from a file """
    tmp_f = open(path, 'rb')
    file_game = pickle.load(tmp_f)
    tmp_f.close()
    game = Game()
    game.turn = str(file_game.turn)
    game.logs = list(file_game.logs)
    game.version = int(file_game.version)
    game.highlight_cells = list(file_game.highlight_cells)
    game.white_player = str(file_game.white_player)
    game.black_player = str(file_game.black_player)
    game.board = list(file_game.board)
    return game

def run(args=[]):
    """ The main cli entry point """

    game_file_name = 'game.tchess'

    # parse the arguments
    options = [arg for arg in args if arg.startswith('-')]
    arguments = [arg for arg in args if not arg.startswith('-')]

    # check `--version` option
    if '--version' in options or '-v' in options:
        print(VERSION)
        sys.exit()

    # check the `--help` option
    if '--help' in options:
        options.remove('--help')
        show_help()
        sys.exit()

    # handle `--no-ansi` option
    if '--no-ansi' in options:
        options.remove('--no-ansi')
        Ansi.disable()

    # handle `--replay` option
    is_play = False
    log_counter = 0
    if '--replay' in options:
        options.remove('--replay')
        is_play = True

    # handle `--replay-speed` option
    play_speed = 1
    for option in options:
        if option.startswith('--replay-speed='):
            options.remove(option)
            value = option.split('=', 1)[-1]
            try:
                play_speed = float(value)
            except:
                pass
            break

    # check the terminal size
    if not '--dont-check-terminal' in options:
        try:
            terminal_width = os.get_terminal_size().columns
        except:
            terminal_width = len(Game.ROW_SEPARATOR)+3
        if terminal_width < len(Game.ROW_SEPARATOR)+3:
            print(
                'ERROR: your terminal width is less than ' + str(len(Game.ROW_SEPARATOR)+3) + '. use --dont-check-terminal to ignore it.',
                file=sys.stderr
            )
            sys.exit(1)

    if len(arguments) > 0:
        game_file_name = arguments[0]

    if os.path.isfile(game_file_name):
        # if file exists, load the game from that
        # (means user wants to open a saved game)
        try:
            game = load_game_from_file(game_file_name)

            # validate the game object
            if not isinstance(game, Game):
                raise

            # check the version
            if game.version != Game().version:
                print('ERROR: file `' + game_file_name + '` is created with OLD/NEW version of tchess and cannot be loaded', file=sys.stderr)
                raise
        except:
            # file is corrupt
            print('ERROR: file `' + game_file_name + '` is corrupt', file=sys.stderr)
            sys.exit(1)
    else:
        game = Game()

    game_logs = game.logs
    if is_play:
        game = Game()

    # set player names
    for option in options:
        if option.startswith('--player-white='):
            game.white_player = option.split('=', 1)[-1]
        elif option.startswith('--player-black='):
            game.black_player = option.split('=', 1)[-1]

    # last result of runed command
    last_message = ''

    while True:
        # render the game board on the terminal
        print('\033[H', end='')
        title = ' Welcome to the TChess! '
        stars_len = len(Game.ROW_SEPARATOR) - len(title)
        title = (int(stars_len/2) * '*') + title + (int(stars_len/2) * '*')
        print(title, end='')
        print(' ' * (len(Game.ROW_SEPARATOR) - len(title)))
        print(' ' * len(Game.ROW_SEPARATOR))
        print(game.render())

        # get command from user and run it
        tmp_turn = game.turn
        ansi_color = Ansi.RED if tmp_turn == 'black' else Ansi.CYAN
        # fix whitespace
        print(last_message, end='')
        print(' ' * (len(Game.ROW_SEPARATOR)-len(last_message)))
        print(' ' * len(Game.ROW_SEPARATOR), end='\r')
        if is_play:
            time.sleep(play_speed)
            try:
                command = game_logs[log_counter]
            except:
                print('Finished.')
                sys.exit()
            log_counter += 1
        else:
            command = input(ansi_color + game.turn + Ansi.RESET + ' Turn >>> ').strip().lower()

        game.highlight_cells = []
        game.selected_cell = None

        # check the empty command
        if command == '':
            last_message = ''
            continue

        # check the exit command
        if command in ['exit', 'quit', 'q']:
            game_file_name = os.path.abspath(game_file_name)
            print('Your game was saved in file `' + game_file_name + '`.')
            print(
                'To continue this game again, run `' + sys.argv[0] + ' '+repr(game_file_name)+'`.'
            )
            print('Good bye!')
            sys.exit()

        # run the command on the game to make effects
        last_message = game.run_command(command)

        # save the game
        # open a file
        # this file is used to save the game state
        # after any command on the game, game will be re-write on this file
        game_file = open(game_file_name, 'wb')
        pickle.dump(game, game_file)
        game_file.close()

if __name__ == '__main__':
    run(sys.argv[1:])
