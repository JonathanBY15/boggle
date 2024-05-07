from boggle import Boggle
from flask import Flask, render_template, request, jsonify, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = '734-154-693'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SECRET_KEY"] = "secret_key"

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def index():
    """Show the board."""
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board, high_score=session.get("high_score", 0))

@app.route('/guess', methods=['POST', 'GET'])
def guess():
    """Check if guess is in dictionary and on board."""
    guess = request.json['guess']

    words = boggle_game.read_dict("words.txt")

    word_is_in_dict = guess in words
    is_valid_word = boggle_game.check_valid_word(session['board'], guess)

    if(is_valid_word == "ok"):
        return {"result": "ok"}
    elif(is_valid_word == "not-on-board"):
        return {"result": "not-on-board"}
    else:
        return {"result": "not-word"}

    return redirect('/')

# track high score
@app.route('/high-score', methods=['POST'])
def high_score():
    """Update high score if necessary."""
    score = request.json['score']
    high_score = session.get("high_score", 0)

    if score > high_score:
        session["high_score"] = score
        return jsonify(isHighScore=True)
    else:
        return jsonify(isHighScore=False)
    
# view function to return the high score
@app.route('/high-score', methods=['GET'])
def get_high_score():
    """Return high score."""    
    return jsonify(high_score=session.get("high_score", 0))