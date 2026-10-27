import csv, json, tempfile, unittest
from pathlib import Path
from collector import AD_FIELDS, SNAPSHOT_FIELDS, platform_for, scalar, migrate_legacy

class CuratedSourceTests(unittest.TestCase):
    def test_supported_public_post_urls(self):
        self.assertEqual(platform_for('https://www.instagram.com/p/ABC/'),'Instagram')
        self.assertEqual(platform_for('https://www.facebook.com/reel/123/'),'Facebook')
        self.assertEqual(platform_for('https://youtu.be/abc'),'YouTube')
        self.assertEqual(platform_for('https://tiktok.com/@x/video/123'),'TikTok')
    def test_rejects_non_https_and_lookalike_hosts(self):
        self.assertIsNone(platform_for('http://facebook.com/x'))
        self.assertIsNone(platform_for('https://facebook.com.example.org/x'))
    def test_missing_metric_stays_blank_and_zero_is_real(self):
        self.assertEqual(scalar({'like_count':0},'like_count'),0)
        self.assertEqual(scalar({},'like_count'),'')
        self.assertEqual(scalar({'like_count':None},'like_count'),'')
    def test_legacy_output_migrates_without_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'complete_candidates.csv').write_text('ad_id,platform,advertiser,recorded_at_utc,source_url,likes\nFB-1,Facebook,Brand,2026-01-01T00:00:00Z,https://facebook.com/x,0\n')
            ads,snaps=migrate_legacy(p)
            self.assertEqual(len(ads),1);self.assertEqual(len(snaps),1)
            self.assertEqual(snaps[0]['likes_exact'],'0')
            self.assertEqual(len(AD_FIELDS),len(set(AD_FIELDS)))
            self.assertEqual(len(SNAPSHOT_FIELDS),len(set(SNAPSHOT_FIELDS)))

if __name__=='__main__':unittest.main()
