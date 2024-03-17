# Portfolio
Flask portfolio created during Python course (The Complete Python Developer - zerotomastery.io)

# Installation
Install in virtual environment using following commands:
```shell
git clone https://github.com/CodeByAlejandro/Portfolio.git
cd Portfolio
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

# Local usage
## Environmental variables
Create `.env` file in project dir with following config:
```shell
export GOOGLE_APP_PASSWORD='google_app_passw_here'
```
Source this `.env` file:
```shell
. .env
```
## Local startup
You can start a local Flask server in debug mode with the following command:
```shell
./start_flask.sh
```
or start it yourself using:
```shell
flask --app server.py run --debug
```
> [!NOTE]
> Debug mode is usefull when working on the code, since it will automatically refresh the server on code changes.
Alternatively you can also start the Flask server from the python module itself by adding the following code:
```python
from socket import gethostname
[...]

if __name__ == '__main__':
    # Do whatever initialization you need here, e.g. `db.create_all()`
    if 'liveconsole' not in gethostname():
        app.run()
```
The clever little if is needed for compatibility with pythonanywhere as it will check if the Flask server is started from pythonanywhere

# Local uninstall
# Uninstall
Deactivate the virtual environment using the exported shell function `deactivate`:
```shell
deactivate
```
Remove the project:
```shell
cd ..
rm -rf Portfolio
```

# Configuration required for `Pythonanywhere`
## Environmental variables
Create `.env` file in project dir with following config:
```shell
export GOOGLE_APP_PASSWORD='google_app_passw_here'
```

This is the google app password for CodeByAlejandro@gmail.com and is needed to allow mailing through this account.

> [!NOTE]
> The Python source code only cares about the existence of the environmental variable, it does not care how it is created.

## WSGI server configuration
```python
# +++++++++++ ENV +++++++++++
# Set my own custom environmental variables for my web-app
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/Portfolio')
load_dotenv(os.path.join(project_folder, '.env'))

# +++++++++++ FLASK +++++++++++
# Flask works like any other WSGI-compatible framework, we just need
# to import the application.  Often Flask apps are called "app" so we
# may need to rename it during the import:
#
#
import sys
#
## The "/home/CodeByAlejandro" below specifies your home
## directory -- the rest should be the directory you uploaded your Flask
## code to underneath the home directory.  So if you just ran
## "git clone git@github.com/myusername/myproject.git"
## ...or uploaded files to the directory "myproject", then you should
## specify "/home/CodeByAlejandro/myproject"
path = '/home/CodeByAlejandro/Portfolio'
if path not in sys.path:
    sys.path.append(path)

from server import app as application  # noqa
#
# NB -- many Flask guides suggest you use a file called run.py; that's
# not necessary on PythonAnywhere.  And you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.
```
