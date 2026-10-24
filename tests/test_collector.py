import unittest
from collector import classify, allowed, metric_issue

class EligibilityTests(unittest.TestCase):
    def setUp(self):
        self.info={'upload_date':'20241001','duration':20,'view_count':0,'like_count':0,'comment_count':0,'repost_count':0,'uploader':'IKEA India','title':'Shop now'}
        self.source={'allowed_uploaders':['IKEA India'],'promotion_keywords':['shop']}
    def test_zero_is_valid_but_missing_is_not(self):
        self.assertIsNone(classify(self.info,self.source))
        self.info['view_count']=None
        self.assertIsNotNone(classify(self.info,self.source))
    def test_reupload_excluded(self):
        self.info['uploader']='Random compilation channel'
        self.assertIsNotNone(classify(self.info,self.source))
    def test_gallery_excluded(self):
        self.info['_type']='multi_video'
        self.assertIsNotNone(classify(self.info,{'curated':True}))
    def test_unknown_date_excluded(self):
        del self.info['upload_date'];self.assertIsNotNone(classify(self.info,self.source))
    def test_required_metrics(self):
        for key in ('like_count', 'comment_count', 'repost_count', 'view_count'):
            info = dict(self.info)
            del info[key]
            self.assertIsNotNone(metric_issue(info))
    def test_conflicting_views(self):
        info = dict(self.info, title='7.5K views | Shop now', view_count=1795)
        self.assertIsNotNone(metric_issue(info))
    def test_hosts(self):
        self.assertTrue(allowed('https://www.youtube.com/watch?v=x'))
        self.assertFalse(allowed('https://youtube.com.example.org/x'))
        self.assertFalse(allowed('file:///etc/passwd'))

if __name__=='__main__':unittest.main()
