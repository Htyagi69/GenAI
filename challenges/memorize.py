from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field 
from typing import List

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
 )
context=[]

class Skill(BaseModel):
   skill_name:str
   description:str

class data(BaseModel):
   name:str
   age:int=Field(description="the age of the person")
   profession:List[Skill]


try:
  while True:
   user_input=input(f">> ")
   if user_input.lower() in ["quit","close"]:
      print("chat closed")
      exit()
   print('\n')
   context.append(
      {  "role":"user",
         "parts":[{"text":user_input}]}
         )
   no=len(context)
   memo=client.models.generate_content(
       model="gemini-2.5-flash",
       contents=context,
       config={
          "response_mime_type":'application/json',
          "response_schema":data
       }
   )

   skill_data: data=memo.parsed
   print(f"Name:{skill_data.name}")
   print(f"Age:{skill_data.age}")
   for e in skill_data.profession:
     print(f"skillName:{e.skill_name}\n description:{e.description}")
   print("\n")
   context.append(
      {  "role":"model",
         "parts":[{"text":memo.text}]}
         )

except Exception as e:
   print(e)