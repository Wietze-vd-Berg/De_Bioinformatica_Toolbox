from flask import Flask, render_template, request, url_for, redirect, send_from_directory
app = Flask(__name__)


@app.route('/')
def home():  # Redirect naar onze 'home' pagina
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html', title='Home', active_page='index')

@app.route('/salmon_invoer', methods=['GET', 'POST'])
def salmon_invoer():
    if request.method == 'GET':
        return render_template('salmon_invoer.html', title='Salmon Invoer', active_page='salmon_invoer')
    elif request.method == 'POST':
        kwargs = request.form
        return render_template('resultaat.html', **kwargs, title='Resultaat', active_page='resultaat')

@app.route('/uitleg')
def uitleg():
    return render_template('uitleg.html', title='Uitleg', active_page='uitleg')

@app.route('/Website/voorbeeld_data/<path:filename>') # Om voorbeeld data te kunnen ophalen met flask, zonder dit geeft het een error
def serve_json(filename):
    return send_from_directory('voorbeeld_data', filename)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', active_page='contact')

@app.errorhandler(404) # Leuke pagina not found error handling :)
def page_not_found(e):
    return render_template('error_handling.html', title='Page not found', active_page='error_handling', error=e)

if __name__ == '__main__':
    app.run()
