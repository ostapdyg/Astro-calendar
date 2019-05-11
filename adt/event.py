from date import Date


class Event:
    def __init__(self, event_type, event_start, event_end, bodies={}):
        self.event_type = event_type
        self.start_time = Date.date_from_str(event_start)
        self.end_time = Date.date_from_str(event_end)
        self.bodies = bodies

