import paho.mqtt.client as mqtt
import json
import logging
import time 
import requests
from weather_api_request import get_weather_data

mqttBroker = "mqtt.eclipseprojects.io"
topic="TEST"
previous_temperature = None
# Function to handle received messages
def client_side_execution(client, userdata, message):
    # Decode the message payload (assuming JSON)
    data = json.loads(message.payload.decode())
    print ("\ndata in-type ",type(data))
    # Extract desired values
    print(f"Received data: {data}")
    if isinstance(data, dict) and "sensors" in data:
        # Extraire la température du dictionnaire "sensors"
        current_temperature = data["sensors"].get("temperature")

        # Vérifier s'il y a une température précédente
        if previous_temperature is not None:
            # Comparer la température actuelle avec la température précédente
            if current_temperature is not None and current_temperature != previous_temperature:
                print(f"Temperature has changed! Previous: {previous_temperature}, Current: {current_temperature}")
                # Ajouter ici le code pour prendre des mesures en cas de changement de température

        # Mettre à jour la température précédente
        previous_temperature = current_temperature


tunis_latitude = 36.8065
tunis_longitude = 10.1815

# Appelez la fonction pour obtenir les données météorologiques
weather_data_tunis = get_weather_data(tunis_latitude, tunis_longitude)

# Vérifiez si les données ont été obtenues avec succès
if weather_data_tunis:
    print("Weather data for Tunis:")
    print(f"Temperature at 2m: {weather_data_tunis['hourly']['temperature_2m'][0]}°C")
    print(f"Precipitation: {weather_data_tunis['hourly']['precipitation'][0]} mm")
else:
    print("Unable to fetch weather data for Tunis.")


client = mqtt.Client("test1")
client.on_message = client_side_execution
client.connect(mqttBroker)
client.subscribe(topic)
client.loop_forever()

