import os
import csv
import calendar
import datetime
import psycopg2
import psycopg2.extras
import pytz
import requests
import urllib

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# WEATHER API
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = psycopg2.connect(host=os.environ['DB_HOST'], 
                      port=int(os.environ['DB_PORT']),
                      database=os.environ['DB_NAME'],
                      user=os.environ['DB_USER'],       
                      password=os.environ['DB_PASSWORD'])
                     
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
   
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def error(message, code):
    final_message = "Error " + str(code) + ": " +  message
    return render_template("error.html", final_message=final_message, code=code)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    with db.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", ('admin',))
        admin = cur.fetchall()
      
        if len(admin) == 1:
            if session["user_id"] == admin[0]["user_id"]:
                admin_id = admin[0]["user_id"]
        else:
            admin_id = None
  
        if request.method == "POST":
            # Add freetext plants or gardens (including require plants) to SQL database, per user input from form in index.html
            if request.form.get("add_freetext_plant_button"):
                if not request.form.get("plant_name_add"):
                    return error("Must provide plant name.", 400)
                elif not request.form.get("duration_to_maturity_months_add"):
                    return error("Must provide duration to maturity (months).", 400)
                elif not request.form.get("plant_spacing_metres_add"):
                    return error("Must provide spacing (metres).", 400)
                elif not request.form.get("perennial_or_annual_add"):
                    return error("Must specify perennial or annual.", 400)
    
                if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_add")) or not request.form.get("plant_name_add").islower():
                    return error("Plant name must be lowercase and alphabetical.", 400)
    
                try:
                    duration_to_maturity_months_add = int(request.form.get("duration_to_maturity_months_add"))
                except ValueError:
                    return error("Duration to maturity (months) must be integer.", 400)
    
                if duration_to_maturity_months_add <= 0:
                        return error("Duration to maturity (months) must be positive number.", 400)
    
                try:
                    plant_spacing_metres_add = int(request.form.get("plant_spacing_metres_add"))
                except ValueError:
                    try:
                        plant_spacing_metres_add = float(request.form.get("plant_spacing_metres_add"))
                    except ValueError:
                        return error("Spacing (metres) must be integer or decimal number.", 400)
    
                if plant_spacing_metres_add <= 0:
                    return error("Spacing (metres) must be positive number.", 400)
    
                string_plant_spacing_metres_add = str(plant_spacing_metres_add)
                decimal_places = string_plant_spacing_metres_add[::-1].find(".")
    
                if decimal_places == -1:
                    metres_squared_required_add = round(plant_spacing_metres_add ** 2, 0)
                elif decimal_places == 1:
                    metres_squared_required_add = round(plant_spacing_metres_add ** 2, 2)
                elif decimal_places == 2:
                    metres_squared_required_add = round(plant_spacing_metres_add ** 2, 4)
                else:
                    metres_squared_required_add = round(plant_spacing_metres_add ** 2, 6)
    
    
                if request.form.get("perennial_or_annual_add") != "perennial" and request.form.get("perennial_or_annual_add") != "annual":
                    return error("Must select either perennial or annual.", 400)
    
                january_add = "no"
                february_add = "no"
                march_add = "no"
                april_add = "no"
                may_add = "no"
                june_add = "no"
                july_add = "no"
                august_add = "no"
                september_add = "no"
                october_add = "no"
                november_add = "no"
                december_add = "no"
    
                if request.form.get("january_add") == "yes":
                    january_add = "yes"
                if request.form.get("february_add") == "yes":
                    february_add = "yes"
                if request.form.get("march_add") == "yes":
                    march_add = "yes"
                if request.form.get("april_add") == "yes":
                    april_add = "yes"
                if request.form.get("may_add") == "yes":
                    may_add = "yes"
                if request.form.get("june_add") == "yes":
                    june_add = "yes"
                if request.form.get("july_add") == "yes":
                    july_add = "yes"
                if request.form.get("august_add") == "yes":
                    august_add = "yes"
                if request.form.get("september_add") == "yes":
                    september_add = "yes"
                if request.form.get("october_add") == "yes":
                    october_add = "yes"
                if request.form.get("november_add") == "yes":
                    november_add = "yes"
                if request.form.get("december_add") == "yes":
                    december_add = "yes"
    
                cur.execute("INSERT INTO freetext_plants (user_id, plant_name, duration_to_maturity_months, plant_spacing_metres, metres_squared_required, perennial_or_annual, january, february, march, april, may, june, july, august, september, october, november, december) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (int(session["user_id"]), request.form.get("plant_name_add"), duration_to_maturity_months_add, plant_spacing_metres_add, metres_squared_required_add, request.form.get("perennial_or_annual_add"), january_add, february_add, march_add, april_add, may_add, june_add, july_add, august_add, september_add, october_add, november_add, december_add,))          
                db.commit()
              
                return redirect("/")
    
            if request.form.get("remove_freetext_plant_button"):
                if not request.form.get("plant_name_remove"):
                    return error("Must provide plant name.", 400)
                if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_remove")) or not request.form.get("plant_name_remove").islower():
                    return error("Plant name must be lowercase and alphabetical.", 400)
  
                cur.execute("SELECT freetext_plants.plant_name FROM freetext_plants WHERE freetext_plants.user_id = %s", (int(session["user_id"]),))
                freetext_plant_names_from_user = cur.fetchall()
              
                is_plant_in_db = False
    
                for i in range(len(freetext_plant_names_from_user)):
                    if freetext_plant_names_from_user[i]["plant_name"] == request.form.get("plant_name_remove"):
                        is_plant_in_db = True
    
                if is_plant_in_db == False:
                    return error("Plant name not found.", 400)
    
                cur.execute("SELECT plant_id FROM freetext_plants WHERE plant_name = %s AND user_id = %s", (request.form.get("plant_name_remove"), int(session["user_id"])))
                plant_id = cur.fetchall() 
  
  
                for i in range(len(plant_id)):
                  cur.execute("DELETE FROM freetext_plants WHERE plant_id = %s", (plant_id[i]["plant_id"],))
                  cur.execute("DELETE FROM planted_in_gardens WHERE plant_id = %s", (plant_id[i]["plant_id"],))
                  cur.execute("DELETE FROM companion_friends WHERE plant_id_a = %s OR plant_id_b = %s", (plant_id[i]["plant_id"], plant_id[i]["plant_id"]))
                  cur.execute("DELETE FROM companion_enemies WHERE plant_id_a = %s OR plant_id_b = %s", (plant_id[i]["plant_id"], plant_id[i]["plant_id"]))
                
                db.commit()
              
                return redirect("/")
    
            if request.form.get("add_new_garden_button"):
                if not request.form.get("add_new_garden_name"):
                    return error("Must provide garden name.", 400)
                elif not request.form.get("add_new_garden_size"):
                    return error("Must provide garden size (metres squared).", 400)
    
                if not all(x.isalpha() or x.isspace() for x in request.form.get("add_new_garden_name")) or not request.form.get("add_new_garden_name").islower():
                        return error("Garden name must be lowercase and alphabetical.", 400)
    
                try:
                    add_new_garden_size = int(request.form.get("add_new_garden_size"))
                except ValueError:
                    return error("Garden size (metres squared) must be integer.", 400)
    
                if add_new_garden_size <= 0:
                    return error("Garden size (metres squared) must be integer.", 400)
    
                cur.execute("SELECT garden_name FROM gardens WHERE user_id = %s", (int(session["user_id"]),))
                garden_names_user = cur.fetchall()
              
                for i in range(len(garden_names_user)):
                    if garden_names_user[i]["garden_name"] == request.form.get("add_new_garden_name"):
                        return error("You already have a garden with that name.", 400)
  
                cur.execute("INSERT INTO gardens (garden_name, garden_size_metres_squared, user_id) VALUES (%s, %s, %s)", (request.form.get("add_new_garden_name"), request.form.get("add_new_garden_size"), int(session["user_id"])))
                db.commit()
              
                return redirect("/")
    
            if request.form.get("remove_garden_button"):
                if not request.form.get("remove_garden_name"):
                    return error("Must provide garden name.", 400)
                if not all(x.isalpha() or x.isspace() for x in request.form.get("remove_garden_name")) or not request.form.get("remove_garden_name").islower():
                    return error("Garden name must be lowercase and alphabetical.", 400)
    
                cur.execute("SELECT garden_name FROM gardens WHERE user_id = %s", (int(session["user_id"]),))
                garden_names = cur.fetchall()
    
                is_plant_in_db = False
    
                for i in range(len(garden_names)):
                    if garden_names[i]["garden_name"] == request.form.get("remove_garden_name"):
                        is_plant_in_db = True
    
                if is_plant_in_db == False:
                    return error("You don't have a garden with that name.", 400)
    
                cur.execute("SELECT garden_id FROM gardens WHERE garden_name = %s AND user_id = %s", (request.form.get("remove_garden_name"), int(session["user_id"])))
                garden_id = cur.fetchall()
  
                for i in range(len(garden_id)):
                  cur.execute("DELETE FROM gardens WHERE garden_id = %s", (garden_id[i]["garden_id"],))
                  cur.execute("DELETE FROM planted_in_gardens WHERE garden_id = %s", (garden_id[i]["garden_id"],))
  
                db.commit()
            
                return redirect("/")
    
            if request.form.get("add_plants_to_garden_button"):
                if not request.form.get("add_plants_to_garden_garden_name"):
                    return error("Must provide garden name.", 400)
                if not request.form.get("add_plants_to_garden_plant_name"):
                    return error("Must provide plant name.", 400)
                if not request.form.get("add_plants_to_garden_number_of_plants"):
                    return error("Must provide number of plants to add.", 400)
                if not request.form.get("add_plants_to_garden_month_planted"):
                    return error("Must indicate in which month planted.", 400)
                if not request.form.get("add_plants_to_garden_months_to_remain_planted"):
                    return error("Must provide number of months to remain planted.", 400)
                if not request.form.get("add_plants_to_garden_freetext"):
                    return error("Must indicate whether plant is freetext.", 400)
    
                if not all(x.isalpha() or x.isspace() for x in request.form.get("add_plants_to_garden_garden_name")) or not request.form.get("add_plants_to_garden_garden_name").islower():
                    return error("Garden name must be lowercase and alphabetical.", 400)
                if not all(x.isalpha() or x.isspace() for x in request.form.get("add_plants_to_garden_plant_name")) or not request.form.get("add_plants_to_garden_plant_name").islower():
                    return error("Plant name must be lowercase and alphabetical.", 400)
                if not all(x.isalpha() or x.isspace() for x in request.form.get("add_plants_to_garden_month_planted")) or not request.form.get("add_plants_to_garden_month_planted").islower():
                    return error("Month planted must be lowercase and alphabetical.", 400)
    
                try:
                    add_plants_to_garden_number_of_plants = int(request.form.get("add_plants_to_garden_number_of_plants"))
                except ValueError:
                    return error("Number of plants to add must be integer.", 400)
    
                if add_plants_to_garden_number_of_plants <= 0:
                    return error("Number of months this plant was planted for must be positive number.", 400)
    
                try:
                    add_plants_to_garden_months_to_remain_planted = int(request.form.get("add_plants_to_garden_months_to_remain_planted"))
                except ValueError:
                    return error("Number of months to remain planted must be integer.", 400)
    
                if add_plants_to_garden_months_to_remain_planted <= 0:
                    return error("Number of months to remain planted must be positive number.", 400)
    
                if request.form.get("add_plants_to_garden_freetext") != "yes" and request.form.get("add_plants_to_garden_freetext") != "no":
                    return error("Is the plant freetext? Must select either yes or no.", 400)

                print("TESTINGGGGGGGGGGGGGTESTINGGGGGGGGGGGGGTESTINGGGGGGGGGGGGGTESTINGGGGGGGGGGGGGTESTINGGGGGGGGGGGGGTESTINGGGGGGGGGGGGGTESTINGGGGGGGGGGGGGTESTINGGGGGGGGGGGGG")
                
                garden_id = None
                cur.execute("SELECT garden_id FROM gardens WHERE user_id = %s AND garden_name = %s", (int(session["user_id"]), request.form.get("add_plants_to_garden_garden_name")))
                garden_id = cur.fetchone()["garden_id"]
  
                if garden_id == None:
                    return error("Garden name not found.", 400)
    
                plant_id = None
                if request.form.get("add_plants_to_garden_freetext") == 'no':
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("add_plants_to_garden_plant_name"),))
                    plant_id = cur.fetchone()["plant_id"]
                elif request.form.get("add_plants_to_garden_freetext") == 'yes':
                    cur.execute("SELECT plant_id FROM freetext_plants WHERE plant_name = %s", (request.form.get("add_plants_to_garden_plant_name"),))
                    plant_id = cur.fetchone()["plant_id"]
                if plant_id == None:
                    return error("Plant not found.", 400)
    
                months_of_year = []
                for j in range(1, 13):
                    months_of_year.append(calendar.month_name[j].lower())
    
                if request.form.get("add_plants_to_garden_month_planted") not in months_of_year:
                    return error("Month to be planted invalid.", 400)
    
                if request.form.get("add_plants_to_garden_freetext") != 'yes' and  request.form.get("add_plants_to_garden_freetext") != 'no':
                    return error("Is the plant freetext? Must select either yes or no.", 400)
    
                cur.execute("INSERT INTO planted_in_gardens (plant_id, garden_id, number_of_plants, month_planted, months_to_remain_planted, freetext) VALUES (%s, %s, %s, %s, %s, %s)", (plant_id, garden_id, request.form.get("add_plants_to_garden_number_of_plants"), request.form.get("add_plants_to_garden_month_planted"), request.form.get("add_plants_to_garden_months_to_remain_planted"), request.form.get("add_plants_to_garden_freetext")),)
                db.commit()
              
                return redirect("/")
    
            if request.form.get("remove_plants_from_garden_button"):
                if not request.form.get("remove_plants_from_garden_garden_name"):
                    return error("Must provide garden name.", 400)
                if not request.form.get("remove_plants_from_garden_plant_name"):
                    return error("Must provide plant name.", 400)
                if not request.form.get("remove_plants_from_garden_number_of_plants"):
                    return error("Must provide number of plants to remove.", 400)
                if not request.form.get("remove_plants_from_garden_month_planted"):
                    return error("Must provide month planted.", 400)
                if not request.form.get("remove_plants_from_garden_months_to_remain_planted"):
                    return error("Must provide number of months this plant was planted for.", 400)
                if not request.form.get("remove_plants_from_garden_freetext"):
                    return error("Is the plant freetext? Must select either yes or no.", 400)
                if not all(x.isalpha() or x.isspace() for x in request.form.get("remove_plants_from_garden_garden_name")) or not request.form.get("remove_plants_from_garden_garden_name").islower():
                    return error("Garden name must be lowercase and alphabetical.", 400)
                if not all(x.isalpha() or x.isspace() for x in request.form.get("remove_plants_from_garden_plant_name")) or not request.form.get("remove_plants_from_garden_plant_name").islower():
                    return error("Plant name must be lowercase and alphabetical.", 400)
                if not all(x.isalpha() or x.isspace() for x in request.form.get("remove_plants_from_garden_month_planted")) or not request.form.get("remove_plants_from_garden_month_planted").islower():
                    return error("Month planted must be lowercase and alphabetical.", 400)
    
                if request.form.get("remove_plants_from_garden_freetext") != "yes" and request.form.get("remove_plants_from_garden_freetext") != "no":
                    return error("Is the plant freetext? Must select either yes or no.", 400)
                try:
                    remove_plants_from_garden_number_of_plants = int(request.form.get("remove_plants_from_garden_number_of_plants"))
                except ValueError:
                    return error("Number of plants to remove from garden must be integer.", 400)
    
                if remove_plants_from_garden_number_of_plants <= 0:
                    return error("Number of plants to remove from garden must be positive number.", 400)
    
                try:
                    remove_plants_from_garden_months_to_remain_planted = int(request.form.get("remove_plants_from_garden_months_to_remain_planted"))
                except ValueError:
                    return error("Number of months this plant was planted for must be integer.", 400)
    
                if remove_plants_from_garden_months_to_remain_planted <= 0:
                    return error("Number of months this plant was planted for must be positive number.", 400)
    
                cur.execute("SELECT garden_id FROM gardens WHERE user_id = %s AND garden_name = %s", (int(session["user_id"]), request.form.get("remove_plants_from_garden_garden_name")),)
                garden_ids = cur.fetchall()
  
                if len(garden_ids) == 0:
                    return error("Garden name not found.", 400)
                garden_id = garden_ids[0]["garden_id"]
    
                plant_id = None
                if request.form.get("remove_plants_from_garden_freetext") == 'no':
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("remove_plants_from_garden_plant_name"),),)  
                    plant_id = cur.fetchone()["plant_id"]
                elif request.form.get("remove_plants_from_garden_freetext") == 'yes':
                    cur.execute("SELECT plant_id FROM freetext_plants WHERE plant_name = %s", (request.form.get("remove_plants_from_garden_plant_name"),),)
                    result = cur.fetchone()
                    plant_id = result["plant_id"]
   
                if plant_id == None:
                    return error("Plant not found.", 400)
    
                cur.execute("SELECT month_planted FROM planted_in_gardens WHERE garden_id = %s AND plant_id = %s", (garden_id, plant_id),)
                months_planted = cur.fetchall()

                planted_that_month = False
                for i in range(len(months_planted)):
                    if request.form.get("remove_plants_from_garden_month_planted") == months_planted[i]["month_planted"]:
                        planted_that_month = True
    
                if not (planted_that_month):
                    return error("None of that plant was planted that month.", 400)
    
                cur.execute("SELECT number_of_plants FROM planted_in_gardens WHERE garden_id = %s AND plant_id = %s AND month_planted = %s", (garden_id, plant_id, request.form.get("remove_plants_from_garden_month_planted")),)
                number_of_plants = cur.fetchall()

                correct_number_of_plants_that_month = False
                for i in range(len(number_of_plants)):
                    if int(request.form.get("remove_plants_from_garden_number_of_plants")) == number_of_plants[i]["number_of_plants"]:
                        correct_number_of_plants_that_month = True
                    if not (correct_number_of_plants_that_month):
                        return error("Must match number of plants planted that month.", 400)
    
                cur.execute("SELECT months_to_remain_planted FROM planted_in_gardens WHERE garden_id = %s AND plant_id = %s AND month_planted = %s AND number_of_plants = %s", (garden_id, plant_id, request.form.get("remove_plants_from_garden_month_planted"), int(request.form.get("remove_plants_from_garden_number_of_plants"))),)
                months_to_remain_planted = cur.fetchall()
                
                correct_months_to_remain_planted = False
                for i in range(len(months_to_remain_planted)):
                    if int(request.form.get("remove_plants_from_garden_months_to_remain_planted")) == months_to_remain_planted[i]["months_to_remain_planted"]:
                        correct_months_to_remain_planted = True
                if not (correct_months_to_remain_planted):
                    return error("The requested plant (that was planted that month) was not to remain planted for that many months.", 400)
    
                cur.execute("DELETE FROM planted_in_gardens WHERE garden_id = %s AND plant_id = %s AND month_planted = %s AND number_of_plants = %s AND months_to_remain_planted = %s", (garden_id, plant_id, request.form.get("remove_plants_from_garden_month_planted"), request.form.get("remove_plants_from_garden_number_of_plants"), request.form.get("remove_plants_from_garden_months_to_remain_planted"),),)
                db.commit()        
                return redirect("/")
              
            return redirect ("/")
    
        else:
            cur.execute("SELECT garden_id, garden_name, garden_size_metres_squared FROM gardens WHERE user_id = %s", (int(session["user_id"]),),)
            garden_ids_from_user = cur.fetchall()

            number_of_gardens_from_user = len(garden_ids_from_user)
    
            planted_gardens_from_user = []
            for i in range(number_of_gardens_from_user):
                planted_gardens_from_user.append([])
    
            months_of_year = []
            for i in range(1, 13):
                months_of_year.append(calendar.month_name[i].lower())
    
            total_different_plants_in_garden = []
            all_plant_names_in_garden = []
            space_remaining_each_month = []
            for i in range(number_of_gardens_from_user):
                total_different_plants_in_garden.append([])
                all_plant_names_in_garden.append([])
                space_remaining_each_month.append([])
    
            if number_of_gardens_from_user > 0:
                for i in range(number_of_gardens_from_user):
                    plants_planted_each_month_of_year = []
                    plants_growing_each_month_of_year = []
                    for j in range(12):
                        plants_planted_each_month_of_year.append([])
                        plants_growing_each_month_of_year.append([])
                        space_remaining_each_month[i].append([])
                    for j in range(12):
                        cur.execute("SELECT plants.plant_name, planted_in_gardens.number_of_plants, planted_in_gardens.months_to_remain_planted, plants.metres_squared_required, plants.perennial_or_annual FROM gardens INNER JOIN planted_in_gardens ON gardens.garden_id = planted_in_gardens.garden_id INNER JOIN plants ON planted_in_gardens.plant_id = plants.plant_id WHERE planted_in_gardens.month_planted = %s AND gardens.garden_id = %s AND gardens.user_id = %s AND planted_in_gardens.freetext = 'no'", (months_of_year[j], int(garden_ids_from_user[i]["garden_id"]), int(session["user_id"])),)
                        monthly_plants_nonfreetext = cur.fetchall()
                        cur.execute("SELECT freetext_plants.plant_name, planted_in_gardens.number_of_plants, planted_in_gardens.months_to_remain_planted, freetext_plants.metres_squared_required, freetext_plants.perennial_or_annual FROM gardens INNER JOIN planted_in_gardens ON gardens.garden_id = planted_in_gardens.garden_id INNER JOIN freetext_plants ON planted_in_gardens.plant_id = freetext_plants.plant_id WHERE planted_in_gardens.month_planted = %s AND gardens.garden_id = %s AND gardens.user_id = %s AND planted_in_gardens.freetext = 'yes'", (months_of_year[j], int(garden_ids_from_user[i]["garden_id"]), int(session["user_id"])),)
                        monthly_plants_freetext = cur.fetchall()
            
                        for k in range(len(monthly_plants_nonfreetext)):
                            plants_planted_each_month_of_year[j].append(monthly_plants_nonfreetext[k])
                        for k in range(len(monthly_plants_freetext)):
                            plants_planted_each_month_of_year[j].append(monthly_plants_freetext[k])
    
                        for k in range(len(plants_planted_each_month_of_year[j])):
                            plant_months_to_remain_planted = int(plants_planted_each_month_of_year[j][k]["months_to_remain_planted"])
                            plant_perennal_or_annual = plants_planted_each_month_of_year[j][k]["perennial_or_annual"]
                            if plant_perennal_or_annual == "perennial":
                                for l in range(j, 12):
                                    plants_growing_each_month_of_year[l].append(plants_planted_each_month_of_year[j][k])
                            elif plant_perennal_or_annual == "annual":
                                for l in range(plant_months_to_remain_planted):
                                    plants_growing_each_month_of_year[j + l].append(plants_planted_each_month_of_year[j][k])
    
                    for j in range(12):
                        planted_gardens_from_user[i].append(plants_growing_each_month_of_year[j])
    
                    for j in range(12):
                        for k in range(len(planted_gardens_from_user[i][j])):
                            all_plant_names_in_garden[i].append(planted_gardens_from_user[i][j][k]["plant_name"])
    
                    all_plant_names_in_garden[i] = list(set(all_plant_names_in_garden[i]))
                    total_different_plants_in_garden[i] = len(all_plant_names_in_garden[i])
    
                    garden_size = int(garden_ids_from_user[i]["garden_size_metres_squared"])
                    for j in range(12):
                        space_remaining_each_month[i][j] = garden_size
                    for j in range(12):
                        for k in range(len(planted_gardens_from_user[i][j])):
                            plant_space_required = float(planted_gardens_from_user[i][j][k]["metres_squared_required"]) * float(planted_gardens_from_user[i][j][k]["number_of_plants"])
                            space_remaining_each_month[i][j] -= plant_space_required
    
            return render_template("index.html", space_remaining_each_month=space_remaining_each_month, all_plant_names_in_garden=all_plant_names_in_garden, total_different_plants_in_garden=total_different_plants_in_garden, garden_ids_from_user=garden_ids_from_user, planted_gardens_from_user=planted_gardens_from_user, number_of_gardens_from_user=number_of_gardens_from_user, admin_id=admin_id, months_of_year=months_of_year)
  

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    with db.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", ('admin',))
        admin = cur.fetchall()
        if len(admin) == 1 and session["user_id"] == admin[0]["user_id"]:
            admin_id = admin[0]["user_id"]
            if request.method == "POST":
                # Insert new data from admin page into database
    
                if request.form.get("add_plant_button"):
                    if not request.form.get("plant_name_add"):
                        return error("Must provide plant name.", 400)
                    elif not request.form.get("duration_to_maturity_months_add"):
                        return error("Must provide duration to maturity (months).", 400)
                    elif not request.form.get("plant_spacing_metres_add"):
                        return error("Must provide spacing (metres).", 400)
                    elif not request.form.get("metres_squared_required_add"):
                        return error("Must provide space required (metres squared).", 400)
                    elif not request.form.get("perennial_or_annual_add"):
                        return error("Must specify perennial or annual.", 400)
    
                    if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_add")) or not request.form.get("plant_name_add").islower():
                        return error("Plant name must be lowercase and alphabetical.", 400)
    
                    try:
                        duration_to_maturity_months_add = int(request.form.get("duration_to_maturity_months_add"))
                    except ValueError:
                        return error("Duration to maturity (months) must be integer.", 400)
    
                    if duration_to_maturity_months_add <= 0:
                            return error("Duration to maturity (months) must be positive number.", 400)
    
                    try:
                        plant_spacing_metres_add = int(request.form.get("plant_spacing_metres_add"))
                    except ValueError:
                        try:
                            plant_spacing_metres_add = float(request.form.get("plant_spacing_metres_add"))
                        except ValueError:
                            return error("Spacing (metres) must be integer or decimal number.", 400)
    
                    if plant_spacing_metres_add <= 0:
                        return error("Spacing (metres) must be positive number.", 400)
    
                    try:
                        metres_squared_required_add = int(request.form.get("metres_squared_required_add"))
                    except ValueError:
                        try:
                            metres_squared_required_add = float(request.form.get("metres_squared_required_add"))
                        except ValueError:
                            return error("Required space per plant (metres squared) must be integer or decimal number.", 400)
    
                    if metres_squared_required_add <= 0:
                        return error("Required space per plant (metres squared) must be positive number.", 400)
    
                    if request.form.get("perennial_or_annual_add") != "perennial" and request.form.get("perennial_or_annual_add") != "annual":
                        return error("Must select either perennial or annual.", 400)
    
                    january_add = "no"
                    february_add = "no"
                    march_add = "no"
                    april_add = "no"
                    may_add = "no"
                    june_add = "no"
                    july_add = "no"
                    august_add = "no"
                    september_add = "no"
                    october_add = "no"
                    november_add = "no"
                    december_add = "no"
    
                    if request.form.get("january_add") == "yes":
                        january_add = "yes"
                    if request.form.get("february_add") == "yes":
                        february_add = "yes"
                    if request.form.get("march_add") == "yes":
                        march_add = "yes"
                    if request.form.get("april_add") == "yes":
                        april_add = "yes"
                    if request.form.get("may_add") == "yes":
                        may_add = "yes"
                    if request.form.get("june_add") == "yes":
                        june_add = "yes"
                    if request.form.get("july_add") == "yes":
                        july_add = "yes"
                    if request.form.get("august_add") == "yes":
                        august_add = "yes"
                    if request.form.get("september_add") == "yes":
                        september_add = "yes"
                    if request.form.get("october_add") == "yes":
                        october_add = "yes"
                    if request.form.get("november_add") == "yes":
                        november_add = "yes"
                    if request.form.get("december_add") == "yes":
                        december_add = "yes"
    
                    cur.execute(
                        "INSERT INTO plants (plant_name, duration_to_maturity_months, plant_spacing_metres, metres_squared_required, perennial_or_annual, january, february, march, april, may, june, july, august, september, october, november, december) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                            request.form.get("plant_name_add"),
                            duration_to_maturity_months_add,
                            plant_spacing_metres_add,
                            metres_squared_required_add,
                            request.form.get("perennial_or_annual_add"),
                            january_add,
                            february_add,
                            march_add,
                            april_add,
                            may_add,
                            june_add,
                            july_add,
                            august_add,
                            september_add,
                            october_add,
                            november_add,
                            december_add
                        )
                    )
                    db.commit()
                    return redirect("/admin")
    
                if request.form.get("remove_plant_button"):
                    if not request.form.get("plant_name_remove"):
                        return error("Must provide plant name.", 400)
                    if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_remove")) or not request.form.get("plant_name_remove").islower():
                        return error("Plant name must be lowercase and alphabetical.", 400)
    
                    cur.execute("SELECT plant_name FROM plants WHERE freetext = %s", ('no',))
                    plant_names = cur.fetchall()

                    cur.execute(
                        """
                        SELECT plants.plant_name 
                        FROM plants 
                        INNER JOIN freetext_plants_users 
                        ON plants.plant_id = freetext_plants_users.plant_id 
                        WHERE plants.freetext = %s AND freetext_plants_users.user_id = %s
                        """,
                        ('yes', int(session["user_id"]))  
                    )
                    freetext_plant_names_from_user = cur.fetchall()

                    is_plant_in_db = False
    
                    for i in range(len(plant_names)):
                        if plant_names[i]["plant_name"] == request.form.get("plant_name_remove"):
                            is_plant_in_db = True
    
                    for i in range(len(freetext_plant_names_from_user)):
                        if freetext_plant_names_from_user[i]["plant_name"] == request.form.get("plant_name_remove"):
                            is_plant_in_db = True
    
                    if is_plant_in_db == False:
                        return error("Plant name not found.", 400)
    
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_remove"),))
                    plant_id = cur.fetchone()
    
                    cur.execute("DELETE FROM plants WHERE plant_id = %s", (plant_id[0]["plant_id"],))
                    cur.execute("DELETE FROM planted_in_gardens WHERE plant_id = %s", (plant_id[0]["plant_id"],))
                    cur.execute("DELETE FROM companion_friends WHERE plant_id_a = %s OR plant_id_b = %s", (plant_id[0]["plant_id"], plant_id[0]["plant_id"]))
                    cur.execute("DELETE FROM companion_enemies WHERE plant_id_a = %s OR plant_id_b = %s", (plant_id[0]["plant_id"], plant_id[0]["plant_id"]))
                    
                    db.commit()
                    
                    return redirect("/admin")
    
                if request.form.get("update_plant_button"):
                    if not request.form.get("plant_name_update"):
                        return error("Must provide plant name.", 400)
                    elif not request.form.get("duration_to_maturity_months_update"):
                        return error("Must provide duration to maturity (months).", 400)
                    elif not request.form.get("plant_spacing_metres_update"):
                        return error("Must provide spacing (metres).", 400)
                    elif not request.form.get("metres_squared_required_update"):
                        return error("Must provide space required (metres squared).", 400)
                    elif not request.form.get("perennial_or_annual_update"):
                        return error("Must specify perennial or annual.", 400)
    
                    if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_update")) or not request.form.get("plant_name_update").islower():
                        return error("Plant name must be lowercase and alphabetical.", 400)
    
                    plant_name = request.form.get("plant_name_update")
                    if request.form.get("new_plant_name_update"):
                        if not all(x.isalpha() or x.isspace() for x in request.form.get("new_plant_name_update")) or not request.form.get("new_plant_name_update").islower():
                            return error("New plant name must be lowercase and alphabetical.", 400)
                        plant_name = request.form.get("new_plant_name_update")
    
                    try:
                        duration_to_maturity_months_update = int(request.form.get("duration_to_maturity_months_update"))
                    except ValueError:
                        return error("Duration to maturity (months) must be integer.", 400)
    
                    if duration_to_maturity_months_update <= 0:
                            return error("Duration to maturity (months) must be positive number.", 400)
    
                    try:
                        plant_spacing_metres_update = int(request.form.get("plant_spacing_metres_update"))
                    except ValueError:
                        try:
                            plant_spacing_metres_update = float(request.form.get("plant_spacing_metres_update"))
                        except ValueError:
                            return error("Spacing (metres) must be integer or decimal number.", 400)
    
                    if plant_spacing_metres_update <= 0:
                        return error("Spacing (metres) must be positive number.", 400)
    
                    try:
                        metres_squared_required_update = int(request.form.get("metres_squared_required_update"))
                    except ValueError:
                        try:
                            metres_squared_required_update = float(request.form.get("metres_squared_required_update"))
                        except ValueError:
                            return error("Required space per plant (metres squared) must be integer or decimal number.", 400)
    
                    if metres_squared_required_update <= 0:
                        return error("Required space per plant (metres squared) must be positive number.", 400)
    
                    if request.form.get("perennial_or_annual_update") != "perennial" and request.form.get("perennial_or_annual_update") != "annual":
                        return error("Must select either perennial or annual.", 400)
    
                    january_update = "no"
                    february_update = "no"
                    march_update = "no"
                    april_update = "no"
                    may_update = "no"
                    june_update = "no"
                    july_update = "no"
                    august_update = "no"
                    september_update = "no"
                    october_update = "no"
                    november_update = "no"
                    december_update = "no"
    
                    if request.form.get("january_update") == "yes":
                        january_add = "yes"
                    if request.form.get("february_update") == "yes":
                        february_add = "yes"
                    if request.form.get("march_update") == "yes":
                        march_add = "yes"
                    if request.form.get("april_update") == "yes":
                        april_add = "yes"
                    if request.form.get("may_update") == "yes":
                        may_add = "yes"
                    if request.form.get("june_update") == "yes":
                        june_add = "yes"
                    if request.form.get("july_update") == "yes":
                        july_add = "yes"
                    if request.form.get("august_update") == "yes":
                        august_add = "yes"
                    if request.form.get("september_update") == "yes":
                        september_add = "yes"
                    if request.form.get("october_update") == "yes":
                        october_add = "yes"
                    if request.form.get("november_update") == "yes":
                        november_add = "yes"
                    if request.form.get("december_update") == "yes":
                        december_add = "yes"
    
                    cur.execute(
                        "UPDATE plants SET plant_name = %s, duration_to_maturity_months = %s, plant_spacing_metres = %s, metres_squared_required = %s, perennial_or_annual = %s, january = %s, february = %s, march = %s, april = %s, may = %s, june = %s, july = %s, august = %s, september = %s, october = %s, november = %s, december = %s WHERE plant_name = %s",
                        (
                            plant_name,
                            duration_to_maturity_months_update,
                            plant_spacing_metres_update,
                            metres_squared_required_update,
                            request.form.get("perennial_or_annual_update"),
                            january_update,
                            february_update,
                            march_update,
                            april_update,
                            may_update,
                            june_update,
                            july_update,
                            august_update,
                            september_update,
                            october_update,
                            november_update,
                            december_update,
                            request.form.get("plant_name_update"),
                        ),
                    )
                    db.commit()
                  
                    return redirect("/admin")
    
                if request.form.get("add_companion_friends_button"):
                    if not request.form.get("plant_name_add_friend_a"):
                        return error("Must provide plant A name.", 400)
                    elif not request.form.get("plant_name_add_friend_b"):
                        return error("Must provide plant B name.", 400)
    
                    if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_add_friend_a")) or not request.form.get("plant_name_add_friend_a").islower():
                        return error("Plant A name must be lowercase and alphabetical.", 400)
                    elif not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_add_friend_b")) or not request.form.get("plant_name_add_friend_b").islower():
                        return error("Plant B name must be lowercase and alphabetical.", 400)
    
                    cur.execute("SELECT plant_name FROM plants")
                    plant_names = cur.fetchall()
                    cur.execute("SELECT plant_name FROM freetext_plants WHERE user_id = %s", (int(session["user_id"]),))
                    freetext_plant_names_from_user = cur.fetchall()
                        
                    is_plant_a_in_db = False
                    is_plant_b_in_db = False
                    for i in range(len(plant_names)):
                        if plant_names[i]["plant_name"] == request.form.get("plant_name_add_friend_a"):
                            is_plant_a_in_db = True
                        if plant_names[i]["plant_name"] == request.form.get("plant_name_add_friend_b"):
                            is_plant_b_in_db = True
    
                    for i in range(len(freetext_plant_names_from_user)):
                        if freetext_plant_names_from_user[i]["plant_name"] == request.form.get("plant_name_add_friend_a"):
                            is_plant_a_in_db = True
                        if freetext_plant_names_from_user[i]["plant_name"] == request.form.get("plant_name_add_friend_b"):
                            is_plant_b_in_db = True
    
                    if not is_plant_a_in_db:
                        return error("Plant A name not found. Consider adding as freetext before trying again.", 400)
                    if not is_plant_b_in_db:
                        return error("Plant B name not found. Consider adding as freetext before trying again.", 400)
  
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_add_friend_a"),))
                    plant_a_id = cur.fetchone()
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_add_friend_b"),))
                    plant_b_id = cur.fetchone()
    
                    cur.execute(
                        "INSERT INTO companion_friends (plant_id_a, plant_id_b) VALUES (%s, %s)",
                        (plant_a_id["plant_id"], plant_b_id["plant_id"])
                    )
                    db.commit()

                    return redirect("/admin")
    
                if request.form.get("remove_companion_friends_button"):
                    if not request.form.get("plant_name_remove_friend_a"):
                        return error("Must provide plant A name.", 400)
                    elif not request.form.get("plant_name_remove_friend_b"):
                        return error("Must provide plant B name.", 400)
    
                    if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_remove_friend_a")) or not request.form.get("plant_name_remove_friend_a").islower():
                        return error("Plant A name must be lowercase and alphabetical.", 400)
                    elif not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_remove_friend_b")) or not request.form.get("plant_name_remove_friend_b").islower():
                        return error("Plant B name must be lowercase and alphabetical.", 400)
    
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_remove_friend_a"),))
                    plant_a_id = cur.fetchone()

                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_remove_friend_b"),))
                    plant_b_id = cur.fetchone()

                    cur.execute("SELECT * FROM companion_friends")
                    companion_friends = cur.fetchall()
                    
                    are_plants_a_and_b_friends = False
    
                    for i in range(len(companion_friends)):
                        if companion_friends[i]["plant_id_a"] == plant_a_id[0]["plant_id"]:
                            if companion_friends[i]["plant_id_b"] == plant_b_id[0]["plant_id"]:
                                are_plants_a_and_b_friends = True
                        if companion_friends[i]["plant_id_b"] == plant_a_id[0]["plant_id"]:
                            if companion_friends[i]["plant_id_a"] == plant_b_id[0]["plant_id"]:
                                are_plants_a_and_b_friends = True
    
                    if not are_plants_a_and_b_friends:
                        return error("Plants A and B are not friends.", 400)
    
                    cur.execute("DELETE FROM companion_friends WHERE plant_id_a = %s AND plant_id_b = %s", (plant_a_id[0]["plant_id"], plant_b_id[0]["plant_id"]))
                    cur.execute("DELETE FROM companion_friends WHERE plant_id_a = %s AND plant_id_b = %s", (plant_b_id[0]["plant_id"], plant_a_id[0]["plant_id"]))   
                    db.commit()
                  
                    return redirect("/admin")
    
                if request.form.get("add_companion_enemies_button"):
                    if not request.form.get("plant_name_add_enemy_a"):
                        return error("Must provide plant A name.", 400)
                    elif not request.form.get("plant_name_add_enemy_b"):
                        return error("Must provide plant B name.", 400)
    
                    if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_add_enemy_a")) or not request.form.get("plant_name_add_enemy_a").islower():
                        return error("Plant A name must be lowercase and alphabetical.", 400)
                    elif not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_add_enemy_b")) or not request.form.get("plant_name_add_enemy_b").islower():
                        return error("Plant B name must be lowercase and alphabetical.", 400)
    
                    cur.execute("SELECT plant_name from plants")
                    plant_names = cur.fetchall()

                  
                    cur.execute("SELECT plant_name FROM freetext_plants WHERE user_id = %s", (int(session["user_id"]),))
                    freetext_plant_names_from_user = cur.fetchall()
    
                    is_plant_a_in_db = False
                    is_plant_b_in_db = False
                    for i in range(len(plant_names)):
                        if plant_names[i]["plant_name"] == request.form.get("plant_name_add_enemy_a"):
                            is_plant_a_in_db = True
                        if plant_names[i]["plant_name"] == request.form.get("plant_name_add_enemy_b"):
                            is_plant_b_in_db = True
    
                    for i in range(len(freetext_plant_names_from_user)):
                        if freetext_plant_names_from_user[i]["plant_name"] == request.form.get("plant_name_add_enemy_a"):
                            is_plant_a_in_db = True
                        if freetext_plant_names_from_user[i]["plant_name"] == request.form.get("plant_name_add_enemy_b"):
                            is_plant_b_in_db = True
    
                    if not is_plant_a_in_db:
                        return error("Plant A name not found. Consider adding as freetext before trying again.", 400)
                    if not is_plant_b_in_db:
                        return error("Plant B name not found. Consider adding as freetext before trying again.", 400)
    
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_add_enemy_a"),))
                    plant_a_id = cur.fetchall() 

                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_add_enemy_b"),))
                    plant_b_id = cur.fetchall()

                    cur.execute("INSERT INTO companion_enemies (plant_id_a, plant_id_b) VALUES (%s, %s)", (plant_a_id[0]["plant_id"], plant_b_id[0]["plant_id"]))
                    db.commit()

                    return redirect("/admin")
    
                if request.form.get("remove_companion_enemies_button"):
                    if not request.form.get("plant_name_remove_enemy_a"):
                        return error("Must provide plant A name.", 400)
                    elif not request.form.get("plant_name_remove_enemy_b"):
                        return error("Must provide plant B name.", 400)
    
                    if not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_remove_enemy_a")) or not request.form.get("plant_name_remove_enemy_a").islower():
                        return error("Plant A name must be lowercase and alphabetical.", 400)
                    elif not all(x.isalpha() or x.isspace() for x in request.form.get("plant_name_remove_enemy_b")) or not request.form.get("plant_name_remove_enemy_b").islower():
                        return error("Plant B name must be lowercase and alphabetical.", 400)
    
                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = %s", (request.form.get("plant_name_remove_enemy_a"),))
                    plant_a_id = cur.fetchall()

                    cur.execute("SELECT plant_id FROM plants WHERE plant_name = ?", (request.form.get("plant_name_remove_enemy_b"),))
                    plant_b_id = cur.fetchall() 

                    cur.execute("SELECT * FROM companion_enemies")
                    companion_enemies = cur.fetchall()
    
                    are_plants_a_and_b_enemies = False
    
                    for i in range(len(companion_friends)):
                        if companion_enemies[i]["plant_id_a"] == plant_a_id[0]["plant_id"]:
                            if companion_enemies[i]["plant_id_b"] == plant_b_id[0]["plant_id"]:
                                are_plants_a_and_b_friends = True
                        if companion_enemies[i]["plant_id_b"] == plant_a_id[0]["plant_id"]:
                            if companion_enemies[i]["plant_id_a"] == plant_b_id[0]["plant_id"]:
                                are_plants_a_and_b_enemies = True
    
                    if not are_plants_a_and_b_enemies:
                        return error("Plants A and B are not enemies.", 400)
    
                    cur.execute("DELETE FROM companion_enemies WHERE plant_id_a = ? AND plant_id_b = ?", (plant_a_id[0]["plant_id"], plant_b_id[0]["plant_id"]))
                    cur.execute("DELETE FROM companion_enemies WHERE plant_id_a = ? AND plant_id_b = ?", (plant_b_id[0]["plant_id"], plant_a_id[0]["plant_id"]))
                    db.commit()

                    return redirect("/admin")
    
            else:
                return render_template("admin.html", admin_id=admin_id)
    
        else:
            return error("You are not an admin.", 401)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    with db.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM users WHERE username = 'admin'");
        admin = cur.fetchall()
    
        if len(admin) == 1 and session["user_id"] == admin[0]["user_id"]:
            admin_id = admin[0]["user_id"]
    
        if request.method == "POST":
            if not request.form.get("username"):
                return error("Must provide username.", 400)
            elif not request.form.get("new_password"):
                return error("Must provide new password.", 400)
            elif not request.form.get("confirmation"):
                return error("Must provide password confirmation.", 400)
    
            if request.form.get("new_password") != request.form.get("confirmation"):
                return error("Passwords must match.", 400)
    
            hash_password = generate_password_hash(request.form.get("new_password"))
    
            cur.execute("UPDATE users SET hash_password = %s WHERE username = %s", (hash_password, request.form.get("username")))
            db.commit()
          
            return redirect("/")
    
        else:
            return render_template("change_password.html", admin_id=admin_id)


@app.route("/information")
@login_required
def information():
     with db.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM users WHERE username = 'admin'");
        admin = cur.fetchall()
         
        if len(admin) == 1 and session["user_id"] == admin[0]["user_id"]:
            admin_id = admin[0]["user_id"]

        cur.execute("SELECT plant_name, duration_to_maturity_months, plant_spacing_metres, metres_squared_required, perennial_or_annual, january, february, march, april, may, june, july, august, september, october, november, december FROM plants ORDER BY plant_name")
        plants = cur.fetchall()
        cur.execute("SELECT freetext_plants.plant_name, freetext_plants.duration_to_maturity_months, freetext_plants.plant_spacing_metres, freetext_plants.metres_squared_required, freetext_plants.perennial_or_annual, freetext_plants.january, freetext_plants.february, freetext_plants.march, freetext_plants.april, freetext_plants.may, freetext_plants.june, freetext_plants.july, freetext_plants.august, freetext_plants.september, freetext_plants.october, freetext_plants.november, freetext_plants.december FROM freetext_plants WHERE freetext_plants.user_id = %s ORDER BY freetext_plants.plant_name", (int(session["user_id"]),))
        freetext_plants_from_user = cur.fetchall()
         
        companion_friends = []
        cur.execute("SELECT * FROM companion_friends")
        companion_friends_ids = cur.fetchall()
         
        if len(companion_friends_ids) != 0:
            cur.execute("SELECT plants_friends_a.plant_name AS companion_friends_plant_a, plants_friends_b.plant_name AS companion_friends_plant_b FROM companion_friends INNER JOIN plants AS plants_friends_a ON companion_friends.plant_id_a = plants_friends_a.plant_id INNER JOIN plants AS plants_friends_b ON companion_friends.plant_id_b = plants_friends_b.plant_id")
            companion_friends = cur.fetchall()  
            
            deleted_row_quantity = 0
            original_range_for_i = len(companion_friends) - 1
    
            deleted_rows = []
            companion_friends_buffer = []
    
            for i in range(original_range_for_i):
                if i == original_range_for_i - deleted_row_quantity:
                    break
                for j in range(i + 1, original_range_for_i + 1):
                    if companion_friends[i]["companion_friends_plant_a"] == companion_friends[j]["companion_friends_plant_a"]:
                        if companion_friends[i]["companion_friends_plant_b"] == companion_friends[j]["companion_friends_plant_b"]:
                            deleted_rows.append(companion_friends[j])
                            deleted_row_quantity += 1
                            break
                    elif companion_friends[i]["companion_friends_plant_a"] == companion_friends[j]["companion_friends_plant_b"]:
                        if companion_friends[i]["companion_friends_plant_b"] == companion_friends[j]["companion_friends_plant_a"]:
                            deleted_rows.append(companion_friends[j])
                            deleted_row_quantity += 1
                            break
    
            for i in range(len(companion_friends)):
                if companion_friends[i] not in deleted_rows:
                    companion_friends_buffer.append(companion_friends[i])
    
            companion_friends = companion_friends_buffer
    
        companion_enemies = []
        cur.execute("SELECT * FROM companion_enemies")
        companion_enemies_ids = cur.fetchall()
         
        if len(companion_enemies_ids) != 0:
            cur.execute("SELECT plants_enemies_a.plant_name AS companion_enemies_plant_a, plants_enemies_b.plant_name AS companion_enemies_plant_b FROM companion_enemies INNER JOIN plants AS plants_enemies_a ON companion_enemies.plant_id_a = plants_enemies_a.plant_id INNER JOIN plants AS plants_enemies_b ON companion_enemies.plant_id_b = plants_enemies_b.plant_id")
            companion_enemies = cur.fetchall()
                
            deleted_row_quantity = 0
            original_range_for_i = len(companion_enemies) - 1
    
            deleted_rows = []
            companion_enemies_buffer = []
    
            for i in range(original_range_for_i):
                if i == original_range_for_i - deleted_row_quantity:
                    break
                for j in range(i + 1, original_range_for_i + 1):
                    if companion_enemies[i]["companion_enemies_plant_a"] == companion_enemies[j]["companion_enemies_plant_a"]:
                        if companion_enemies[i]["companion_enemies_plant_b"] == companion_enemies[j]["companion_enemies_plant_b"]:
                            deleted_rows.append(companion_enemies[j])
                            deleted_row_quantity += 1
                            break
                    elif companion_enemies[i]["companion_enemies_plant_a"] == companion_enemies[j]["companion_enemies_plant_b"]:
                        if companion_enemies[i]["companion_enemies_plant_b"] == companion_enemies[j]["companion_enemies_plant_a"]:
                            deleted_rows.append(companion_enemies[j])
                            deleted_row_quantity += 1
                            break
    
            for i in range(len(companion_enemies)):
                if companion_enemies[i] not in deleted_rows:
                    companion_enemies_buffer.append(companion_enemies[i])
    
            companion_enemies = companion_enemies_buffer
    
        return render_template("information.html", plants=plants, freetext_plants_from_user=freetext_plants_from_user, companion_friends=companion_friends, companion_enemies=companion_enemies, admin_id=admin_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return error("Must provide username.", 400)
        elif not request.form.get("password"):
            return error("Must provide password.", 400)

        with db.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
            rows = cur.fetchall()
            
        if len(rows) != 1 or not check_password_hash(rows[0]["hash_password"], request.form.get("password")):
            return error("Invalid username and/or password", 400)

        session["user_id"] = rows[0]["user_id"]
 
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
  
    if request.method == "POST":
        if not request.form.get("username"):
            return error("Must provide username.", 400)
        elif not request.form.get("password"):
            return error("Must provide password.", 400)
        elif not request.form.get("confirmation"):
            return error("Must provide password confirmation.", 400)

        with db.cursor(cursor_factory = psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
            rows = cur.fetchall()
  
            if len(rows) != 0:
                return error("Username already taken.", 400)
            elif request.form.get("password") != request.form.get("confirmation"):
                return error("Passwords must match.", 400)
    
            hash_password = generate_password_hash(request.form.get("password"))
    
            cur.execute("INSERT INTO users (username, hash_password) VALUES (%s, %s)", (request.form.get("username"), hash_password))
            db.commit()
      
        return redirect("/login")

    else:
        return render_template("register.html")

@app.route("/weather", methods=["GET", "POST"])
@login_required
def weather():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/bom"

    params = {
            "latitude": -37.8045,
            "longitude": 144.979,
            "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
            "timezone": "Australia/Sydney"
        }
    freetext_location = "no"
    latitude = None
    longitude = None

    if request.method == "POST":
        if request.form.get("add_location_button"):
            if not request.form.get("latitude"):
                return error("Must provide latitude.", 400)
            elif not request.form.get("longitude"):
                return error("Must provide longitude.", 400)

            try:
                latitude = int(request.form.get("latitude"))
            except ValueError:
                try:
                    latitude = float(request.form.get("latitude"))
                except ValueError:
                    return error("Latitude must be integer or decimal number.", 400)

            if latitude < -90 or latitude > 90:
                return error("Latitude must be between -90 and 90.", 400)

            try:
                longitude = int(request.form.get("longitude"))
            except ValueError:
                try:
                    longitude = float(request.form.get("longitude"))
                except ValueError:
                    return error("Longitude must be integer or decimal number.", 400)

            if longitude < -180 or longitude > 180:
                return error("Longitude must be between -180 and 180.", 400)

            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
                "timezone": "Australia/Sydney"
            }

            freetext_location = "yes"


    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(2).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["rain_sum"] = daily_rain_sum

    daily_dataframe = pd.DataFrame(data = daily_data)

    return render_template("weather.html", latitude=latitude, longitude=longitude, freetext_location=freetext_location, daily_dataframe=daily_dataframe)

