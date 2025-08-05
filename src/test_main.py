import unittest
import os
import shutil
import sys
from main import main

class TestMainWithBasepath(unittest.TestCase):
    def setUp(self):
        os.makedirs("content", exist_ok=True)
        os.makedirs("static", exist_ok=True)
        with open("content/index.md", "w") as f:
            f.write("# Index Title\n[Link](/about)")
        with open("static/style.css", "w") as f:
            f.write("body { color: blue; }")
        with open("template.html", "w") as f:
            f.write('<html><head><title>{{ Title }}</title><link href="/style.css"></head><body>{{ Content }}</body></html>')
        if os.path.exists("public"):
            shutil.rmtree("public")

    def test_basepath(self):
        sys.argv = ["main.py", "/Static-Site-Generator/"]
        main()
        with open("public/index.html") as f:
            content = f.read()
        self.assertIn('href="/Static-Site-Generator/about"', content)
        self.assertIn('href="/Static-Site-Generator/style.css"', content)
        self.assertIn("<title>Index Title</title>", content)
        self.assertTrue(os.path.exists("public/style.css"))

    def test_default_basepath(self):
        sys.argv = ["main.py"]
        main()
        with open("public/index.html") as f:
            content = f.read()
        self.assertIn('href="/about"', content)
        self.assertIn('href="/style.css"', content)
        self.assertIn("<title>Index Title</title>", content)

if __name__ == "__main__":
    unittest.main()