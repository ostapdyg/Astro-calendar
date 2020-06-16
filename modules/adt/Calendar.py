from modules.adt import Date
from modules.adt import TwoDimArray
from modules.adt import Event
from os import path

class Calendar:
    @classmethod
    def create_from_file(cls, filename, calendar=None):
        """
        Create a new or add to existing Calendar based on file
        :param filename: str
        :return: Calendar object
        """
        if not calendar:
            calendar = Calendar()
        calendar.add_from_file(filename)
        return calendar

    def add_from_file(self, filename):
        """
        Add to a calendar events from the file
        :param filename: str
        :return: Calendar object
        """
        filename = path.abspath(filename)
        with open(filename, 'r') as input_file:
            line = ' '
            while not line.startswith('BEGIN:VEVENT'):
                if line == '':
                    return
                line = input_file.readline()
            while not line.startswith('END:VCALENDAR'):
                if line == '':
                    return
                event = self.read_event(input_file)
                if event:
                    self.add_event(event)
                line = input_file.readline()
        return

    def write_to_file(self, filename):
        filename = path.abspath(filename)
        with open(filename, 'w') as output_file:
            for event in self:
                output_file.writelines(['BEGIN:VEVENT\n',
                                        'DTSTART:' +
                                        event.start_time.file_str()+'\n',
                                        'SUMMARY:'+event.event_type+'\n',
                                        'DESCRIPTION:'+event.description+'\n',
                                        'URL:'+event.url+'\n',
                                        'END:VEVENT\n'
                                        ])
            output_file.write('END:VCALENDAR')


    @staticmethod
    def read_event(input_file):
        """
        Read one event from file
        Precondition: pointer is after BEGIN:VEVENT
        :param input_file: file object
        :return: Event object
        """
        line = ' '
        start_date = ''
        description = ''
        event_type = ''
        url = ''
        while not line.startswith('END:VEVENT'):
            if line=='':
                return
            line = input_file.readline()
            if line.startswith('DTSTART:'):
                start_date = line.split(':')[1][:-2]
            if line.startswith('SUMMARY:'):
                event_type = line.split(':')[1][:-1]
            if line.startswith('DESCRIPTION:'):
                description = line.split(':')[1].split('.')[0]+'.'
            if line.startswith('URL:'):
                url = ':'.join(line.split(':')[1:])[:-1]
        if start_date and event_type and description:
            return Event(event_type, start_date, description, url)
        return None

    def __init__(self):
        self._years = {}

    def add_event(self, event):
        """
        Add an event to calendar
        :param event:
        :return:
        """
        year = event.start_time.year
        if year not in self._years:
            self._years[year] = Calendar.CalendarYear(year)

        self._years[year].add_event(event)

    def remove_event(self, event):
        if not isinstance(event, Event):
            raise TypeError
        if event in self.get_for_date(event.start_time):
            self.get_for_date(event.start_time).remove(event)

    def get_for_date(self, date):
        """
        Returns all events for some day
        :param date:
        :return:
        """
        if type(date) == str:
            date = Date.date_from_str(date)
        year = date.year
        if year in self._years:
            return self._years[year][date.month, date.day]

    def __str__(self):
        res = ''
        for event in self:
            res += str(event) + '\n'
        return res

    def __iter__(self):
        return self.CalendarIterator(self._years)

    def __contains__(self, item):
        return item in self.get_for_date(item.date)

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
            for ev in self._months[event.start_time.month][
                                    event.start_time.day]:
                if ev == event:
                    return
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
            if self._years_nums:
                self.pos = 0
                self.cur_iterator = self._years[self._years_nums[self.pos]].__iter__()

        def __next__(self):
            if not self._years_nums:
                raise StopIteration
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





