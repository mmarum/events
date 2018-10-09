import json

# Maybe this is being
# replaced by EventForm
# in forms.py

class Event:
    def __init__(self, start, end, title, location, description):
        self.title = title
        self.start = start
        self.end = end
        self.location = location
        self.description = description


    def event_dict(self):
        return self.__dict__


    def write_event_json(self):
        f = open("events.json", "a")
        f.write(json.dumps(self.event_dict()))

