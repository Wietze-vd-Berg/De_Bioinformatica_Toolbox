from flask import Flask, render_template, request, url_for, redirect, send_from_directory

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    """
    Rendert de indexpagina van de website.

    :param: Geen parameters.
    :return: De gerenderde 'index.html'-sjabloon met titel en actieve pagina.
    """
    return render_template('index.html', title='Home', active_page='index')


@app.route('/salmon_invoer', methods=['GET', 'POST'])
def salmon_invoer():
    """
    Behandelt de Salmon invoerpagina en verwerkt formulierinzendingen.

    Bij GET wordt de invoerpagina getoond. Bij POST worden checkbox-gegevens
    verzameld en doorgestuurd naar de resultaatpagina.

    :param: Geen directe parameters, maar gebruikt 'request' voor formulierdata.
    :return: De gerenderde 'salmon_invoer.html' bij GET, of 'resultaat.html' bij POST.
    """
    if request.method == 'GET':

        extra_input = False  # Standaard geen extra invoerveld

        if "checkbox3" in request.form:
            print("ik werk!")
            extra_input = True
            print(extra_input)
        else:
            print("Ik doe moeilijk en werk niet, loser!")

        return render_template('salmon_invoer.html', title='Salmon Invoer', active_page='salmon_invoer', extra_input_file=extra_input)
    elif request.method == 'POST':
        # Verkrijg checkbox-waarden uit het formulier
        kwargs = {
            'indexeddata': request.form.get('checkbox1'),
            'addlibtype': request.form.get('checkbox2'),
            'addmultiplefiles': request.form.get('checkbox3'),
            'addgcbias': request.form.get('checkbox4'),
            'addposbias': request.form.get('checkbox5'),
            'addseqbias': request.form.get('checkbox6')
        }

        fasta_file = request.files.get("fasta-file")
        if fasta_file:
            kwargs["fasta_file"] = fasta_file  # toevoegen aan de kwargs

        # Render resultaatpagina met checkbox-gegevens
        return render_template('resultaat.html', title='Resultaat', active_page='resultaat', **kwargs)


@app.route('/uitleg')
def uitleg():
    """
    Rendert de uitlegpagina.

    :param: Geen parameters.
    :return: De gerenderde 'uitleg.html'-sjabloon met titel en actieve pagina.
    """
    return render_template('uitleg.html', title='Uitleg', active_page='uitleg')


@app.route('/Website/voorbeeld_data/<path:filename>')
def serve_json(filename):
    """
    Serveert bestanden uit de 'voorbeeld_data'-map.

    :param filename: De naam van het bestand dat geserveerd moet worden.
    :return: Het gevraagde bestand uit de 'voorbeeld_data'-directory.
    """
    return send_from_directory('voorbeeld_data', filename)


@app.route('/contact')
def contact():
    """
    Rendert de contactpagina.

    :param: Geen parameters.
    :return: De gerenderde 'contact.html'-sjabloon met titel en actieve pagina.
    """
    return render_template('contact.html', title='Contact', active_page='contact')


@app.errorhandler(404)
def page_not_found(e):
    """
    Behandelt 404-fouten en toont een aangepaste foutpagina.

    :param e: De fout die de 404 heeft veroorzaakt.
    :return: De gerenderde 'error_handling.html'-sjabloon met foutinformatie.
    """
    return render_template('error_handling.html', title='Page not found', active_page='error_handling', error=e)


if __name__ == '__main__':
    app.run(debug=True)