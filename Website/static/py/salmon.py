import os
import subprocess


class SalmonInvoer:
#Classes die verantwoordelijk is voor het uitvoeren van Salmon-indexering en kwantisatie

    def __init__(self, index_path, input_file):
        """
        Initialiseert de klassenvariabelen voor indexeren en kwantiseren.

        :param index_path: Het pad naar de indexbestanden voor Salmon.
        :param input_file: Het bestand dat geüpload is voor verwerking.
        """
        self.input_file_path = index_path
        self.output_dir = f'../Website/output/{input_file.filename}'

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # waneer output map niet bestaat maakt hij een aan

        self.index_dir = f'../Website/index/{input_file.filename}'

        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)

    def run_index(self, input_file_path):
        """
        Voert de Salmon-indexering uit op het opgegeven bestand.

        :param input_file_path: Het pad naar het bestand dat moet worden geïndexeerd.
        :return: Een dictionary met het resultaat van de indexering.
        """
        console_cmd = [
            'salmon', 'index',
            '-t', input_file_path,
            '-i', self.index_dir
        ]
        try:
            subprocess.check_output(console_cmd, text=True)
            return {'success': True}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e}
        # geeft een error als er geen output in staat

    def run_quant(self, input_file):
        """
        Voert de Salmon-kwantisatie uit op het geüploade bestand.

        :param input_file: Het bestand dat moet worden gekwantificeerd.
        :return: Een dictionary met het resultaat van de kwantisatie.
        """
        console_cmd = [
            'salmon', 'quant',
            '-i', self.index_dir,
            '-l', 'A',
            '-r', self.input_file_path,
            '-o', self.output_dir,
        ]

        try:
            output = subprocess.check_output(console_cmd, text=True)
            return {'success': True, 'output': output}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': str(e)}

    def get_result(self):
        """
        Haalt het resultaat op van de Salmon-kwantisatie.

        :return: Het resultaat van de kwantisatie, of een foutmelding als het bestand niet wordt gevonden.
        """
        result_file = os.path.join(self.output_dir, 'quant.sf')
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                return {'success': True, 'result': f.readlines()}
        else:
            return {'success': False, 'error': 'File not found'}


def salmon_handler(opties):
    """
    Verwerkt de Salmon-analyse met de gegeven opties.

    :param opties: De checkboxes die in de SalmonInvoer-klasse worden aangevinkt als kwargs.
    :return: Het resultaat van de Salmon-analyse of een foutmelding.
    """
    uploaded_file = opties['fasta_file']
    file_path = os.path.join('../Website/uploads', uploaded_file.filename)

    if not os.path.exists('../Website/uploads'):
        os.makedirs('../Website/uploads')
    uploaded_file.save(file_path)

    salmon_invoer = SalmonInvoer(file_path, uploaded_file)

    indexresult = salmon_invoer.run_index(file_path)
    if not indexresult['success']:
        return indexresult

    quantresult = salmon_invoer.run_quant(file_path)
    if not quantresult['success']:
        # Retourneer de error als kwantisatie niet werkt, omdat de value ('success') dan false is
        return quantresult

    result = salmon_invoer.get_result()
    return result
