# ProjectsAutomation Service

This project automates the process of Dvmn project teams creation.  
You can install and run it on your local machine or use preconfigured [Heroku app](http://blooming-stream-71357.herokuapp.com/admin)


![Screenshot](Screenshot.png)

## Installation
1. Clone project
```bash
git clone https://github.com/gennadis/dvmn_teams.git
cd dvmn_teams
```

2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Rename `.env.example` to `.env` and fill your secrets in it.  
Important! Place `.env` in `dvmn_teams` folder.


5. Migrate
```bash
python manage.py migrate
```

6. Create Django superuser
```bash
python manage.py createsuperuser
```

7. Create and import fake fixtures if needed  
50 students and 2 PM will be generated and added to a database.
```bash
python manage.py makefakes
python manage.py loaddata students.json pms.json timeslots.json
```

8. Make empty teams for PMs and students  
Generated teams will contain:  
- PM
- Timeslot
- Group level
- No students
```bash
python manage.py maketeams
```

9. Run gunicorn web server
```bash
gunicorn dvmn_teams.wsgi
```

10. Run telegram bot
```bash
python manage.py telebot
```

## Usage
1. Open admin panel  
Open app in browser [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

2. Add yourself as a Student to test the bot  
Make sure to enter your real Telegram `@username`, otherwise bot won't recognize you as a student.

3. Start using bot by typing `/start` command
