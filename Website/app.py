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
        kwargs = {
            'cb1' : request.form.get('checkbox1'),
            'cb2' : request.form.get('checkbox2'),
            'cb3' : request.form.get('checkbox3')
        }
        return render_template('resultaat.html', title='Resultaat', active_page='resultaat', **kwargs)

@app.route('/uitleg')
def uitleg():
    return render_template('uitleg.html', title='Uitleg', active_page='uitleg')

@app.route('/Website/voorbeeld_data/<path:filename>') # Om voorbeeld data te kunnen ophalen met flask, zonder dit geeft het een error
def serve_json(filename):
    return send_from_directory('voorbeeld_data', filename)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', active_page='contact')

@app.errorhandler(Exception) # Leuke pagina not found error handling :)
def error_handler(e):
    error_code = getattr(e, 'code', 500)
    return render_template('error_handling.html', title=f'error {error_code}', active_page='error_handling', error=e, error_code=error_code)

if __name__ == '__main__':
    app.run()
