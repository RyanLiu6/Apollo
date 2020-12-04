class Santa:
    def __init__(self, name, recipient):
        self.name = name
        self.recipient = recipient

class SecretSantas:
    def __init__(self):
        self.santas = {}

    def add_santa(self, santa):
        self.santas[santa.name] = santa

    def get_santa(self, name):
        return self.santas[name]

    def get_names(self):
        return self.santas.keys()

    def __str__(self):
        to_return = ""
        for k, v in self.santas.items():
            to_return += f"Name: {k} | Recipient: {v.recipient}\n"

        return to_return
