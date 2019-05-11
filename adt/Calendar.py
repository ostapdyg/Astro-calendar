from adt.array import Array
from adt.event import Event

class Calendar:
    @classmethod
    def create_from_file(cls, filename):
        """
        Create a new Calendar based on file
        :param filename: str
        :return: Calendar object
        """
        pass

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

    class CalendarYear:
        """
        Helper class for Calendar;
        Stores events for one year
        """
        def __init__(self, year):
            self.year = year
            self._months = Array(13, Array(32, []))

        def add_event(self, event):
            """
            Adds event to the calendar
            :param event: Event object
            :return:
            """
            if not event.isinstance(Event):
                raise TypeError
            if event.start_time.year != self.year:
                raise ValueError('Wrong event year')
            self._months[event.start_time.months][
                event.start_time.day].append(event)
            self._months[event.start_time.months][
                event.start_time.day].sort()

        def __getitem__(self, d):
            """
            Return list of events for given month and day
            :param d: tuple of two ints, representing month and day
            :return:
            """
            return self._months[d[0]][d[1]]

        def __iter__(self):
            return Calendar.YearIterator

    class YearIterator:
        def __init__(self, months):
            self._months = months
            self.cur_month = 1
            self.cur_day = 1
            self.cur_pos = 0

        def __next__(self):
            try:
                while self.cur_pos >= self._months[self.cur_month, self.cur_day]:
                    self.cur_day += 1
                    self.cur_month += self.cur_day//32
                    self.cur_day = self.cur_day%32
                    self.cur_pos = 0
                    if self.cur_month > 12:
                        raise StopIteration
                res = self._months[self.cur_month, self.cur_day][self.cur_pos]
                self.cur_pos += 1
                return res
            except IndexError:
                raise StopIteration

    class CalendarIterator:
        def __init__(self, years):
            self._years = years
            self._years_nums = sorted(self._years.keys())
            if self._years_nums == []:
                raise StopIteration
            self.pos = 0
            self.cur_iterator = self._years[self._years_nums[0]].__iter__()

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



a = Array(10, [Event('Solar eclipse', '20190101T120020', '20190101T120510',{'Moon', 'Sun'})])
print(a[0])
