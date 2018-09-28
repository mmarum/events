import json

class Read:

    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        if self.filename in ['events', 'users']:
            f = open(self.filename + ".json", "r")
            data = json.loads(f.read())
            f.close()
            return data
