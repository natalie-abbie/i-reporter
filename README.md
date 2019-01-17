# IReporter
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b46278283303475bb1de7680bc048762)](https://www.codacy.com/app/natalie-abbie/i-reporter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=natalie-abbie/i-reporter&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/natalie-abbie/i-reporter.svg?branch=ft-api-endpoints-163228164)](https://travis-ci.org/natalie-abbie/i-reporter)
[![Coverage Status](https://coveralls.io/repos/github/natalie-abbie/i-reporter/badge.svg?branch=ft-api-endpoints-163228164)](https://coveralls.io/github/natalie-abbie/i-reporter?branch=ft-api-endpoints-163228164)

The iReporter api enables users to register and login to the platform with their correct creditials inorder to report a redf flag or an intervention in line with corruption

## Built with

To get started for the coding you will need to 
* install Flask as our major dependence, 
* pep8 for neat and professional codes,
* pylint to help you around with a few of the errors. 
* python 3.6 as the version to be used. 

### Installation

Here is how to go about installing of the requirements that will be need 
* We shall need to work in a virtual environment so lets go ahead and;
Create a virtual environment for linux users
```
 virtualenv "name of the virtual environment eg venv" (virtualenv venv)
 ```
Then when the virtual environmemt is created, Activate the environment

```
    source "name of the virtual environment eg venv/bin/activate" (source venv/bin/activate)
 ```
 In your Vscode you therefore get to realise its in brackets eg (venv)nataline.......... and when all this is done get to your application directorty if already pushed to github by cloning the repo 
 
 ```
 git clone https://github.com/natalie-abbie/i-report.git 
 cd to the application directory eg cd i-report
 incase its in the branch git checkout branchname
 ```
 After all the dependences are installed in your virtualenv therefore run the command to put the depences in the in the requirements.txt file 
 ```
 pip install >Requirements.txt 
 and to install the dependences again run the below command in your terminal to install all the dependences
 pip install -r Requirements.txt
 ```
 Run the application with:
 ```
 python run.py
 ```

## Running the tests

For running the tests you can either use;
```
pytest
Nose2
test_filename
```

### URL ENDPOINTS for v1 api

| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `api/v1/redflag/<flag_id>` | `GET` | Retrieves a specific redflag by id
|`api/v1/redflag/create_redflag`|`POST`| creates redflag
| `/api/v1/redflag'` | `GET` | Gets all the red flags created by the users
| `api/v1/getuser` | `GET` | Retrieve all users |
| `api/v1/auth/register | `POST` |  registers a new User |
| `api/v1/auth/login` | `POST` |  Logs in a registered user |
| `api/v1/redflag/<flag_id>/location`|`PUT`| Changes the location of a specific  user
| `api/v1/redflag/<flag_id>/description` | `PUT` | changes the description of a specific user |
| `api/v1/redflag/<flag_id>`|`DELETE`| deletes the red of a specific user|
| `api/v1/logout` | `POST` |  Logs out a user |

### USER
An example of how its posted in postman
```
{
    "firstname":"abio",
    "lastname": "natalie",
    "othernames": "talies",
    "username": "natalyn",
   "phonenumber":"0700000000",
    "password": "nats123",
    "email": "nats@gmail.com"
}
```

    "message": "Account created successfully",
    "users": [
        {
            "email": "nats@gmail.com",
            "firstname": "drats",
            "lastname": "natalie",
            "othernames": "talies",
            "password": "pbkdf2:sha256:50000$c1VEQCYo$6afbf7610f70e51a99923db6ef46c9bef7dd10abbb0d7104c1128a31b675a612",
            "phonenumber": "0700000000",
            "registeredOn": "2019-01-17 04:29:16.721806",
            "userid": "8e9348bb-5d53-418f-8bae-153d73f0e98a",
            "username": "natalyn"
        }
    ]
### CREATE REDFLAGS
An example of how its posted in postman
```
{
    "location":"kyanja",
    "type":"corruption",
    "description":"emblezzing money for road construction"
}
```
### RESULT IN POSTMAN 
```
[
      "flags": [
        [
            "dd83ff7e-88e3-44f1-a574-f8d270412231",
            "natalyn"
        ],
        {
            "description": "emblezzing money for road construction",
            "flag_id": "f8e2b2f9-6715-4a0e-b28a-fbe0feb18d76",
            "location": "kyanja",
            "type": "corruption"
        }
    ],
    "message": "flag successfully created"
}
```

## Versioning
```
/api/v1/.....
```

## Authors
Natalie Abbie 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

