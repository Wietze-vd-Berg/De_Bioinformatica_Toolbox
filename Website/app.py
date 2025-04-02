import os
import matplotlib
matplotlib.use('Agg') # Voorkomt crashes met threads en plots
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, jsonify
from static.py.salmon import salmon_handler
import uuid, threading

# threading variabels
tasks = {}
results = {}

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
        # Verkrijg waardes uit het formulier
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

        task_id = str(uuid.uuid4())
        tasks[task_id] = "processing"

        threading.Thread(target=start_salmon_verwerking, args=(kwargs, fasta_file.filename, task_id)).start()

        return redirect(url_for("verwerken", task_id=task_id))

@app.route("/verwerken/<task_id>")
def verwerken(task_id):
    return render_template("verwerken.html", task_id=task_id)

@app.route("/status/<task_id>")
def status(task_id):
    return jsonify({"status": tasks.get(task_id, "onbekend")})

@app.route("/resultaat/<task_id>")
def resultaat(task_id):
    result = results.get(task_id)
    if not result:
        return "Resultaat niet gevonden", 404
    if not result['success']:
        return f"Fout tijdens verwerking: {result['error']}", 400

    bar_chart_data = generate_bar_chart(result['result'])

    return render_template(
        'resultaat.html',
        title='Resultaat',
        active_page='resultaat',
        bar_chart_data=bar_chart_data,
        kwargs=result['kwargs'],
        fasta_filename=result['fasta_filename']
    )



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

@app.route('/download/<fasta_filename>')
def download_quant_file(fasta_filename):
    folder = os.path.join('salmon_file_manager', 'output', fasta_filename)

    file_path = os.path.join(folder, 'quant.sf')
    print("Zoekpad:", file_path)
    if not os.path.exists(file_path):
        return f'Bestand niet gevonden', 404

    return send_from_directory(folder, 'quant.sf', as_attachment=True)

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
    plt.close()
    img_io.seek(0)
    bar_chart_data = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return bar_chart_data

def start_salmon_verwerking(kwargs, fasta_filename, task_id):
    try:
        quantresult = salmon_handler(kwargs)
        if quantresult['success']:
            results[task_id] = {
                "success": True,
                "result": quantresult['result'],
                "kwargs": kwargs,
                "fasta_filename": fasta_filename
            }
            tasks[task_id] = "done"
        else:
            results[task_id] = quantresult
            tasks[task_id] = "error"
    except Exception as e:
        results[task_id] = {"success": False, "error": str(e)}
        tasks[task_id] = "error"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
