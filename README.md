
<h1 align="center">CPIMS upgrade by incognito 👋</h1>
<p align="center">

  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> 
    <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>

</p>

<p><b>Incognito is a group comprising four members formed during the HealthIT Hackathon at Kabarak University and their primary task was upgrading `cpims-dcs-3.0` to python 3.10 and django 4.0.2</b></p>


### 📝 Tasks done by incognito

1. python 2.7 to 3.10.0 
> we used an online python 2 to o 3 converter [python2to3.com](https://www.python2to3.com) for every python file it converted the .py files to python3 syntax
2. django 1.8 to 4.0.2 <br />
> we used ```django-upgrade``` library for converting files from django 1.8 to 4.0.2 here is a link to [django-upgrade](https://github.com/adamchainz/django-upgrade) with detailed instructions
3. Added ``on_delete=models.CASCADE`` to ``ForeignKey`` and ``OneToOneField`` and used pycharm's ReGex capabilities for faster lookup:

```sh 
    -models.ForeignKey("auth.User")
    +models.ForeignKey("auth.User", on_delete=models.CASCADE)

    -models.OneToOneField("auth.User")
    +models.OneToOneField("auth.User", on_delete=models.CASCADE)
```
    
4. changed templates staticfiles to static <br />

```sh
    -{% load staticfiles %}
    +{% load static %}
```
5. commented is_allowed_groups due to complexity of decorators.py <br />
6. used default django backends auth instead of the cpims middleware <br />
    
```sh
    -AUTHENTICATION_BACKENDS = ['cpovc_auth.backends.CPOVCAuthenticationBackend']
    +AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

```
7. updated requirements.txt
```sh 
pip freeze
```

8. wrote tests for cpovc_offline_mode and used ```coverage``` to see the percentage coverage of our tests
```shell
pip install coverage
coverage run manage.py test cpims.tests.tests_urls -v 3
```

## 🚀 Usage

Make sure you have [python 3.10](https://www.python.org/getit/) and [postgreSQL](https://www.postgresql.org/) installed

#### Installation
    clone the repository to your local machine
    git clone https://github.com/uonafya/cpims-dcs-3.0

Just run the following command at the root of your project:

#### install virtualenv windows

    pip install virtualenv

#### create virtualenv

    virtualenv venv

#### activate virtualenv

    venv\Scripts\activate

##### install requirements

    pip install -r requirements.txt

##### initialize db

    py manage.py makemigrations 
    py manage.py migrate
    py manage.py createsuperuser
    py manage.py runserver



## Code Contributors

This upgrade exists thanks to the people who contributed.

👤 **Vivian Atieno Ouma**

- Phone: +254705412563
- Gmail: atienooumavee@gmail.com
- Github: [github.com/Atieno-Ouma](https://github.com/Atieno-Ouma)

👤 **Ivan Toroitich Bowen**

- Phone: +254791440095
- Gmail: bowenivan16@gmail.com
- Github: [github.com/874bowen](https://github.com/874bowen)

👤 **Shem Miriam Wanjiru**

- Phone: +254714660411
- Gmail: shemmiriam@gmail.com
- Github: [Shem Miriam](https://github.com/shemmiriam)

👤 **Rebecca Cheptoek Kibet**

- Phone: +254759669534
- Gmail: rebbytoek095@gmail.com
- Github: [Rebecca Cheptoek](https://github.com/Rebeccacheptoek)
## 🤝 Contributing

Contributions, issues and feature requests are welcome.<br />
Feel free to check [cpims]( https://github.com/uonafya/cpims-ovc-3.0) if you want to contribute.<br />


