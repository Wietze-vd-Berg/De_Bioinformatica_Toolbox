import unittest
from Website.modules.salmon import salmon_handler

class TestSalmon(unittest.TestCase):
    def setUp(self):
        self.test_fasta_path = "tests/testfasta.fasta" # Gebruik een bestaand FASTA-bestand voor de test

    def test_salmon_py(self): # Dit test dus of een bestaand FASTA-bestand wel wordt verwerkt door Salmon
        with open(self.test_fasta_path, "rb") as fasta_file: # open dat bestand als een fasta-file voor de invoer
            opties = {'fasta_file': fasta_file} # soort van flask bestandupload maar dan in de test
            result = salmon_handler(opties)

            self.assertTrue(result['success'], {result.get('error')}) # Controleer of alles goed ging, anders error

if __name__ == '__main__':
    unittest.main()