import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        result = self.client.get("/")
        self.assertNotIn(b"123 Magic Unicorn Way San Francisco, CA", result.data)
        self.assertIn(b"Please RSVP", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertIn(b"123 Magic Unicorn Way", result.data)
        self.assertNotIn(b"Please RSVP", result.data)
        print("FIXME")


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        result = self.client.get("/games")
        self.assertIn(b"Connect Four", result.data)


if __name__ == "__main__":
    unittest.main()
