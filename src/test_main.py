import unittest
import os
import shutil
from main import main

class TestMain(unittest.TestCase):
    def setUp(self):
        os.makedirs("static", exist_ok=True)
        os.makedirs("content", exist_ok=True)
        with open("static/test.css", "w") as f:
            f.write("body { color: blue; }")
        with open("content/index.md", "w") as f:
            f.write("# Test Title\nSome content")
        with open("template.html", "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

    def test_main(self):
        main()
        self.assertTrue(os.path.exists("public/test.css"))
        self.assertTrue(os.path.exists("public/index.html"))
        with open("public/index.html") as f:
            content = f.read()
        self.assertIn("<title>Test Title</title>", content)
        self.assertIn("<p>Some content</p>", content)