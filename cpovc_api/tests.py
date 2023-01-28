# from django.test import TestCase
import requests
# from django.utils.timezone import utc
# Create your tests here.

# default=datetime.datetime(2019, 8, 23, 17, 59, 40, 153036, tzinfo=utc)

url = 'http://localhost:8004/api/v1/crs/'
# url = 'https://test.cpims.net/api/v1/crs/'
# url = 'http://childprotection.go.ke/api/v1/crs/'
headers = {'Authorization': 'Token 330764ede3eb59acca76b8f064b84eb477ff452e'}

data = {"county": "001", "constituency": "001", "case_category": "CDIS",
        "child_dob": "2010-06-15", "perpetrator": "PKNW",
        "child_first_name": "Susan", "child_surname": "Atieno",
        "case_landmark": "Near kiroboto primary",
        "case_narration": "Child was abducted", "child_sex": "SMAL",
        "reporter_first_name": "Mark", "reporter_surname": "Masai",
        "reporter_telephone": "254722166058",
        "reporter_county": "001", "reporter_sub_county": "001",
        "case_reporter": "CRSF", "organization_unit": "Helpline",
        "hh_economic_status": "UINC", "family_status": "FSUK",
        "mental_condition": "MNRM", "physical_condition": "PNRM",
        "other_condition": "CHNM", "risk_level": "RLMD",
        "case_date": "2019-10-14",
        "perpetrators": [{"relationship": "RCPT", "first_name": "James",
                          "surname": "Kamau", "sex": "SMAL"}],
        "caregivers": [{"relationship": "CGPM", "first_name": "Mama",
                        "surname": "Atieno", "sex": "SMAL"}],
        "case_details": [{'category': 'CIDS',
                          'place_of_event': 'PEHF',
                          'date_of_event': '2019-09-01',
                          'nature_of_event': 'OOEV'}]}

data = {'hh_economic_status': 'UINC', 'child_sex': 'SFEM', 'case_reporter': 'CRSF', 'physical_condition': 'no', 'case_date': '2020-09-13', 'reporter_first_name': 'Leonard', 'county': '047', 'reporter_county': '047', 'reporter_surname': 'mbugua', 'perpetrators': [{'first_name': '', 'surname': '', 'relationship': '', 'sex': 'SMAL'}], 'other_condition': 'CHNM', 'risk_level': 'RLMD', 'perpetrator': 'PKNW', 'mental_condition': 'MNRM', 'family_status': 'FSUK', 'case_narration': u"Leonard mbugua from nairobi county, kasarani sb county in ruai ward called the line with number 704241274 to say her neighbour  Tabitha Nyokabi age 17 years has been physically assaulted by her step father Antony wanjohi. her mothers name is Leah wangui. she says sometimes he makes sexual advances towards her. she has tried telling her mother about the incident and all she does is talk to him but does not chase him out of their home. she says she had reported the matter to the police station he was arrested and released on the same day. she was asking for assistance and she was referred to the chiefs office and the children's office", 'organization_unit': 'Helpline', 'caregivers': [{'first_name': 'Leah', 'surname': 'wangui', 'relationship': 'CGPM', 'sex': 'SMAL'}], 'reporter_sub_county': '280', 'case_details': [{'category': 'CSNG', 'place_of_event': 'PEHF', 'date_of_event': '2020-09-13', 'nature_of_event': 'OOEV'}], 'child_surname': 'wangui', 'reporter_telephone': '704241274', 'case_category': 'CSNG', 'case_landmark': 'st john primary', 'child_first_name': 'Leah', 'constituency': '280', 'child_dob': '2020-09-13'}

response = requests.post(url, json=data, headers=headers)
# data = {"case_id": "64d2a692-ef3c-11e9-98c6-d4258b5a3abb"}
# response = requests.get(url, params=data, headers=headers)

# print (response)
print('==' * 50, 'HEADERS', '==' * 50)
print (response.headers)
print ('\n')
print('==' * 50, 'CONTENT', '==' * 50)
print (response.content)

'''
case_id = 'f6e09348-c5d2-11e9-9018-d4258b5a3abb'
response = requests.get(url, params={"case_id": case_id}, headers=headers)

print (response)
print (response.headers)
print (response.content)
'''
