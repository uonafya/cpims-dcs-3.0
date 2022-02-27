from urllib import response
import pandas as pd

from django.test import TestCase


writer = pd.ExcelWriter('sales_summary.xlsx', engine='xlsxwriter')
data = pd.read_csv('input.csv')
data.to_excel(writer, sheet_name='mysheet', index=False)
workbook = writer.book
workbook.filename = 'sales_summary.xlsm'
workbook.add_vba_project('vbaProject.bin')
writer.save()

# Create your tests here.

class URLTests(TestCase):
    def test_reports(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
