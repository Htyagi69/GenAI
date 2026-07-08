from google import genai
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


weather_function = {
    "type": "function",
    "name":"get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}
calculate_function={
    "type":"function",
    "name":"get_calculation",
    "description":"Performs basic mathematical operations including addition (+), subtraction (-), multiplication (*), division (/), and modulo (%).",
    "parameters":{
        "type":"object",
        "properties":{
            "num1":{
                "type":"number",
                "description":"an integer e.g. 234"
            },
            "num2":{
                "type":"number",
                "description":"an integer e.g. 345"
            },
            "op":{
                "type":"string",
                "description":"an operator e.g. *"
            },
        },
        "required":["num1","num2","op"]
    },
}

time_function = {
    "type": "function",
    "name":"get_current_time",
    "description": "Gets the current time.",
     "parameters": {
                "type": "object",
                "properties": {},  # Empty object since no arguments are needed
                "required": []
            }
    }

API_KEY=os.getenv("OPEN_WEATHER_API_KEY")
def get_current_temperature(location):
  try:
     url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
     
     res=requests.get(url)
     if res.status_code==200:
      data=res.json()
    #  print(f"weather: {data}")
      return data
  except Exception as e:
      print(e)

def get_current_time():
   now=datetime.now()
   time=now.time()
   return time

def get_calculation(num1:int,num2:int,op):
    if op=='+':
        return num1+num2
    if op=='-':
        return num1-num2
    if op=='*':
        return num1*num2
    if op=='/':
        return num1/num2 if num2!=0 else "Error:Division by zero"
    if op=='%':
        return num1 % num2
    if op=='**':
        return num1 ** num2
    else:
        return 'invalid'

prompt=input(f">> ")

try:
  interaction=client.interactions.create(
      model="gemini-2.5-flash",
      input=prompt,
      tools=[weather_function,time_function,calculate_function]
  )
  
  has_call=False
  pending_step=None
  weather_data=None
  time=None
  calc=None

  for step in interaction.steps:
      if step.type=="function_call":
          has_call=True
          pending_step=step
          print(f"Function to call: {step.name}")
          print(f"Arguments: {step.arguments}")
  
          if step.name=='get_current_temperature':
           weather_data=get_current_temperature(**step.arguments)
           print(f"Function execution result:{weather_data['main']['temp']}°C")
          if step.name=='get_current_time':
             time=get_current_time()
          if step.name=='get_calculation':
             calc=get_calculation(**step.arguments)
             if calc=="invalid":
                print("Invalid opertion")
                exit()
  
# Weather
  if has_call :
    # weather
    if weather_data :
     func_result=f"the weather of {pending_step.arguments['location']} shows a temperature {weather_data['main']['temp']}"

    if time :
     func_result=f"the current time is {time}"

    if calc :
     num1=pending_step.arguments['num1']
     num2=pending_step.arguments['num2']
     op=pending_step.arguments['op']
     func_result=f"the solution with {num1} {op} {num2} is {calc}"

    final_res=client.interactions.create(
       model='gemini-2.5-flash',
       previous_interaction_id=interaction.id,
       input=[{
         'type':'function_result',
         "name":pending_step.name,
         "id":pending_step.id,
         "result":func_result
       }],
       # response_format={
       #    "type":"text",
       #    "mime_type":"application/json"
       # }
    )
    print(f"Final Response: {final_res.output_text}")
  
 
  
    if not has_call and interaction.output_text:
      print(f"{interaction.output_text}")
  
except Exception as e:
      print(e)

