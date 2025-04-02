import os
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from flask import Flask, render_template, request, send_from_directory
from static.py.salmon import salmon_handler

app = Flask(__name__)

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

    Bij GET wordt de invoerpagina getoond. Bij POST worden de geüploade bestanden verwerkt en doorgestuurd naar de resultaatpagina.
    """
    if request.method == 'GET':
        return render_template('salmon_invoer.html', title='Salmon Invoer', active_page='salmon_invoer')

    elif request.method == 'POST':
        # Verkrijg checkbox-waarden uit het formulier
        kwargs = {}

        fasta_file = request.files.get("fasta-file")
        fastq_file1 = request.files.get("fastq-file1")
        fastq_file2 = request.files.get("fastq-file2")
        seqBias = request.form.get("seqBias")
        posBias = request.form.get('posBias')
        gcBias = request.form.get('gcBias')

        if not fasta_file or not fastq_file1 or not fastq_file2:
            return 'error-bericht', 400

        kwargs["fasta_file"] = fasta_file  # toevoegen aan de kwargs
        kwargs["fastq_file1"] = fastq_file1
        kwargs["fastq_file2"] = fastq_file2

        if seqBias: kwargs['seqBias'] = True
        else: kwargs['seqBias'] = False

        if posBias: kwargs['posBias'] = True
        else: kwargs['posBias'] = False

        if gcBias: kwargs['gcBias'] = True
        else: kwargs['gcBias'] = False

        # Voer de Salmon-analyse uit met de gegeven parameters
        quantresult = salmon_handler(kwargs)

        if not quantresult['success']: # Error handling
            return str(quantresult['error']).replace('\n', '<br>'), 400 #returnd de error plus een 400 status code

        # Veronderstel dat quantresult de analysegegevens bevat die je nodig hebt voor de heatmap
        # Zorg ervoor dat quantresult de juiste vorm heeft (bijv. een 2D lijst of numpy array)

        # Gebruik hier de juiste gegevens van quantresult voor de heatmap
        # Voorbeeld: neem aan dat quantresult een dictionary is en dat 'data' een numpy array bevat.
        # Pas dit aan op basis van je werkelijke output van Salmon

        data_fastq1 = quantresult['result']

        # Genereer de staafgrafiek
        bar_chart_data = generate_bar_chart(data_fastq1)

        return render_template('resultaat.html', title='Resultaat', active_page='resultaat',
                               bar_chart_data=bar_chart_data, kwargs=kwargs)


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


@app.route("/test-salmon")
def test_salmon():
    import subprocess
    try:
        output = subprocess.check_output(["salmon", "--version"], text=True)
        return f"<pre>{output}</pre>"
    except FileNotFoundError:
        return "Salmon niet gevonden."



def generate_bar_chart(data_fastq1):
    """
    Genereert een staafgrafiek met TPM-expressie van de top 10 genen.

    :param data_fastq1: Lijst met expressiewaarden van FASTQ 1
    :param data_fastq2: Lijst met expressiewaarden van FASTQ 2
    :return: Base64-encoded afbeelding
    """
    top10 = sorted(data_fastq1, key=lambda x: x['TPM'], reverse=True)[:10]
    labels = [d['Name'] for d in top10]
    values_fastq1 = [d['TPM'] for d in top10]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    x = np.arange(len(labels))

    ax.bar(x - bar_width/2, values_fastq1, bar_width, label='FASTQ 1', color='salmon')

    ax.set_xlabel('Genen')
    ax.set_ylabel('TPM Expressie')
    ax.set_title('TPM Expressie Vergelijking (Top 10)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    # Voeg een ondertitel toe met uitleg
    plt.figtext(0.5, -0.1, "TPM-expressie van de top 10 genen op basis van RNA-sequentieanalyse.",
                wrap=True, horizontalalignment='center', fontsize=10)

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    bar_chart_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close()

    return bar_chart_data


if __name__ == '__main__':
    app.run(debug=True)
