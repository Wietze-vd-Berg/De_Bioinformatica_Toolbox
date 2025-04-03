import os
import uuid, threading

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, jsonify

from modules import barchart
from static.py.salmon import salmon_handler

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

        # 1. Tijdelijke map aanmaken
        temp_dir = os.path.join("tmp_uploads", str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)

        # 2. Bestanden opslaan
        fasta_path = os.path.join(temp_dir, fasta_file.filename)
        fastq1_path = os.path.join(temp_dir, fastq_file1.filename)
        fastq2_path = os.path.join(temp_dir, fastq_file2.filename)

        fasta_file.save(fasta_path)
        fastq_file1.save(fastq1_path)
        fastq_file2.save(fastq2_path)

        # 3. Alleen paden meegeven
        kwargs["fasta_file_path"] = fasta_path
        kwargs["fastq_file1_path"] = fastq1_path
        kwargs["fastq_file2_path"] = fastq2_path

        if seqBias: kwargs['seqBias'] = True
        else: kwargs['seqBias'] = False

        if posBias: kwargs['posBias'] = True
        else: kwargs['posBias'] = False

        if gcBias: kwargs['gcBias'] = True
        else: kwargs['gcBias'] = False

        # Voer de Salmon-analyse uit met de gegeven parameters

        task_id = str(uuid.uuid4())
        tasks[task_id] = "processing"

        threading.Thread(target=start_salmon_verwerking, args=(kwargs, task_id)).start()

        return redirect(url_for("verwerken", task_id=task_id))

@app.route("/verwerken/<task_id>")
def verwerken(task_id):
    return render_template("verwerken.html", task_id=task_id)

@app.route("/status/<task_id>")
def status(task_id):
    task_info = tasks.get(task_id, {"step": "onbekend", "status": "queued"})
    result = results.get(task_id)

    response = {
        "status": task_info["status"],
        "step": task_info["step"]
    }

    if result:
        response["success"] = result.get("success")
        response["error"] = result.get("error")
        response["status_code"] = result.get("status_code", 200 if result.get("success") else 500)

    return jsonify(response), response.get("status_code", 200)



@app.route("/resultaat/<task_id>")
def resultaat(task_id):
    result = results.get(task_id)
    if not result:
        return "Resultaat niet gevonden", 404
    if not result['success']:
        return f"Fout tijdens verwerking: {result['error']}", 400

    update_step(task_id, "chart", "processing")
    bar_chart_data = barchart.generate_bar_chart(result['result'])
    update_step(task_id, "chart", "done")

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

@app.route('/resultaat/download/<fasta_filename>')
def download_quant_file(fasta_filename):
    folder = os.path.join(app.root_path, 'salmon_file_manager', 'output', fasta_filename)

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

def start_salmon_verwerking(kwargs, fasta_filename, task_id):
    try:
        tasks[task_id] = {"step": "index", "status": "processing"}
        quantresult = {}

        print(f"[{task_id}] Start Salmon index")
        result = salmon_handler(kwargs, status_callback=lambda step, status: update_step(task_id, step, status))

        if result['success']:
            tasks[task_id] = {"step": "done", "status": "done"}
            results[task_id] = {
                "success": True,
                "result": result['result'],
                "kwargs": kwargs,
                "fasta_filename": os.path.basename(kwargs['fasta_file_path'])
            }
        else:
            tasks[task_id] = {"step": "error", "status": "error"}
            results[task_id] = {
                "success": False,
                "error": result.get("error", "Onbekende fout"),
                "status_code": 500
            }

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        tasks[task_id] = {"step": "error", "status": "error"}
        results[task_id] = {
            "success": False,
            "error": str(e),
            "trace": error_trace,
            "status_code": 500
        }

    finally:
        try:
            os.remove(kwargs['fasta_file_path'])
            os.remove(kwargs['fastq_file1_path'])
            os.remove(kwargs['fastq_file2_path'])
            os.rmdir(os.path.dirname(kwargs['fasta_file_path']))  # verwijder tijdelijke map
        except Exception as e:
            print(f"Fout bij opruimen: {e}")

def update_step(task_id, step, status):
    tasks[task_id] = {"step": step, "status": status}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
