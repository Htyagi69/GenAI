from dotenv import load_dotenv
import os
from google import genai
from rich.console import Console

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

console=Console()

def llm():
  console.print("Welcome [bold cyan] to llm [italic red] Type exit to quit\n")
  while True:
    user_input=input(f">> ")
    try:
      if user_input.lower() in ["exit","end","quit"]:
         console.print("\n[italic red]Goodbye!![/italic red]\n")
         break
  
      if not user_input.strip():
         continue
  
      interaction=client.models.generate_content_stream(
          model="gemini-2.5-flash",
          contents=user_input,
      )
      
      # print(interaction.output_text)
      for event in interaction:
          console.print(f"[bold magenta]{event.text}",end="")
          # console.print(event.text,end="",markup=False)
      print("\n\n")

    except :  
       print("Try after sometime")

llm()
