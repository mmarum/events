import json

class Event:
    def __init__(self, start, end, title):
        self.start = start
        self.end = end
        self.title = title

    def event_dict(self):
        return self.__dict__

    def write_event_json(self):
        f = open("events.json", "a")
        f.write(json.dumps(self.event_dict()))

