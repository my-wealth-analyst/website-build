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
Eventually the backend python code will be running 24/7 on a cloud server (Amazon AWS, DigitalOcean, Google Cloud, etc.).
A domain name (e.g. 'www.xyz.com') will need to be registered.

Then, users will type in http://www.xyz.com and will be served the website content exactly as in the development server  



#### Django admin back end
To access the database back end, go to http://localhost:8000/admin

username: admin

password: mywealthadmin

AlphaVantage API key: M4TA2P8B2OU22SPC

### Current Functionality (as at 14May 2019)
- Django core configured
- Charting functionality complete with selectable time-bounds (e.g. 3months, 1yr,5yrs,10yrs,all) (requires aesthetic review)
- Current prices functionality complete (requires aesthetic review)
- Landing page (draft - requires aesthetic review)
- Header bar (draft - requires aesthetic review)
- Auto-retrieval of data from perthmint website for Gold and Silver. Only pulls data up to the end of the last month.
     - TO-DO: find source for last 30 days prices

### Current Functionality (as at 17May 2019)
Stage 1 revisions completed:
- chart layout revised in line with comments
- charts now include recession indicators, and horizontal overvalue/undervalue lines
- live data pulling from 'https://www.marketindex.com.au/' and 'https://coinmarketcap.com/currencies/bitcoin/' and 'https://www.alphavantage.co/' (for AUD/USD) completed. These will run once per hour (in production).
- aesthetic comments incorporated
