from datetime import datetime


class AuditLogger:

    def __init__(self):

        self.events = []

    def record(
        self,
        event,
        action=None,
        resource=None,
        result=None
    ):

        entry = {

            "timestamp": datetime.now().isoformat(),

            "event": event,

            "action": action,

            "resource": resource,

            "result": result
        }

        self.events.append(entry)

    def get_events(self):

        return list(self.events)

    def clear(self):

        self.events.clear()