# LUCKY DRAW GAMING SERVICE
Project building an API using Flask and Python


Introduction
------------
A service which allows users to get Lucky Draw Raffle tickets
and use one lucky draw raffle ticket to participate in a lucky draw game.

This service calls a local SQLite database. Please see databases directory for more details.

Installing Project Dependencies
-----

You can install the dependency using the following command:

`pip install flask`

Next run the following command to install the dependencies for scheduler:

`pip install APScheduler`


Running the application
-----
After you have performed all the dependency installations from above, you can run the following command on your terminal
to start this app.

From the root of this project enter the following terminal command:

`python app.py`


Project Database
-----
This project uses a local sqlite for a repository.  


Rest API's endpoints
-----

GET - homepage: [/](http://127.0.0.1:5000/)

GET - newuser: [/enternew](http://127.0.0.1:5000/enternew?)

POST - newregister_db: [/addrec](http://127.0.0.1:5000/addrec?) + include the details

GET - purchaseticket: [/buy](http://127.0.0.1:5000/buy?)

POST - ticket_db: [/purchase](http://127.0.0.1:5000/purchase?) + include the details

GET - participate: [/part](http://127.0.0.1:5000/part?)

POST - participate_db: [/parevent](http://127.0.0.1:5000/parevent?) + include the details

GET - show_winners: [/winner](http://127.0.0.1:5000/winner?)

GET - show_next_event: [/event](http://127.0.0.1:5000/event?)
