class SalmonInvoer:
    def __init__(self):
        self.consolemsg = []
    def add_option(self, option):
        if option:
            self.consolemsg.append(f'{option[0]}: {option[1] if option[1] == 'checked' else 'not checked'}')
        else:
            self.consolemsg.append('NoneType')

    def dosalmon(self):
        print(', '.join(self.consolemsg))

def salmon_handler(opties):
    """

    :param opties: de checkboxes die in salmon_invoer worden aangevinkt als kwargs
    :return: de verwerkte data door salmon
    """
    print(type(opties))
    salmon_invoer = SalmonInvoer()
    for key, value in opties.items():
        salmon_invoer.add_option([key, value])

    salmon_invoer.dosalmon()