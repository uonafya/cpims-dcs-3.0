# cpims-dcs-3.0
CPIMS DCS upgrade
## files edited by incognito
we upgraded all modules from

    python 2.7 to 3.10.0
    django 1.8 to 4.0.2
    changed templates staticfiles to static
    commented is_allowed_groups
    used default django backends auth instead of the cpims middleware
    updated requirements.txt

#### install python 3.10 https://www.python.org/getit/
#### Installation
    clone the repository to your local machine
    git clone https://github.com/uonafya/cpims-dcs-3.0

#### install virtualenv windows

    pip install virtualenv

#### create virtualenv

    virtualenv venv

#### activate virtualenv

    venv\Scripts\activate

##### install requirements

    pip install -r requirements.txt