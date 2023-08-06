""" Serves a game and waits for guest to play online """

import uuid
import logging
from flask import Flask, request, Response

CURRENT_SESSION = None

def serve(game, host='0.0.0.0', port=8799):
    """ Serve the server """
    app = Flask(__name__)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/connect')
    def connect():
        global CURRENT_SESSION

        # check session already started
        if CURRENT_SESSION is not None:
            return Response('session currently started', status=401)

        # get user confirmation
        try:
            guest_name = request.args['name']
            if game.guest_color == 'white':
                game.white_player = guest_name
            else:
                game.black_player = guest_name
        except:
            guest_name = 'Unknow'
        if input(
            'User `' + guest_name + '` wants to play. Do you accept? [y/n] '
        ) not in ('y', 'Y'):
            print('Rejected.')
            return Response('Rejected', status=403)

        game.guest_connected = True

        # start the session
        CURRENT_SESSION = str(uuid.uuid4())
        return CURRENT_SESSION

    @app.route('/me')
    def me():
        # return color of guest
        if CURRENT_SESSION is None:
            return Response('Please start a session first', status=401)

        try:
            if request.args['session'] == CURRENT_SESSION:
                # render the game
                return game.guest_color
            raise
        except:
            return Response('invalid session', status=401)

    @app.route('/render')
    def render():
        if CURRENT_SESSION is None:
            return Response('Please start a session first', status=401)

        try:
            if request.args['session'] == CURRENT_SESSION:
                # render the game and turn
                output = game.turn + '\n' + game.render()
                if game.is_end:
                    # game is finished
                    output += '\n' + ('Checkmate!' + (' ' * (len(game.ROW_SEPARATOR)-10)))
                    output += '\n' + (game.winner + ' won!' + (' ' * (len(game.ROW_SEPARATOR)-10)))
                return output
            raise
        except:
            return Response('invalid session', status=401)

    @app.route('/command')
    def command():
        if CURRENT_SESSION is None:
            return Response('Please start a session first', status=401)

        try:
            if request.args['session'] == CURRENT_SESSION:
                # put the command on the game object
                if request.args['cmd'].strip().lower() == 'back':
                    return Response('command `back` is disabled for guest', status=401)
                game.guest_ran = game.run_command(request.args['cmd'])
                return game.guest_ran
            raise ValueError()
        except:
            return Response('invalid session', status=401)

    print('Serving on ' + host + ':' + str(port))
    print('Others can join this game by running `tchess --connect ' + host + ':' + str(port) + '`')

    app.run(host, port)
