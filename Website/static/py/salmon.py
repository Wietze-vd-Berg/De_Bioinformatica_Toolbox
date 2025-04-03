import os
import subprocess


class SalmonInvoer:
#Classes die verantwoordelijk is voor het uitvoeren van Salmon-indexering en kwantisatie

    def __init__(self, index_path, fasta_filename, r1_path, r2_path):
        self.input_file_path = index_path
        self.r1 = r1_path
        self.r2 = r2_path
        self.output_dir = f'../Website/salmon_file_manager/output/{fasta_filename}'
        self.index_dir = f'../Website/salmon_file_manager/index/{fasta_filename}'

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.index_dir, exist_ok=True)

    def run_index(self):
        """
        Voert de Salmon-indexering uit op het opgegeven bestand.

        :return: Een dictionary met het resultaat van de indexering.
        """
        console_cmd = [
            'salmon', 'index',
            '-t', self.input_file_path,
            '-i', self.index_dir
        ]
        try:
            subprocess.run(console_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {'success': True}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e}
        # geeft een error als er geen output in staat

    def run_quant(self, opties):
        """
        Voert de Salmon-kwantisatie uit op het geüploade bestand.

        :return: Een dictionary met het resultaat van de kwantisatie.
        """
        console_cmd = [
            'salmon', 'quant',
            '--quiet',
            '-i', self.index_dir,
            '-l', 'A',
            '-1', self.r1,
            '-2', self.r2,
            '-o', self.output_dir,
        ]
        if opties['gcBias']: console_cmd.append('--gcBias')
        if opties['seqBias']: console_cmd.append('--seqBias')
        if opties['posBias']: console_cmd.append('--posBias')

        try:
            output = subprocess.run(console_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': str(e)}

        return {'success': True, 'output': output}

    def get_result(self):
        result_file = os.path.join(self.output_dir, 'quant.sf')
        if os.path.exists(result_file):
            try:
                with open(result_file, 'r') as f:
                    lines = f.readlines()

                header = lines[0].strip().split('\t')
                result_list = []

                for line in lines[1:]:
                    values = line.strip().split('\t')
                    entry = dict(zip(header, values))
                    entry['TPM'] = float(entry['TPM'])  # Zorg dat TPM numeriek is
                    result_list.append(entry)

                return {'success': True, 'result': result_list}
            except Exception as e:
                return {'success': False, 'error': f'Fout bij inlezen quant.sf: {e}'}
        else:
            return {'success': False, 'error': 'quant.sf niet gevonden'}


def salmon_handler(opties, status_callback=None):
    def report(step, status="processing"):
        if status_callback:
            status_callback(step, status)

    fasta_file_path = opties["fasta_file_path"]
    fastq_file1_path = opties["fastq_file1_path"]
    fastq_file2_path = opties["fastq_file2_path"]
    fasta_filename = os.path.basename(fasta_file_path)

    salmon_invoer = SalmonInvoer(
                    fasta_file_path,     # index_path
                    fasta_filename,      # naam van fasta bestand
                    fastq_file1_path,    # R1 path
                    fastq_file2_path     # R2 path
        )


    report("index", "processing")
    # indexering
    indexresult = salmon_invoer.run_index()
    if not indexresult['success']:
        report("index", "error")
        return indexresult
    report("index", "done")

    report("quant", "processing")
    quantresult = salmon_invoer.run_quant(opties)
    if not quantresult['success']:
        report("quant", "error")
        return quantresult
    report("quant", "done")

    result = salmon_invoer.get_result()

    return result


