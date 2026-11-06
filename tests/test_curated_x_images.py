"""Regression checks for curated X image date provenance."""
import importlib.util, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import collect_other_platforms as collector

class CuratedImageTests(unittest.TestCase):
    def source(self):
        return dict(platform='X',url='https://x.com/brand/status/123',
                    media_url='https://pbs.twimg.com/media/example?format=webp&name=large',
                    publication_date_source='original_ui_exact_date',
                    published_date='2025-02-10',publication_label='5:36 AM · Feb 10, 2025',
                    ui_observed_at_utc='2026-01-01T00:00:00Z',caption='Buy this product')

    def collect(self,source):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(collector,'fetch',return_value=(b'RIFFtestWEBP','image/webp')), patch.object(collector.yt_dlp,'YoutubeDL',side_effect=AssertionError('Image route must not follow CTA links')):
                collector.run({'sources':[source]},d)
            rows=json.loads((Path(d)/'candidates.json').read_text())
            report=json.loads((Path(d)/'latest_run.json').read_text())
            return rows,report

    def test_explicit_ui_date_retains_timezone_uncertainty(self):
        rows,_=self.collect(self.source())
        self.assertEqual(rows[0]['published_date'],'2025-02-10')
        self.assertIn('timezone_unspecified',rows[0]['date_status'])
        self.assertIn('timezone unspecified',rows[0]['publication_evidence'])
        self.assertEqual(rows[0]['media_path'],'media/X_123.webp')

    def test_label_date_disagreement_is_rejected(self):
        s=self.source();s['published_date']='2025-02-11'
        rows,report=self.collect(s)
        self.assertEqual(rows,[])
        self.assertIn('disagrees',report['events'][0]['error'])

    def test_missing_observation_timestamp_is_rejected(self):
        s=self.source();s.pop('ui_observed_at_utc')
        rows,report=self.collect(s)
        self.assertEqual(rows,[])
        self.assertEqual(report['events'][0]['status'],'failed')
