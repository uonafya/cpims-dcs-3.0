# Codeblocks CPIMS DCS Upgrade

<p align="center">
<a href="https://github.com/uonafya/cpims-ovc-3.0/tree/Codeblock-Lead-WalterBanda-0712908255">
    <img src="https://img.shields.io/badge/Built%20by%20Codeblocks%20-black?style=for-the-badge&logo=django"
         alt="Built By"> </a>
     <a href="https://github.com/uonafya/cpims-ovc-3.0/tree/Codeblock-Lead-WalterBanda-0712908255/wiki"><img src="https://img.shields.io/badge/Wiki%20%F0%9F%93%9C%20-black?style=for-the-badge&logo=django"
         alt="Project Wiki"></a>
     <img src="https://img.shields.io/badge/Version-4.0.2-blue?style=for-the-badge&logo=django&labelColor=black"
         alt="Django Version">
     <img src="https://img.shields.io/github/license/uonafya/cpims-ovc-3.0?style=for-the-badge&logo=github&logoColor=white&labelColor=black"
         alt="License">
</p>

## Who we are 😊

`Codeblocks` are a group formed in the recent HealthIt Hackathon hosted at Kabarak University.

We were responsible in the upgrade of the CPIMS from `python 2.7 to python 3.9` and upgrade of django from `django 1.8 to django 4.0.2`.

## Tasks worked on ⚒
We worked on cpims-ovs and cpims-dcs repositories. The main tasks undertaken was the syntax upgrade from python 2 to python 3. 

We worked on the cpims-ovc-forms and cpims-dcs-main. The individual changes made on the modules can be found on our [wiki](). 

Below is the list of few changes made on our modules.

`CPIMS-OVC-forms :` 

    - [x] Syntax upgrade on the Models, views, forms and urls
    - [x] Writing of 
    
`CPIMS-DCS-main :` 

    - [x] Syntax upgrade on the Models, views, forms and urls
    - [x] Writing of tests

## Guide 🗺
### Installation
The requirements for this project is python and pip

One the requirements are installed, you can setup a virtual environment using `venv`
```shell
$ pip install virtualenv
```

On **Success** you have to create a virtual environment with python 3.9 
```shell
$ python3 venv .env

$ source .env/bin/activate
```

When the virtual environment is created, you can install the required packages using 
```shell
$ pip install -r ./requirements/all.txt
```

`⚠` 🚧 This project is under active development so the starting the django server may fail.

### Project Setup 👶
To start one has to make `migrations`
```shell
$ python manage.py makemigrations
```

Then migrate 
```shell
$ python manage.py migrate
```

`🎉` You can start the dev server now and start contributing

### Running the Dev Server 🖥
To run the dev server 
```shell
$ python manage.py runserver
```

### Running your Tests 🧪
To run tests
```shell
$ python manage.py test
```

## License
This Project is under the [`Apache`](https://choosealicense.com/licenses/) License
## Contributors

1. [Emmanual Changole](https://github.com/EmmanuelChangole)
2. [Walter Banda](https://github.com/WalterBanda)
3. [Amos Kipyegon](https://github.com/Amos-Ditto)
4. [Joseph Karanja](https://github.com/joe052)
5. [Isaiah Mwinga](https://github.com/izzoh-ade)
