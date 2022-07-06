# sockdrawer
Implementation of REST API sock drawer

## Setup
These steps are for a POSIX system. 
First up is to clone the repository:
```
git clone https://github.com/aecollier/sockdrawer.git
cd sockdrawer
```

Create a virtual environment to install dependencies in and activate it (ensure virtualenv is installed first):
```
virtualenv socksenv
source socksenv/bin/activate
```

Then install the dependencies:
```
pip install -r requirements.txt
```

Once pip has finished downloading the dependencies:
```
python3 manage.py runserver
```

And then navigate to `http://127.0.0.1:8000/sock/` and test other endpoints from there!
The "sock" directory contains the bulk of my code. You'll find most of the API implementation in "views.py", although "models.py", "serializers.py", and "urls.py" have been created as well. 
