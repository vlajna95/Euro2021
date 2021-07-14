# Euro 20/21 

A Django project to save matches, teams, phase and group details for the Euro 20/21 (football). 


## Some instructions 

First things first, install the requirements from the provided file. 

```bash
pip install -r requirements.txt
```

Next, create the database with the provided models. Of course, you also need a super user, so create it right after creating the database. 

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

This was a project mainly intended for local usage, so there's no proper static files handling. Anyways, you can get all the static file with the standard command. 

```bash
python manage.py collectstatic
```


Then you can import the data provided in matches app fixtures (JSON format), if you want to see the full project functionality. There are twelve matches (the whole first round of the group phase). 

```bash
python -Xutf8 manage.py loaddata matches
```

**Important:** Use the Python UTF-8 mode in order to avoid encoding problems, I've used some emojis here. :smiley: 


## An additional command 

There's a command provided by the matches app which creates a text file with the syntax I used to fill the description/overview for the match. 

```bash
python manage.py newmatch "12 FRAGER"
```

This will create the file **12 FRAGER.txt** in the root directory and pre-fill it with the default syntax. Try it, it wont do anything to the database. 

**Note:** You must have the 22 player names in your clipboard for this to work, every player in its own line, with no empty lines between the two teams.


## Some random details 

The project and database contents are in serbian, if anybody cares. :grin:
