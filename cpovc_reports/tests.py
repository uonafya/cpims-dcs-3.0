import pandas as pd
import json
from django.test import TestCase
from django.urls import reverse, resolve
from django.test.client import Client


writer = pd.ExcelWriter('sales_summary.xlsx', engine='xlsxwriter')
data = pd.read_csv('input.csv')
data.to_excel(writer, sheet_name='mysheet', index=False)
workbook = writer.book
workbook.filename = 'sales_summary.xlsm'
workbook.add_vba_project('vbaProject.bin')
writer.save()

# urls tests



