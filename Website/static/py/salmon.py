import os
import subprocess

class SalmonInvoer:
    def __init__(self, index_path):
        self.index_path = index_path
        self.output_dir = '../Website/output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def run_quant(self, input_file):
        console_cmd = [
            'salmon', 'quant',
            '-i', self.index_path,
            '-l', 'A',
            '-r', input_file,
            '-o', self.output_dir,
        ]
        try:
            output = subprocess.check_output(console_cmd, text=True)
        except subprocess.CalledProcessError as e:



    def dosalmon(self):
        print(', '.join(self.consolemsg))

def salmon_handler(opties):
    """

    :param opties: de checkboxes die in salmon_invoer worden aangevinkt als kwargs
    :return: de verwerkte data door salmon
    """

    salmon_invoer = SalmonInvoer()
    for key, value in opties.items():
        salmon_invoer.add_option([key, value])

    salmon_invoer.dosalmon()