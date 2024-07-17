import unittest
import os

os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Heet Shah</title>" in html

        # TODO: Add more tests relating to the home page
        assert "<h1>Heet Shah</h1>" in html
        assert "<header class=\"nav-bar\">" in html


    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert 'timeline_posts' in json
        assert len(json['timeline_posts']) == 0

        # TODO: Add more tests relative to GET and POST apis
        response = self.client.post("/api/timeline_post", data={"name": "Bob Marley", "email": "test@mailing.com", "content": "This is a post from Bob Marley."}) 
        assert response.status_code == 200
        assert response.is_json

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert len(json['timeline_posts']) == 1
        assert json['timeline_posts'][0]['name'] == "Bob Marley"
        assert json['timeline_posts'][0]['email'] == "test@mailing.com"
        assert json['timeline_posts'][0]['content'] == "This is a post from Bob Marley."

        # TODO: Add more tests relating to the timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h2>Timeline</h2>" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

