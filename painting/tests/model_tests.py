from django.test import TestCase
from functional_tests.factory import paintingFactory


class paintingtest(TestCase):
    def setUp(self):
        self.painting = paintingFactory(title='Lokesh')

    def test_title_to_share_returns_meet_Lokesh__farmer_from_sivaganga_tamil_nadu(self):
        self.assertEqual(self.painting.title_to_share,'Meet Lokesh, farmer from Sivaganga, Tamil Nadu')

    def test_featured_image_returnes_the_image(self):
        self.assertEqual(self.painting.featured_image,self.painting.image)

    def test_to_str_returns_lokesh_sivaganga(self):
        self.assertEqual(str(self.painting),'Lokesh Sivaganga')

    def test_get_absolute_url_return_path_with_paintings_s_painting_page(self):
        self.assertRegexpMatches(self.painting.get_absolute_url(),'/categories/paintings/s/lokesh/?')