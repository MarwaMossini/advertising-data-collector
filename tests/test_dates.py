import unittest
from collector import publication_date,metric_snapshot
class DateAndMetricTests(unittest.TestCase):
 def test_timestamp_recovers_date(self):
  self.assertEqual(publication_date({'timestamp':1792685485},{})[0],'2026-10-22')
 def test_upload_date_normalized(self):
  self.assertEqual(publication_date({'upload_date':'20260430'},{})[0],'2026-04-30')
 def test_does_not_guess_from_relative_or_invalid_dates(self):
  self.assertEqual(publication_date({'upload_date':'20260231'},{'published_date':'yesterday'})[0],'')
 def test_dated_source_requires_provenance(self):
  self.assertEqual(publication_date({}, {'published_date':'2026-04-30'})[0],'')
  self.assertEqual(publication_date({}, {'published_date':'2026-04-30','publication_date_source':'prior original metadata'})[0],'2026-04-30')
 def test_conflicting_view_count_withheld(self):
  v,note=metric_snapshot({'title':'7.5K views | Mop','view_count':1812})
  self.assertEqual(v['views'],'');self.assertIn('conflicts',note)
 def test_shares_and_reposts_are_distinct(self):
  v,_=metric_snapshot({'repost_count':3,'like_count':0})
  self.assertEqual(v['shares'],'');self.assertEqual(v['reposts'],3);self.assertEqual(v['likes'],0)
if __name__=='__main__':unittest.main()
