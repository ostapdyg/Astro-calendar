from .modules import *
import unittest


class test_file_io(unittest.TestCase):
    def test_basic_io(self):
        cal1 = Calendar.create_from_file('testcal_in.cal')
        self.assertEqual(cal1.get_for_date('20200103T044721Z')[0].url,
                         'https://in-the-sky.org/news.php?id=20200103_08_100')
        cal1.add_event(Event('Test Event', '20200301T010101', 'Test Event',
                             'www.testurl'))
        cal1.write_to_file('testcal_out.cal')
        cal2 = Calendar.create_from_file('testcal_out.cal')
        events1 = [ev for ev in cal1]
        events2 = [ev for ev in cal2]
        for i in range(len(events1)):
            self.assertEqual(events1[i], events2[i])


if __name__=='__main__':
    unittest.main()