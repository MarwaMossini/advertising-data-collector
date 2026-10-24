import unittest
from collector import classify, allowed

class EligibilityTests(unittest.TestCase):
    def setUp(self):
        self.info={'upload_date':'20241001','duration':20,'view_count':0,'uploader':'IKEA India','title':'Shop now'}
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
    def test_hosts(self):
        self.assertTrue(allowed('https://www.youtube.com/watch?v=x'))
        self.assertFalse(allowed('https://youtube.com.example.org/x'))
        self.assertFalse(allowed('file:///etc/passwd'))

if __name__=='__main__':unittest.main()
