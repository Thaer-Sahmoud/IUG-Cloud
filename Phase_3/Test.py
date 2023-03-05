from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/message', methods=['POST'])
def message():
    msg = request.form['message']
    return render_template('message.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
