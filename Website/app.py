from flask import Flask, render_template, request, url_for, redirect, send_from_directory

app = Flask(__name__)

# Home route die doorverwijst naar de indexpagina
@app.route('/')
def home():
    return redirect(url_for('index'))

# Route voor de indexpagina
@app.route('/index')
def index():
    return render_template('index.html', title='Home', active_page='index')

# Route voor de salmon_invoer pagina, waar je de gegevens kunt invoeren
@app.route('/salmon_invoer', methods=['GET', 'POST'])
def salmon_invoer():
    if request.method == 'GET':
        return render_template('salmon_invoer.html', title='Salmon Invoer', active_page='salmon_invoer')
    elif request.method == 'POST':
        # Verkrijg de checkbox-waarden uit het formulier
        kwargs = {
            'cb1': request.form.get('checkbox1'),
            'cb2': request.form.get('checkbox2'),
            'cb3': request.form.get('checkbox3')
        }
        # Render de resultaatpagina met de doorgegeven gegevens
        return render_template('resultaat.html', title='Resultaat', active_page='resultaat', **kwargs)

# Route voor de uitlegpagina
@app.route('/uitleg')
def uitleg():
    return render_template('uitleg.html', title='Uitleg', active_page='uitleg')

# Route voor het serveren van voorbeeld data (bijvoorbeeld JSON-bestanden)
@app.route('/Website/voorbeeld_data/<path:filename>')
def serve_json(filename):
    return send_from_directory('voorbeeld_data', filename)

# Route voor de contactpagina
@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', active_page='contact')

# Foutpagina voor 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_handling.html', title='Page not found', active_page='error_handling', error=e)

# Start de app
if __name__ == '__main__':
    app.run(debug=True)  # Debugmodus ingeschakeld voor foutopsporing
