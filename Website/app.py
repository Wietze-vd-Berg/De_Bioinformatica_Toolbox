from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html', title='Home', activate_page='index')

@app.route('/salmon_invoer')
def salmon_invoer():
    if request.method == 'GET':
        return render_template('salmon_invoer.html', title='Salmon Invoer', activate_page='salmon_invoer')
    elif request.method == 'POST':
        kwargs = request.form
        return render_template('resultaat.html', **kwargs, title='Resultaat')

@app.route('/uitleg')
def uitleg():
    return render_template('uitleg.html', title='Uitleg', activate_page='uitleg')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', activate_page='contact')

@app.errorhandler(404)
def page_not_found(e):
    return f'<title>Error 404</title>Page not found! <br>{e}'

if __name__ == '__main__':
    app.run()
