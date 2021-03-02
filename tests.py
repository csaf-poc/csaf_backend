import copy
from dictdiffer import patch
import json
import unittest

from app import create_app, db
from app.models.advisory import Advisory
from app.models.audit_trail import AuditRecord
from config import Config


class TestConfig(Config):
    TESTING = True
    MONGODB_DB = 'csaf_advisory_db'
    MONGODB_USERNAME = None
    MONGODB_PASSWORD = None
    MONGODB_HOST = 'mongomock://localhost:27017/csaf_advisory_db'
    MONGODB_PORT = 27017


class AdvisoryAPITestCase(unittest.TestCase):

    sample_advisory = {
        "document":{
            "csaf_version":"2.0",
            "title":"Minimal Advisory",
            "publisher":{
                "type":"discoverer"
            },
            "type":"Example",
            "tracking":{
                "current_release_date":"2020-12-31T00:00:00Z",
                "id":"Example Document",
                "initial_release_date":"2020-12-31T00:00:00Z",
                "revision_history":[
                    {
                        "number":"1",
                        "date":"2020-12-31T00:00:00Z",
                        "summary":"Summary of Example Advisory"
                    }
                ],
                "status":"draft",
                "version":"1"
            }
        }
    }

    def setUp(self):
        self.app = create_app(TestConfig)
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.connection.drop_database(TestConfig.MONGODB_DB)
        self.app_context.pop()

    def test_create_advisory(self):
        # Create advisory
        resp = self.test_client.post('/api/advisories', json=self.sample_advisory)
        data = json.loads(resp.data)
        assert str(Advisory.objects.first().id) == data.get('_id')

    def test_audit_trail(self):
        # Create advisory
        resp = self.test_client.post('/api/advisories', json=self.sample_advisory)
        data = json.loads(resp.data)
        a_id = data.get('_id', '')
        # Update advisory
        updated_advisory = copy.deepcopy(self.sample_advisory)
        updated_advisory['document']['title'] = 'Updated Advisory'
        updated_advisory['document']['tracking']['version'] = '2'
        self.test_client.put('/api/advisories/{}'.format(a_id), json=updated_advisory)
        # Delete advisory
        self.test_client.delete('/api/advisories/{}'.format(a_id))
        # Get audit trail
        resp = self.test_client.get('/api/advisories/{}/trail'.format(a_id))
        data = json.loads(resp.data)
        audit_records = data.get('_items', [])
        # Restore advisory versions
        v1_advisory = patch(audit_records[1]['_diff'], {})
        assert v1_advisory == self.sample_advisory, 'Initial (v1)'
        v2_advisory = patch(audit_records[2]['_diff'], v1_advisory)
        assert v2_advisory == updated_advisory, 'Updated (v2)'
        v3_advisory = patch(audit_records[3]['_diff'], v2_advisory)
        assert v3_advisory == {}, 'Deleted (v3)'


if __name__ == '__main__':
    unittest.main(verbosity=2)
