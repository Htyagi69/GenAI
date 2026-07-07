import os
from dotenv import load_dotenv
from google import genai
import pathlib

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
try:
  userInput=input("path:")
  path=pathlib.Path(userInput)
  if not path.exists():
     raise FileNotFoundError(f"{path} file not found" )
#   myFile=client.files.upload(file=path)
  
  myFile=path.read_text(encoding="utf-8")
  Summarize_prompt={
     1:"You are a helpful teacher,use content as reference and explain in One paragraph. Use simple language, short sentences, and examples where appropriate.",
     2:"You are an Interviewer ,use content as reference and ask me 5 related questions ,you mmay increase difficulty according to you",
     3:"Read the content critically.Find out the major weakness, missing information and assumptions out of it",
     4:"You are a good Translator use content as reference and translate it in hindi with easy normal slang"}
  totalchoices=len(Summarize_prompt)

  print("\nExplain style\n")

  for no,pro in Summarize_prompt.items():
     print(f"No.{no}-{pro}")
  
  choice=int(input("choice No:"))
  option=1
  if 0<choice<=totalchoices:
     option=choice
  else:
     print("Invalid choice")
     exit()
  prompt=Summarize_prompt[choice]
  summarize=client.models.generate_content_stream(
      model="gemini-2.5-flash",
      contents=[myFile,prompt]
  )
  
  for word in summarize:
      print(word.text,end="")

except Exception as e:
   print(e)

# load_dotenv()

# filepath=pathlib.Path("hello.pdf")

# pdf_bytes=filepath.read_bytes()
# client=genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# prompt="Summarize this document"

# summarize=client.models.generate_content_stream(
#     model="gemini-2.5-flash",
#     contents=[
#          prompt,
#          types.Part.from_bytes(
#            data=pdf_bytes ,
#            mime_type="application/pdf"
#         ),
#     ]
# )

# for word in summarize:
#     print(word.text,end="")
