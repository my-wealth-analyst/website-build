# website-build

#### Installation
You will need to install python on your computer to run the server locally. This is just during the development of the website. In production, the cloud server will run python and it will operate like any website through your browser.

 Windows:
 i) download Python 3.7.3 from https://www.python.org/downloads/
 ii) open command prompt (CMD) to the 'website-build' root folder (the folder with a file called 'requirements.txt' in it)
 iii) enter this command in CMD >>              'pip install -r requirements.txt'     (without the quotes)

#### Running the development server
You can think of the dev server as the 'brains' of the back-end. The website isn't static, so it needs something running the logic in the background.
To run the dev server, do the following:

Windows:
i) open command prompt (CMD) to: "Website-Built > mywealthanalyst_django" (the folder with a file called 'manage.py' in it)
ii) enter this command in CMD >>             'python manage.py runserver' (without the quotes)
iii) open your browser and type in this URL:          http://localhost:8000/




#### The production server
The production server runs on a DigitalOcean cloud server, details:
Droplet name: mywealthanalyst
IP Address: 104.248.152.99
Username: root
Password: mywealthanalyst_admin

Postgres database details:
Database name: mywealthanalyst
username: admin
password: admin



#### Django admin back end
To access the database back end, go to http://localhost:8000/admin

email: admin@admin.com
password: admin
AlphaVantage API key: M4TA2P8B2OU22SPC
