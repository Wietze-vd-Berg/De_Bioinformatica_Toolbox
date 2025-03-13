from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', title='Home')

@app.route('/salmon_invoer')
def salmon_invoer():
    if request.method == 'GET':
        return render_template('salmon_invoer.html', title='Salmon Invoer')
    elif request.method == 'POST':
        kwargs = request.form
        return render_template('resultaat.html', **kwargs, title='Resultaat')


if __name__ == '__main__':
    app.run()
