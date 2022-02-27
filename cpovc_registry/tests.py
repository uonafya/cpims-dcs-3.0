from django.test import TestCase
from datetime import datetime
import unittest

# Create your tests here.



start_date = '2002-01-01'
fmt = '%Y-%m-%d'

new_date = datetime.strptime(start_date, fmt)
todate = datetime.now()

print(new_date)

class Test_Login(unittest.TestCase):

    def test_clean_username(self):
        response = self.cleaned_data['username']
        self.assertEqual(username,)

    def test_clean_password(self):
        pass


# class Test_View(TestCase):
#     def test_home(self):
#         test = self.client.get(self,'home')
#         self.assertEqual(test, test.)