import unittest
from app import app

class TestApp(unittest.TestCase):

  # Ensure that Flask was set up correctly
  def test_index(self):
    tester = app.test_client(self)
    response = tester.get('/', content_type="html/text")
    self.assertEqual(response.status_code, 200)

  # Ensure that the index page loads correctly
  def test_index_page_loads(self):
    tester = app.test_client(self)
    response = tester.get('/', content_type="html/text")
    self.assertTrue(b'Latest Posts' in response.data)

  # Ensure posts load correctly
  def test_posts_load(self):
    tester = app.test_client()
    response = tester.get('/', content_type="html/text")
    self.assertIn(b'7 Python mistakes all beginner developers make', response.data)

  # Ensure login behaves correctly given correct credentials
  def test_correct_login(self):
    tester = app.test_client()
    response = tester.post('/login', data=dict(email='a', password='a'), follow_redirects = True)
    self.assertIn(b'Latest Posts', response.data)

  # Ensure login behaves correctly given incorrect credentials
  def test_incorrect_login(self):
    tester = app.test_client()
    response = tester.post('/login', data=dict(email='b', password='b'), follow_redirects = True)
    self.assertIn(b'No such user or wrong password.', response.data)

  # Ensure logout behaves correctly
  def test_logout(self):
    tester = app.test_client()
    tester.post('/login', data=dict(email='a', password='a'), follow_redirects = True)
    response = tester.get('/logout', follow_redirects = True)
    self.assertIn(b'SIGN UP', response.data)

  # Ensure that the post details page requires login
  def test_postdetail_page_requires_login(self):
    tester = app.test_client(self)
    response = tester.get('/post/1', follow_redirects = True)
    self.assertTrue(b'LOG IN' in response.data)
  
  # Ensure that the profile page requires login
  def test_profile_page_requires_login(self):
    tester = app.test_client(self)
    response = tester.get('/myprofile', follow_redirects = True)
    self.assertTrue(b'LOG IN' in response.data)

if __name__ == '__main__':
  unittest.main()