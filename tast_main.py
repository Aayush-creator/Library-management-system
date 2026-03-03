import unittest
import json
import os

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": {}, "movies": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

class TestCineVault(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "users": {"testuser": "testpass"},
            "movies": [
                {"title": "Inception", "genre": "Sci-Fi",
                 "year": 2010, "rating": 9.0, "added_by": "testuser"},
                {"title": "Titanic", "genre": "Romance",
                 "year": 1997, "rating": 8.5, "added_by": "testuser"}
            ]
        }
        save_data(self.test_data)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_load_data(self):
        data = load_data()
        self.assertIn("users", data)
        self.assertIn("movies", data)

    def test_save_data(self):
        test_data = {"users": {"john": "1234"}, "movies": []}
        save_data(test_data)
        data = load_data()
        self.assertEqual(data["users"]["john"], "1234")

    def test_login_correct_password(self):
        data = load_data()
        result = "testuser" in data["users"] and data["users"]["testuser"] == "testpass"
        self.assertTrue(result)

    def test_login_wrong_password(self):
        data = load_data()
        result = "testuser" in data["users"] and data["users"]["testuser"] == "wrongpass"
        self.assertFalse(result)

    def test_register_new_user(self):
        data = load_data()
        data["users"]["newuser"] = "newpass"
        save_data(data)
        data = load_data()
        self.assertIn("newuser", data["users"])

    def test_duplicate_username(self):
        data = load_data()
        already_exists = "testuser" in data["users"]
        self.assertTrue(already_exists)

    def test_add_movie(self):
        data = load_data()
        data["movies"].append({
            "title": "Avatar",
            "genre": "Sci-Fi",
            "year": 2009,
            "rating": 8.0,
            "added_by": "testuser"
        })
        save_data(data)
        data = load_data()
        titles = [m["title"] for m in data["movies"]]
        self.assertIn("Avatar", titles)

    def test_delete_movie(self):
        data = load_data()
        data["movies"].pop(0)
        save_data(data)
        data = load_data()
        titles = [m["title"] for m in data["movies"]]
        self.assertNotIn("Inception", titles)

    def test_search_movie(self):
        data = load_data()
        keyword = "inception"
        results = [m for m in data["movies"]
                  if keyword in m["title"].lower()
                  or keyword in m["genre"].lower()]
        self.assertEqual(len(results), 1)

    def test_empty_movies_list(self):
        data = load_data()
        data["movies"] = []
        save_data(data)
        data = load_data()
        self.assertEqual(len(data["movies"]), 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
