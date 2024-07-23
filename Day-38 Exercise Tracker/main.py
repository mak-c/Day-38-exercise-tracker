import requests
import datetime
import os

today_date = datetime.datetime.now().strftime('%d/%m/%Y')
today_time = datetime.datetime.now().strftime('%X')

WEIGHT_KG = 68
HEIGHT_CM = 168
AGE = 28

APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

sheet_endpoint = os.environ['sheet_endpoint']
sheet_token = os.environ['sheet_token']


exercise_text = input("Enter exercises completed: ")

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

parameters = {
    'query': exercise_text,
    'weight_kg': WEIGHT_KG,
    'height_cm': HEIGHT_CM,
    'age': AGE,
}

response = requests.post(url=exercise_endpoint, headers=headers, json=parameters)
response.raise_for_status()
exercise_data = response.json()

for exercise in exercise_data['exercises']:
    sheet_inputs = {
        'workout': {
            'date': today_date,
            'time': today_time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }
    sheet_header = {
        'Authorization': f"Bearer {sheet_token}",
    }
    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs, headers=sheet_header)
    sheet_response.raise_for_status()




