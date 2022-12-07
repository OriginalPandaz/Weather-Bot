import os
import discord
import requests
import json

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def fetchWeatherJson():
  url = "https://api.open-meteo.com/v1/forecast?latitude=34.05&longitude=-118.24&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&timezone=America%2FLos_Angeles"
  resp = requests.get(url)
  json_data = json.loads(resp.text)
  return json_data

def get_weekly_temperature():
  json_data = fetchWeatherJson()
  minTemp = "temperature_2m_min"
  maxTemp = "temperature_2m_max"
  city = "Los Angeles\n"
  dailyWeather = {}
  for index, day in enumerate(json_data["daily"]["time"]):
    dailyWeather[day] = [
      int(json_data["daily"][minTemp][index]), int(json_data["daily"][maxTemp][index])
    ]
  res = city
  
  for key, value in dailyWeather.items():
    res += "{:<15} {:<11} {:<5}\n".format(key + ":", str(value[0]) + "°F", str(value[1]) + '°F')

  return res

def get_todays_temperature():
  json_data = fetchWeatherJson()
  minTemp = "temperature_2m_min"
  maxTemp = "temperature_2m_max"
  city = "Los Angeles"
  res = "Todays Temperature in {city} is\n".format(city=city)
  res += str(int(json_data["daily"][maxTemp][0])) + "°F " + str(int(json_data["daily"][minTemp][0])) + "°F "
  return res
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$weather'):
    weekly_temps = get_weekly_temperature()
    await message.channel.send(weekly_temps)

  if message.content.startswith('$today'):
    todays_temp = get_todays_temperature()
    await message.channel.send(todays_temp)
    
client.run(os.environ['TOKEN'])
