from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "tic-tac-toe-secret"

def init_game():
    session['board'] = [" "] * 9
    session['current_player'] = "X"
    session['winner'] = None
    session['draw'] = False

def check_winner(board, icon):
    win_combos = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in win_combos:
        if board[a] == board[b] == board[c] == icon:
            return True
    return False

def check_draw(board):
    return " " not in board

@app.route("/", methods=["GET", "POST"])
def index():
    if 'board' not in session:
        init_game()

    if request.method == "POST":
        if 'reset' in request.form:
            init_game()
            return redirect(url_for('index'))

        if session['winner'] is None and not session['draw']:
            move = int(request.form['move'])
            board = session['board']
            current = session['current_player']

            if board[move] == " ":
                board[move] = current
                if check_winner(board, current):
                    session['winner'] = current
                elif check_draw(board):
                    session['draw'] = True
                else:
                    session['current_player'] = "O" if current == "X" else "X"
                session['board'] = board

        return redirect(url_for('index'))  

    return render_template(
        "index.html",
        board=session['board'],
        current_player=session['current_player'],
        winner=session['winner'],
        draw=session['draw']
    )

if __name__ == "__main__":
    app.run(debug=True)
