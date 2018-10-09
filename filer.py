import json

class File:
    def __init__(self, filename):
        self.filename = filename + ".json"

        if self.filename not in ['events', 'users']:
            return None


    def read(self):
        f = open(self.filename , "r")
        data = json.loads(f.read())
        f.close()
        return data


    def write(self, data):
        f = open(self.filename, "w")
        f.write(data)
        f.close()
        return True
