# Garden Planner
## Video Demo: https://youtu.be/b-vBhZhq2bg
## Description:
This project is a web application that helps users plan their gardens. Users are able to add virtual gardens to their page, and plan which plants they will have in their gardens throughout the year.
The web application also contains a database of commonly grown plants, including optimal months to sow their seeds, duration to maturity, space required, and more. The gardening information is specific to north-east Melbourne (Australia) - a temperate zone - and the metric system is used.
There is also functionality to add or remove freetext plants, check which plants play well with each other (and conversely which plants do not like each other), and to check the weather for the upcoming week for a user-specified location.

## File descriptions:
### flask_session
Stores the sessions from the flask application.

### static
#### colour_months_row.js
This Javascript iterates through the rows containing months of the year in each Yearly Garden Table, and colours the rows according to their season. The colours are semi transparent, to allow the table to blend in with the muted tone of the website as a whole.

#### hide_show_add_freetext_plant.js
This Javascript hides the form for adding freetext plants, and toggles between hiding and showing the form when the hide/show button is clicked.

#### hide_show_add_new_garden.js
This Javascript hides the form for adding a new garden, and toggles between hiding and showing the form when the hide/show button is clicked.

#### hide_show_add_plants_to_garden.js
This Javascript hides the form for adding plants to an existing, and toggles between hiding and showing the form when the hide/show button is clicked.

#### hide_show_all_plants.js
This Javascript hides the table containing informnation for all plants, and toggles between hiding and showing the table when the hide/show button is clicked.

#### hide_show_companion_enemies.js
This Javascript hides the table for companion enemies, and toggles between hiding and showing the table when the hide/show button is clicked.

#### hide_show_companion_friends.js
This Javascript hides the table for companion friends, and toggles between hiding and showing the table when the hide/show button is clicked.

#### hide_show_freetext_plants_user.js
This Javascript hides the table containing informnation for all freetext plants added by the user, and toggles between hiding and showing the table when the hide/show button is clicked.

#### hide_show_remove_freetext_plant.js
This Javascript hides the form for removing freetext plants, and toggles between hiding and showing the form when the hide/show button is clicked.

#### hide_show_remove_garden.js
This Javascript hides the form for removing an existing garden, and toggles between hiding and showing the form when the hide/show button is clicked.

#### hide_show_remove_plants_from_garden.js
This Javascript hides the form for removing existing plants from an existing garden, and toggles between hiding and showing the form when the hide/show button is clicked.

#### search_all_plants.js
This Javascript hides the search table containing informnation for all plants, and shows only the plants (and related information) that have a plant name that begins with the string that the user has typed into the search bar.

#### sort_table.js
This Javascript applies to multiple tables, and sorts the rows by alphabetical order of the plant name.

#### styles.css
This is the main stylesheet containing the css styles for the web application.

#### watercolour_fern.png
This is the original image that is used for the background of the website.

### templates
#### admin.html
This is a admin page, accessible only to the administrator (with the unique username 'admin') when they are logged in. It contains multiple forms which interact with a SQL database. The forms allow the admin to add new plants to the database, remove plants from the database, update information about an existing plant in the database, add or remove companion friends (plants that grow well together), and add or remove companion enemies (plants that do not grow well together).

#### change_password.html
This page allows users that are logged in, to change their passwords by updating their hash password on the database. It requires the new password to be confirmed twice, to ensure a match.

#### error.html
This is an error page, displaying a customised error message to the user when information is entered incorrectly, returning an error 400. This page "GETS" the return value of an error message function, which concatanates the custom 'message' to the error message layout.

#### index.html
This is the home page for the user, and contains the Yearly Garden Plans for their gardens. The Yearly Garden Plans are tables with 12 rows (1 for each month), each of which contains the plants that are growing at that time (and quantity of these plants), and calculates the remaning space in the garden for that month (by subtracting the space taken up from the overall garden size). Below these Yearly Garden Plans, users can access multiple forms to add/remove freetext plants, add/remove gardens, and add/remove plants from their gardens. These forms are hidden initially, and can be toggled to display by clicking on the hide/show buttons beside their form names. This design choice was made to minimise clutter on the home page, so that users would only have to interact with the forms when they intended to.

#### information.html
The information page is accessed from the All Plants button in the navigation bar. It is a comprehensive resource for the user. It contains a search bar, which initially has all rows hidden, and as the user types a string into the search bar, the search results table is automatically populated with plants (and their related information) which have plant names that begin with the string that the user has typed.
For rapid access, there is also an All Plants table, which is initially also hidden, and can be made visible by clicking the hide/show button. It is a simple table that contains all the plants with all their information.
Below that, there is a similar table for freetext plants added by the user, as well as tables listing companion plant friends and enemies.

#### layout.html
This is the HTML boilerplate for all of the web application's pages.
In the head, there is a meta link to optimise display on all viewports. There are also multiple links to the styles.css stylesheet, google fonts, and all javascript files.
In the body, there is a navigation bar with buttons for Home, All Plants, Weather, Change Password and Logout. If admin is logged in, Admin is also visible.

#### login.html
This is the login page, which logs the user out (if session was present) and contains a simple form for the user to enter their username (unique) and password, which is checked using the check_password_hash function.

#### register.html
This is the registration page, which logs the user out (if session was present) and contains a simple form for the user to enter their username (unique), password and password confirmation, which is then submitted for hashing and storage to the project's SQL database.

#### weather.html
This page uses an API from an online weather application called open-meteo, to display the 7-day weather forecast (max temp, min temp and rainfall) for Fitzroy Victoria Australia. It also contains a form for users to submit their own latitude and longitude, so that they can update the weather forecast, if they would like. The latitude and longitude is submitted to open-meteo, which sends back a Panda Dataframe with the weather forecast.
It allows the user to plan their watering schedule according to the expected temperature and rainfall.

### app.py
This is the python code back-end of the web application, which uses Flask to create URL routes.
Most of its functionality has been discussed in descriptions of the associated HTML pages.
Most of the code contained within this document is dedicated to server-side verification of user input, and subsequently updating the SQL database with new information.

### project.db
This is the master SQL database containing information on all users, plants, freetext plants, gardens, companion friends, and companion enemies.
The schema is as follows:
- CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username TEXT NOT NULL, hash_password TEXT NOT NULL);
- CREATE TABLE sqlite_sequence(name,seq);
- CREATE TABLE gardens (garden_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, user_id INTEGER NOT NULL, garden_size_metres_squared NUMERIC NOT NULL, garden_name TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id));
- CREATE TABLE companion_friends (plant_id_a INTEGER NOT NULL, plant_id_b INTEGER NOT NULL, FOREIGN KEY (plant_id_a) REFERENCES plants(plant_id), FOREIGN KEY (plant_id_b) REFERENCES plants(plant_id));
- CREATE TABLE companion_enemies (plant_id_a INTEGER NOT NULL, plant_id_b INTEGER NOT NULL, FOREIGN KEY (plant_id_a) REFERENCES plants(plant_id), FOREIGN KEY (plant_id_b) REFERENCES plants(plant_id));
- CREATE TABLE plants (plant_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, plant_name TEXT NOT NULL UNIQUE, duration_to_maturity_months INTEGER NOT NULL, plant_spacing_metres NUMERIC NOT NULL, metres_squared_required NUMERIC NOT NULL, perennial_or_annual TEXT NOT NULL, january TEXT NOT NULL, february TEXT NOT NULL, march TEXT NOT NULL, april TEXT NOT NULL, may TEXT NOT NULL, june TEXT NOT NULL, july TEXT NOT NULL, august TEXT NOT NULL, september TEXT NOT NULL, october TEXT NOT NULL, november TEXT NOT NULL, december TEXT NOT NULL);
- CREATE TABLE freetext_plants (plant_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, user_id INTEGER NOT NULL , plant_name TEXT NOT NULL, duration_to_maturity_months INTEGER NOT NULL, plant_spacing_metres NUMERIC NOT NULL, metres_squared_required NUMERIC NOT NULL, perennial_or_annual TEXT NOT NULL, january TEXT NOT NULL, february TEXT NOT NULL, march TEXT NOT NULL, april TEXT NOT NULL, may TEXT NOT NULL, june TEXT NOT NULL, july TEXT NOT NULL, august TEXT NOT NULL, september TEXT NOT NULL, october TEXT NOT NULL, november TEXT NOT NULL, december TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id));
- CREATE TABLE planted_in_gardens (plant_id INTEGER NOT NULL, number_of_plants INTEGER NOT NULL DEFAULT 0, month_planted TEXT NOT NULL, months_to_remain_planted INTEGER NOT NULL, freetext TEXT NOT NULL DEFAULT 'no', garden_id INTEGER NOT NULL, FOREIGN KEY (garden_id) REFERENCES gardens(garden_id));

The users table contains the user id (which must be unique), the user name, and the user's hashed password.

The gardens table contains the garden id (which much be unique), the user id associated with the garden, the garden size, and the garden name.

The companion friends table contains the ids of the two plants that are friends. Conversely, the companion enemies table contains the ids of the two plants that are enemies.

The plants table can only be edited by the admin. It contains the plant id (unique), name, duration to maturity from seed (unless otherwise specified), spacing in metres, meters squared required (which is the square of the spacing in metres), whether the plant is perennial or annual (therefore how long it should remain on the Yearly Garden Table once planted), and the months of the year that the plant can be planted from seed (marked as 'yes' if plantable during that month, 'no' if not).

The freetext plants table is the same as the plants table, but also contains the user id associated with that freetext plant.

The planted in gardens table allows us to link specific gardens with multiple plants, by giving information on the plant id of the plant that was planted, the quantity of that plant that was planted, the month it was planted, how long the user specified that it should remain planted (which does not necessarily need to equal the 'duration to maturity' of the plant, as a mature plant can remain in ground after it has matured, and users may know that a certain plant takes longer or shorter to mature in their geographic region/soil), whether the plant was freetext (so that we know whether to search for the plant name in the plants or freetext plants table), and the garden id of the garden that the plant was planted in.

### requirements.txt
This is a text file containing a list of the required imported tools to run the application.

## Data sources:
- Plant information: https://localfoodconnect.org.au/community-gardening/planting-guide/
- Companion planting information: https://www.sgaonline.org.au/companion-planting/
- Weather API: https://open-meteo.com/

## Image sources:
- Website leaf background: https://depositphotos.com/photo/watercolor-pattern-with-fern-leaves-texture-for-fabric-and-wrapping-paper-herbal-print-473825398.html

