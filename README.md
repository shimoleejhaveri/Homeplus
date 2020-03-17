# <img src="https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/logo1.svg" width="10%" alt="JobTracker">
Home+ is a personalised user dashboard that is designed to help the users manage all their daily used apps in one place. It is built using Python as the backend language, and HTML and JavaScript as the frontend languages. The database is built in PostgreSQL, and the UI is designed using CSS and Bootstrap.

## About Me
Before becoming a software engineer, Shimolee worked as an attorney at a leading law firm in India. After moving to the US in 2017, she joined Casetext, a company that builds its own AI to provide contextual legal search results. Working there made her realize that she wanted to be a part of the engineering process itself, thereby inspiring her to join the Hackbright Academy. During her time at Hackbright, she found that the skills that she had acquired as an attorney, such as being adaptable, detail-oriented, and logical thinking, have been most transferable and useful. She enjoys programming because it allows her to experiment with and build solutions to complex problems with a very structured thought process, and learn new ways of solving the same problem.

## Deployment
http://homeplusbeta.com/

## Contents
* [Tech Stack](#tech-stack)
* [APIs](#api)
* [Features](#features)
* [Future State](#future)
* [Installation](#installation)

## <a name="tech-stack"></a>Tech Stack
* Bootstrap
* CSS3
* Flask
* HTML5
* JavaScript (AJAX, Chart.js, jQuery, Toast UI)
* Jinja2
* JSON
* PostgreSQL
* Python
* SQLAlchemy ORM

## <a name="api"></a>APIs
* Alpha Vantage API
* Google Calendar API
* News API

## <a name="features"></a>Features

#### Landing Page
This is the landing page for the website for user login or registration. The forms are built using HTML, and the form inputs are retreived using Flask to send them to the database via SQLAlchemy to be stored.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/Home%20page%20-%3E%20Register.gif "Home+ Landing Page")

#### Active User Dashboard
Once signed in, the user can view the entire dashboard. Home+ has four distinct features that use different functionalities: collaborative to-do lists, latest news, stock information, and calendar.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/Login%20-%3E%20User%20Dashboard.gif "Home+ Active User Dashboard")

#### To-Do List: Add/Remove a List
This feature is connected to the database wherein all the user’s personal information is stored. Users can add new tasks or remove existing tasks from the to-do list feature. The process of adding a new list is similar to the user registration/login one, and the form inputs are saved to the database under the user's unique user ID. List deletion is accomplished using jQuery to create an event handler and listener for each unique list ID. When the "close" button is clicked, it sends a POST request to the Flask endpoint connected with removing a list from the database.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/Add%20:%20Remove%20List.gif "Home+ Add/Remove List")

#### To-Do List: Share a List
Users can also share to-do lists with an existing user of the dashboard. A shared lists table exists in the database that stores the IDs of the user sharing the list and the user that the list has been shared with. In order to allow simultaneous collaboration on one list by two or more users, the shared lists table is queried by running the SQLAlchemy code in Python to display information only to the users that the list has been shared with.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/Share%20List.gif "Home+ Share A List")

#### To-Do List: Add/Check/Remove Items
The process to add a new item or remove an existing item is the same as that of adding/removing a list. The user can also mark an item as completed.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/Add%20:%20Remove%20:%20Complete%20Task.gif "Home+ Add/Check/Remove Items")

#### Calendar
For this feature, the Google Calendar API is used in order to display information specific to the user. The API requires the Google OAuth 2 authorisation for access from the user’s Google account the first time that the user logs in. A JavaScript library called Toast UI is used to render the calendar on the browser, and the Google Calendar API is then called to populate the Toast UI calendar with the user's events. A user can click on the events in the calendar to check the event details. The user can also go to the previous/next months by clicking on the buttons.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/Calendar.gif "Home+ Calendar Authorisation")

#### Stocks
This feature displays five of the most popular stocks with their latest price. The Alpha Vantage API has been used to display real-time stock price information. An AJAX request is made to render information retrieved from the HTTP request to the API on to the web-page asynchronously and at a set interval of time to update the prices.

#### Stocks: Modal Window
A user can also search for any other stock using its symbol or ID to get the price for that stock. Each time the user clicks on the "Submit" button, an AJAX request is made to display the current price.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/Stocks.gif "Home+ Stocks Modal Display")

#### News
This feature to displays 20 of the latest news headlines that are being fetched from the News API. On click, the headlines are being redirected to their actual web-pages.

![alt text](https://github.com/shimoleejhaveri/Homeplus/blob/master/static/img/News.gif "Home+ News Display")

## <a name="future"></a>Future State
The project roadmap for Home+ has several features planned out for the next sprint:
* Maps feature to display commute time using different transit modes using the Google Directions API
* Weather feature to display daily weather using Geolocation API
* Charts to show daily stock price fluctuations for displayed and searched stocks
* Password hashing

## <a name="installation"></a>Installation
To run Home+ on your own machine:

Install PostgresQL (Mac OSX)

Clone or fork this repo:
```
https://github.com/shimoleejhaveri/Homeplus.git
```

Create and activate a virtual environment inside your JobTracker directory:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip install -r requirements.txt
```

Sign up to use the [Alpha Vantage API](https://www.alphavantage.co/), [Google Calendar API](https://developers.google.com/calendar/), and [News API](https://newsapi.org/)

Save your API keys in a file called <kbd>secrets.sh</kbd> using this format:

```
export AV_API_KEY="YOUR_KEY_HERE"
export GOOGLE_API_KEY="YOUR_KEY_HERE"
export GOOGLE_CLIENT_ID="YOUR_ID_HERE"
export CAL_CLIENT_SECRET="YOUR_SECRET_HERE"
export NEWS_API_KEY="YOUR_KEY_HERE"
```

Source your keys from your secrets.sh file into your virtual environment:

```
source secrets.sh
```

Set up the database:

```
createdb hackbright_project
```

Run the app:

```
python3 server.py
```

You can now navigate to 'localhost:5000/' to access Home+.
