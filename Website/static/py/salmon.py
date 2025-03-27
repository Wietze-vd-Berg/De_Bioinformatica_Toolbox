import os
import subprocess

class SalmonInvoer:
    def __init__(self, index_path, input_file):
        self.input_file_path = index_path
        self.output_dir = f'../Website/output/{input_file.filename}'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.index_dir = f'../Website/index/{input_file.filename}'
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)

    def run_index(self, input_file_path):
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

    def run_quant(self, input_file):
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
        result_file = os.path.join(self.output_dir, 'quant.sf')
        if os.path.exists(result_file):
            return {'success': True, 'result': open(result_file, 'r').readlines()}
        else:
            return {'success': False, 'error': 'File not found'}

def salmon_handler(opties):
    """

    :param opties: de checkboxes die in salmon_invoer worden aangevinkt als kwargs
    :return: de verwerkte data door salmon
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
    if not quantresult['success']: # Als quant niet heeft gewerkt
        return quantresult # Returnd de error

    result = salmon_invoer.get_result()
    return result