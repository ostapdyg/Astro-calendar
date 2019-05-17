from Calendar import Calendar
from Event import Event
from Date import Date

cal1 = Calendar()
cal1.add(Event('Solar eclipse', '20190101T120020',
               {'Moon', 'Sun'}))
cal1.add(Event('Solar eclipse', '20190101T120020',
               {'Moon', 'Sun'}))

print(cal1.get_for_date(Date(2019, 1, 1)))