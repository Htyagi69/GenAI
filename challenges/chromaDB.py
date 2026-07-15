import os
from google import genai
from dotenv import load_dotenv
import chromadb

load_dotenv()

chroma_client = chromadb.PersistentClient(path="../chroma_db")

collection=chroma_client.get_or_create_collection(name="docs")

data=[]
docums=["python","football","cooking","ml","travel","movie","ai","music","space","history","physics","dogs","javascript","cats","cars"]

for doc in docums:
    try:
      with open(f"./files/{doc}.txt","r",encoding="utf-8") as f:
        data.append(f.read())
    except Exception as e:
      print(e)

print(data)

collection.add(
    ids=["id1","id2","id3","id4","id5","id6","id7","id8","id9","id10","id11","id12","id13","id14","id15"],
    documents=data
)

user_input=input(f">> ")
result=collection.query(
    query_texts=[user_input],
    n_results=3
)

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

prompt=f"""
  you are an helful assistant.
  Answer the following question with the given context below.

  if answer is not prsent in context,say:
  "I dont Know the answer based on given context"
  Question:
  {user_input}

  Context:
  {result["documents"][0]}

"""

response=client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=prompt,
)

for res in response:
    print(res.text,end="",flush=True)