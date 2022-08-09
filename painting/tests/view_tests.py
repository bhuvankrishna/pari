from django.test import TestCase
from functional_tests.factory import paintingFactory
from django.test import Client


class paintingListTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.painting = paintingFactory(title='Lokesh')
        self.second_painting = paintingFactory(title='SomeNameOfPerson', location__name='Amravati',
                                       location__slug='45-amravati', location__district='amravati')
        self.third_painting = paintingFactory(title='SomeName', location__name='Aamravati',
                                      location__slug='45-aamravati', location__district='aamravati')

    def test_sub_heading_in_context_should_be_people_from_every_indian_district(self):
        response = self.client.get('/categories/paintings/')
        self.assertEqual(response.context_data['sub_heading'], 'People from every indian district')

    def test_painting_should_come_in_order_of_the_district_names(self):
        response = self.client.get('/categories/paintings/')
        self.assertEqual(response.context_data['paintings'][0].title, 'SomeNameOfPerson')


class paintingDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.first_painting = paintingFactory(title='SomeNameOfPerson', location__name='Amravati',
                                      location__slug='45-amravati', location__district='amravati')
        self.second_painting = paintingFactory(title='SomeName', location__name='Aamravati',
                                       location__slug='45-aamravati', location__district='aamravati')

    def test_painting_should_be_in_order_in_painting_district_page(self):
        response = self.client.get('/categories/paintings/a/')
        self.assertEqual(response.context_data['paintings'][0].title, 'SomeName')

    def test_the_complete_url_to_painting_should_give_all_the_details_of_the_painting(self):
        response = self.client.get('/categories/paintings/a/somename/')
        self.assertEqual(response.context_data['painting'].title, 'SomeName')
