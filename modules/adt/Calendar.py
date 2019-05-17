from modules.adt.array import TwoDimArray
from modules.adt.event import Event

class Calendar:
    @classmethod
    def create_from_file(cls, filename, calendar=None):
        """
        Create a new or add to existing Calendar based on file
        :param filename: str
        :return: Calendar object
        """
        with open(filename, 'r') as input_file:
            line = ''
            if not calendar:
                calendar = Calendar()
            while not line.startswith('BEGIN:VEVENT'):
                line = input_file.readline()
            while not line.startswith('END:VCALENDAR'):
                event = cls.read_event(input_file)
                if event:
                    calendar.add_event(event)
                line = input_file.readline()
        return calendar

    @staticmethod
    def read_event(input_file):
        """
        Read one event from file
        Precondition: pointer is after BEGIN:VEVENT
        :param input_file: file object
        :return: Event object
        """
        line = ''
        start_date = ''
        description = ''
        event_type = ''
        url = ''
        while not line.startswith('END:VEVENT'):
            line = input_file.readline()
            if line.startswith('DTSTART:'):
                start_date = line.split(':')[1][:-2]
            if line.startswith('SUMMARY:'):
                event_type = line.split(':')[1][:-1]
            if line.startswith('DESCRIPTION:'):
                description = line.split(':')[1][:-1]
            if line.startswith('URL:'):
                url = line.split(':')[1][:-1]
        if start_date and event_type and description:
            return Event(event_type, start_date, description, url)
        return None

    def __init__(self):
        self._years = dict()

    def add_event(self, event):
        """
        Add an event to calendar
        :param event:
        :return:
        """
        year = event.start_time.year
        if year in self._years:
            self._years[year].add_event(event)
        else:
            self._years[year] = Calendar.CalendarYear(year)
            self._years[year].add_event(event)

    def get_for_date(self, date):
        """
        Returns all events for some day
        :param date:
        :return:
        """
        year = date.year
        if year in self._years:
            return self._years[date.month, date.day]

    def __str__(self):
        res = ''
        for event in self:
            res += str(event) + '\n'
        return res

    def __iter__(self):
        return self.CalendarIterator(self._years)

    class CalendarYear:
        """
        Helper class for Calendar;
        Stores events for one year
        """
        def __init__(self, year):
            self.year = year
            self._months = TwoDimArray(13, 32)
            for month in range(13):
                for day in range(32):
                    self._months[month, day] = []
            self.a = self._months[1][2]


        def add_event(self, event):
            """
            Adds event to the calendar
            :param event: Event object
            :return:
            """
            if not isinstance(event, Event):
                raise TypeError
            if event.start_time.year != self.year:
                raise ValueError('Wrong event year')
            self._months[event.start_time.month][
                event.start_time.day].append(event)

        def __getitem__(self, d):
            """
            Return list of events for given month and day
            :param d: tuple of two ints, representing month and day
            :return:
            """
            return self._months[d[0]][d[1]]

        def __iter__(self):
            return Calendar.YearIterator(self._months)

        def __str__(self):
            res = ''
            for event in self:
                res += str(event)+'\n'
            return res

    class YearIterator:
        """
                Helper class for the Calendar.__iter__ method
        """
        def __init__(self, months):
            self._months = months
            self.cur_month = 1
            self.cur_day = 1
            self.cur_pos = 0
            self.n = 0

        def __next__(self):
            try:
                while self.cur_pos >= len(self._months[self.cur_month][self.cur_day]):
                    self.cur_day += 1
                    self.cur_month += self.cur_day//32
                    self.cur_day = self.cur_day%32
                    self.cur_pos = 0
                    if self.cur_month > 12:
                        raise StopIteration
                res = self._months[self.cur_month][self.cur_day][self.cur_pos]
                self.cur_pos += 1
                self.n += 1
                return res
            except IndexError:
                raise StopIteration

    class CalendarIterator:
        """
        Helper class for the CalendarYear.__iter__ method
        """
        def __init__(self, years):
            self._years = years
            self._years_nums = sorted(self._years.keys())
            if not self._years_nums:
                raise StopIteration
            self.pos = 0
            self.cur_iterator = self._years[self._years_nums[self.pos]].__iter__()

        def __next__(self):
            try:
                return self.cur_iterator.__next__()
            except StopIteration:
                try:
                    self.pos += 1
                    self.cur_iterator = self._years[
                        self._years_nums[self.pos]].__iter__()
                    return self.__next__()
                except IndexError:
                    raise StopIteration




a = Calendar.create_from_file('ical_2020.php')
print(len(str(a._years[2020]).split('\n')))
