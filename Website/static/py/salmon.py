import os
import subprocess


class SalmonInvoer:
#Classes die verantwoordelijk is voor het uitvoeren van Salmon-indexering en kwantisatie

    def __init__(self, index_path, input_file, r1, r2):
        """
        Initialiseert de klassenvariabelen voor indexeren en kwantiseren.

        :param index_path: Het pad naar de indexbestanden voor Salmon.
        :param input_file: Het bestand dat geüpload is voor verwerking.
        """
        self.input_file_path = index_path
        self.r1 = r1
        self.r2 = r2

        self.output_dir = f'../Website/salmon_file_manager/output/{input_file.filename}'

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # waneer output map niet bestaat maakt hij een aan

        self.index_dir = f'../Website/salmon_file_manager/index/{input_file.filename}'

        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)

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
            subprocess.run(console_cmd)
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
            output = subprocess.run(console_cmd)
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


def salmon_handler(opties):
    """
    Verwerkt de Salmon-analyse met de gegeven opties.

    :param opties: De checkboxes die in de SalmonInvoer-klasse worden aangevinkt als kwargs.
    :return: Het resultaat van de Salmon-analyse of een foutmelding.
    """
    fasta_file = opties['fasta_file']
    fasta_file_path = os.path.join('../Website/salmon_file_manager/uploads', fasta_file.filename)
    fastq_file1 = opties['fastq_file1']
    fastq_file1_file_path = os.path.join('../Website/salmon_file_manager/uploads', fastq_file1.filename)
    fastq_file2 = opties['fastq_file2']
    fastq_file2_file_path = os.path.join('../Website/salmon_file_manager/uploads', fastq_file2.filename)

    if not os.path.exists('../Website/salmon_file_manager/uploads'):
        os.makedirs('../Website/salmon_file_manager/uploads')

    fasta_file.save(fasta_file_path)
    fastq_file1.save(fastq_file1_file_path)
    fastq_file2.save(fastq_file2_file_path)

    print(f'salmon __init__ met {fasta_file.filename}, {fastq_file1.filename}, {fastq_file2.filename}')
    salmon_invoer = SalmonInvoer(fasta_file_path, fasta_file, fastq_file1_file_path, fastq_file2_file_path)

    print(f'salmon run_index met {fasta_file.filename}')
    indexresult = salmon_invoer.run_index()
    if not indexresult['success']:
        return indexresult

    print(f'salmon run_quant met indexed {fasta_file.filename}, r1&r2 als {fastq_file1.filename}, {fastq_file2.filename}')
    quantresult = salmon_invoer.run_quant(opties)
    if not quantresult['success']:
        # Retourneer de error als kwantisatie niet werkt, omdat de value ('success') dan false is
        return quantresult

    result = salmon_invoer.get_result()
    return result
