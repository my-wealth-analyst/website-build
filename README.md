# website-build

#### Installation
You will need to install python on your computer to run the server locally. This is just during the development of the website. In production, the cloud server will run python and it will operate like any website through your browser.


 Windows:
 
 i) download Python 3.7.3 from https://www.python.org/downloads/
 
 ii) open command prompt (CMD) to the Website-Built root folder
 
 iii) enter this command in CMD >>              pip install -r requirements.txt
 
 

 Linux:
 
 i) open terminal to the Website-Built root folder
 
 ii) enter this command in terminal >>              pip install -r requirements.txt
 



#### Running the development server
You can think of the dev server as the 'brains' of the back-end. The website isn't static, so it needs something running the logic in the background.
To run the dev server, do the following:


Windows:

i) open command prompt (CMD) to: "Website-Built > mywealthanalyst_django"

ii) enter this command in CMD >>             python3 manage.py runserver

iii) open your browser and type in this URL:          http://localhost:8000/



Linux:

i) open terminal to: "Website-Built > mywealthanalyst_django"

ii) enter this command in terminal >>             python manage.py runserver

iii) open your browser and type in this URL:          http://localhost:8000/



#### The production server
Eventually the backend python code will be running 24/7 on a cloud server (Amazon AWS, DigitalOcean, Google Cloud, etc.).
A domain name (e.g. 'www.xyz.com') will need to be registered.

Then, users will type in http://www.xyz.com and will be served the website content exactly as in the development server  



#### Django admin back end
To access the database back end, go to http://localhost:8000/admin

username: admin

password: mywealthadmin

