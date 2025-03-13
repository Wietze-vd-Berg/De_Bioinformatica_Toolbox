from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', title='Home')

@app.route('/salmon_invoer')
def salmon_invoer():
    return render_template('salmon_invoer.html', title='Salmon Invoer')


if __name__ == '__main__':
    app.run()
