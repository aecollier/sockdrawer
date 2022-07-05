# sockdrawer
Implementation of REST API sock drawer

## Setup
First up is to clone the repository:
'''
git clone https://github.com/aecollier/sockdrawer.git
cd sockdrawer
'''

Create a virtual environment to install dependencies in and activate it:
'''
virtualenv socksenv
source socksenv/bin/activate
'''

Then install the dependencies:
'''
(socksenv)$ pip install -r requirements.txt
'''

Note the (socksenv) in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv.

Once pip has finished downloading the dependencies:
'''

(socksenv)$ cd sockdrawer
(socksenv)$ python manage.py runserver
'''

And then navigate to `http://127.0.0.1:8000/sock/` and test other endpoints from there!
