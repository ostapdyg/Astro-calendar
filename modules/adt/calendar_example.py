from modules import *

cal1 = Calendar.create_from_file('data/ical_2020.php')
for event in cal1:
    print(event.description)

cal1.add_event(Event('Solar eclipse', '20190101T120020',
               {'Moon', 'Sun'}))
cal1.add_event(Event('Solar eclipse', '20190101T120020',
               {'Moon', 'Sun'}))

print(cal1.get_for_date(Date(2019, 1, 1)))