import unittest

from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    

class VulnerabilityModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create(self):
##        vuln = VulnerabilityModel()
##        vuln.from_dict(
##            {
##                'scores': None
##            }
##        )
##        self.assertEqual(vuln.scores, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
