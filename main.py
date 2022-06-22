import requests
import os
from datetime import datetime

APP_ID = os.environ['nutritionix_appid']
APP_KEY = os.environ['nutritionix_key']


def process_exercise(input_message):
    endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }
    data_to_post = {
        "query": input_message,
        "gender": "MALE",
        "weight_kg": 72,
        "height_cm": 165,
        "age": 37
    }
    response = requests.post(url=endpoint, json=data_to_post, headers=headers)
    exercises = response.json()["exercises"]
    rows = []
    for exercise in exercises:
        name = exercise["name"]
        duration = exercise["duration_min"]
        cal = exercise["nf_calories"]
        now = datetime.now()
        my_tuple = (now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"),
                    name, duration, cal)
        rows.append(my_tuple)

    return rows


def update_sheet(rows):
    sheety_endpoint = "https://api.sheety.co/5610985b8f30ed6aa6908e5cea6fe8f1/myWorkoutLogs/sheet1"
    for row in rows:
        data = {
            "sheet1": {
                "date": row[0],
                "time": row[1],
                "exercise": row[2],
                "duration": row[3],
                "calories": row[4]
            }
        }
        print(data)

        response = requests.post(url=sheety_endpoint, json=data)
        print(response.text)


input_message = input("What exercises did you do today? : ")
update_sheet(process_exercise(input_message))
