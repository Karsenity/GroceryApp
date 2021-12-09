class Event:
    def __init__(self, event, failedEvent=None, sourceName='BASE', description='ROOT'):
        self.sourceName = sourceName
        self.description = description
        self.event = event
        self.failedEvent = failedEvent


    def failed(self):
        if self.failedEvent is None:
            return None
        return Event(self.failedEvent, self.failedEvent, sourceName=self.sourceName, description=self.description)


    def start(self):
        self.event()
