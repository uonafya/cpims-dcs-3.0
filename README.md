# CPIMS DCS Workflow

Code base for Child Protection Management Information System (CPIMS) DCS business process

## Technology stack
Python - 3.10\
Django - 4.2.0\
Postgresql - 16


## Functionality
### Existing
Register Org Unit, Workforce, CHV, Caregiver(s), OVC\
Register a case using Case Record Sheet
Manage cases - Summons, courts, case closure
Instition care
Alternative care
Statutory Institution care


## Installation

git clone https://github.com/uonafya/cpims-dcs-3.0 
Edit cpims/settings.py with your credentials\

python manage.py makemigrations\
python manage.pt migrate\
python manage.py check\
python manage.py runserver
