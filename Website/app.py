import os
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from flask import Flask, render_template, request, send_from_directory
from static.py.salmon import salmon_handler

app = Flask(__name__)


# Functie voor het genereren van een heatmap
def generate_heatmap(analysis_data):
    """
    Genereer een heatmap op basis van de analysegegevens van Salmon.
    """
    # Hier verwerk je de daadwerkelijke analysegegevens (bijvoorbeeld 'analysis_data' moet een 2D lijst of numpy array zijn)
    if isinstance(analysis_data, np.ndarray):  # Als de data een numpy array is
        heatmap_data = analysis_data
    else:
        # Converteer andere soorten data naar een numpy array (bijv. van dict, lijst, etc.)
        heatmap_data = np.array(analysis_data)  # Vervang deze lijn door je eigen conversielogica

    # Maak de heatmap met matplotlib
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.imshow(heatmap_data, cmap='hot', interpolation='nearest')
    fig.colorbar(cax)

    # Sla de afbeelding op in geheugen in plaats van op schijf
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)

    # Converteer de afbeelding naar een base64 string
    heatmap_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return heatmap_data


@app.route('/')
@app.route('/index')
def index():
    """
    Rendert de indexpagina van de website.
    """
    return render_template('index.html', title='Home', active_page='index')


@app.route('/salmon_invoer', methods=['GET', 'POST'])
def salmon_invoer():
    """
    Behandelt de Salmon invoerpagina en verwerkt formulierinzendingen.
    """
    if request.method == 'GET':
        extra_input = False  # Standaard geen extra invoerveld

        if "checkbox3" in request.form:
            print("ik werk!")
            extra_input = True
            print(extra_input)
        else:
            print("Ik doe moeilijk en werk niet, loser!")

        return render_template('salmon_invoer.html', title='Salmon Invoer', active_page='salmon_invoer',
                               extra_input_file=extra_input)
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

        # Voer de Salmon-analyse uit met de gegeven parameters
        quantresult = salmon_handler(kwargs)

        # Veronderstel dat quantresult de analysegegevens bevat die je nodig hebt voor de heatmap
        # Zorg ervoor dat quantresult de juiste vorm heeft (bijv. een 2D lijst of numpy array)

        # Gebruik hier de juiste gegevens van quantresult voor de heatmap
        # Voorbeeld: neem aan dat quantresult een dictionary is en dat 'data' een numpy array bevat.
        # Pas dit aan op basis van je werkelijke output van Salmon

        if isinstance(quantresult, dict) and 'data' in quantresult:
            analysis_data = quantresult['data']  # Vervang door de juiste sleutel van je resultaat
        else:
            analysis_data = np.random.rand(10, 10)  # Gebruik hier de echte data van Salmon

        # Genereer de heatmap afbeelding met de werkelijke data
        heatmap_data = generate_heatmap(analysis_data)

        # Render de resultaatpagina met de heatmap
        return render_template('resultaat.html', title='Resultaat', active_page='resultaat', heatmap_data=heatmap_data,
                               **kwargs)


@app.route('/uitleg')
def uitleg():
    """
    Rendert de uitlegpagina.
    """
    return render_template('uitleg.html', title='Uitleg', active_page='uitleg')


@app.route('/Website/voorbeeld_data/<path:filename>')
def serve_json(filename):
    """
    Serveert bestanden uit de 'voorbeeld_data'-map.
    """
    return send_from_directory('voorbeeld_data', filename)


@app.route('/contact')
def contact():
    """
    Rendert de contactpagina.
    """
    return render_template('contact.html', title='Contact', active_page='contact')


@app.errorhandler(404)
def page_not_found(e):
    """
    Behandelt 404-fouten en toont een aangepaste foutpagina.
    """
    return render_template('error_handling.html', title='Page not found', active_page='error_handling', error=e)


if __name__ == '__main__':
    app.run(debug=True)
