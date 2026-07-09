import os
from google import genai
from dotenv import load_dotenv
import requests

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

weather_data={
    "type":"function",
    "name":"weather_forecast",
    "description":"Gets a location as an input and return the weather info",
    "parameters":{
        "type":"object",
        "properties":{
            "location":{
            "type":"string",
            "description": "The city name, e.g. San Francisco",
            }
        },
    },
    "required":["location"],
}

recommend_place={
    "type":"function",
    "name":"must_Visit",
    "description":"Returns real-time tourist attractions, parks, cinemas, museums, and nearby places for a city using the Geoapify Places API. Use this whenever the user asks for places to visit or recommendations.",
    "parameters":{
        "type":"object",
        "properties":{
            "location":{
            "type":"string",
            "description": "The city name, e.g. San Francisco",
        }
        },
    },
    "required":["location"],
}

OPEN_WEATHER_API_KEY=os.getenv("OPEN_WEATHER_API_KEY")

def weather_forecast(location:str):
   try:
     url=f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPEN_WEATHER_API_KEY}&units=metric"
     info=requests.get(url)
     res=info.json()
     return res
   except Exception as e:
      print(e)

PLACES_API_KEY=os.getenv("GEOAPIIFY_API_KEY")

def must_Visit(location:str):
  try:  
    GEO_location_url=f"https://api.geoapify.com/v1/geocode/search?text={location}&apiKey={PLACES_API_KEY}"
    coord=requests.get(GEO_location_url)
    res=coord.json()
    print(f"latitude: {res["features"][0]["properties"]["lat"]}")
    print(f"longitude: {res["features"][0]["properties"]["lon"]}")
    lat=res["features"][0]["properties"]["lat"]
    lon=res["features"][0]["properties"]["lon"]
    place_url=f"https://api.geoapify.com/v2/places?categories=entertainment.cinema,tourism,leisure.park&filter=circle:{lon},{lat},10000&limit=50&apiKey={PLACES_API_KEY}"
    info=requests.get(place_url)
    info=info.json()
    return info
  except Exception as e:
      print(e)


prompt=input(f">> ")

try:
   response=client.interactions.create(
       model="gemini-2.5-flash",
       input=prompt,
       tools=[weather_data,recommend_place]
   )
   
   Tools={
      "weather_forecast":weather_forecast,
      "must_Visit":must_Visit
   }
   has_call=False
   final_inp=[]
   
   for step in response.steps:
        
        if step.type=="function_call":
           print(f"Calling the Function: {step.name}")
           print(f"parameters: {step.arguments}")
           has_call=True
   
           result=Tools[step.name](**step.arguments)
           final_inp.append({
               "type":"function_result",
               "name":step.name,
               "id":step.id,
               "result":result,
           })
             
   if has_call :
       res=client.interactions.create(
               model="gemini-2.5-flash",
               previous_interaction_id=response.id,
               input=final_inp,
       )
       print("final_res",res.output_text)

except Exception as e:
      print(e)