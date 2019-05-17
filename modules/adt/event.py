from date import Date

BODIES_NAMES = {
    'solar': 'Sun',
    'sun': 'Sun',
    'lunar': 'Moon',
    'mercury': 'Mercury',
    'venus': 'Venus',
    'earth': 'Earth',
    'mars': 'Mars',
    'jupiter': 'Jupiter',
    'saturn': 'Saturn',
    'neptune': 'Neptune'
    ''
}

class Event:
    def __init__(self, event_type, event_start, description='', url=''):
        self.event_type = event_type
        self.start_time = Date.date_from_str(event_start)
        self.bodies = set()
        self.description = description
        self.url = url

    def __str__(self):
        return self.event_type+'-'+str(self.start_time)

    def __gt__(self, other):
        return self.start_time>other.start_time

    def __eq__(self, other):
        return self.start_time==other.start_time

    def get_bodies(self):
        """
        Find celestial bodies mentioned in description
        :return:
        """

    def __repr__(self):
        return str(self)
