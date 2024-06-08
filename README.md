# Garden Planner
Garden Planner was my Final Project for CS50. It is a web app, built with a Python/Flask/PostgreSQL stack, that allows users plan their yearly gardens. 

### Getting started
Garden Planner was originally deployed on Render ([here](https://garden-planner-2spe.onrender.com/)), and is not currently live.  

But you can check out my video demonstration on YouTube below! 

#### Video demonstration
[![Garden Planner screencast](https://img.youtube.com/vi/4ROhMB_EX68/0.jpg)](https://www.youtube.com/watch?v=4ROhMB_EX68)

## Description:
Users are able to add virtual gardens to their page, and plan which plants they will have in their gardens throughout the year.

Garden Planner also contains a database of commonly grown plants, including optimal months to sow their seeds, duration to maturity, space required, and more. The gardening information is specific to north-east Melbourne (Australia) - a temperate zone - and the metric system is used.

There is also functionality to add or remove freetext plants, check which plants play well with each other (and conversely which plants do not like each other), and to check the weather for the upcoming week for a user-specified location.

## Schema
This is the main SQL database, which was originally SQLite (and converted to PostgreSQL for deployment on Render). It contains information on all users, plants, freetext plants, gardens, companion friends, and companion enemies.

The schema is as follows:
- CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username TEXT NOT NULL, hash_password TEXT NOT NULL);
- CREATE TABLE sqlite_sequence(name,seq);
- CREATE TABLE gardens (garden_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, user_id INTEGER NOT NULL, garden_size_metres_squared NUMERIC NOT NULL, garden_name TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id));
- CREATE TABLE companion_friends (plant_id_a INTEGER NOT NULL, plant_id_b INTEGER NOT NULL, FOREIGN KEY (plant_id_a) REFERENCES plants(plant_id), FOREIGN KEY (plant_id_b) REFERENCES plants(plant_id));
- CREATE TABLE companion_enemies (plant_id_a INTEGER NOT NULL, plant_id_b INTEGER NOT NULL, FOREIGN KEY (plant_id_a) REFERENCES plants(plant_id), FOREIGN KEY (plant_id_b) REFERENCES plants(plant_id));
- CREATE TABLE plants (plant_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, plant_name TEXT NOT NULL UNIQUE, duration_to_maturity_months INTEGER NOT NULL, plant_spacing_metres NUMERIC NOT NULL, metres_squared_required NUMERIC NOT NULL, perennial_or_annual TEXT NOT NULL, january TEXT NOT NULL, february TEXT NOT NULL, march TEXT NOT NULL, april TEXT NOT NULL, may TEXT NOT NULL, june TEXT NOT NULL, july TEXT NOT NULL, august TEXT NOT NULL, september TEXT NOT NULL, october TEXT NOT NULL, november TEXT NOT NULL, december TEXT NOT NULL);
- CREATE TABLE freetext_plants (plant_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, user_id INTEGER NOT NULL , plant_name TEXT NOT NULL, duration_to_maturity_months INTEGER NOT NULL, plant_spacing_metres NUMERIC NOT NULL, metres_squared_required NUMERIC NOT NULL, perennial_or_annual TEXT NOT NULL, january TEXT NOT NULL, february TEXT NOT NULL, march TEXT NOT NULL, april TEXT NOT NULL, may TEXT NOT NULL, june TEXT NOT NULL, july TEXT NOT NULL, august TEXT NOT NULL, september TEXT NOT NULL, october TEXT NOT NULL, november TEXT NOT NULL, december TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id));
- CREATE TABLE planted_in_gardens (plant_id INTEGER NOT NULL, number_of_plants INTEGER NOT NULL DEFAULT 0, month_planted TEXT NOT NULL, months_to_remain_planted INTEGER NOT NULL, freetext TEXT NOT NULL DEFAULT 'no', garden_id INTEGER NOT NULL, FOREIGN KEY (garden_id) REFERENCES gardens(garden_id));

## Technologies:
- Python 
- Flask 
- SQLite
- PostgreSQL 
- HTML
- CSS
- JavaScript
- Render

## Data sources:
- Plant information: https://localfoodconnect.org.au/community-gardening/planting-guide/
- Companion planting information: https://www.sgaonline.org.au/companion-planting/
- Weather API: https://open-meteo.com/

## Image sources:
- Website leaf background: https://depositphotos.com/photo/watercolor-pattern-with-fern-leaves-texture-for-fabric-and-wrapping-paper-herbal-print-473825398.html