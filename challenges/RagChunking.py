import os
from google import genai
from dotenv import load_dotenv
import chromadb

load_dotenv()

chroma_client=chromadb.PersistentClient(path="../chunk_db")

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

user_input=input(f">> ")

collection_full=chroma_client.get_or_create_collection(name="docums")
collection_2=chroma_client.get_or_create_collection(name="chunk_2")
collection_5=chroma_client.get_or_create_collection(name="chunk_5")

all_data=None
with open("./files/pythonfile.txt","r",encoding="utf-8") as f:
    all_data=f.read()

sentences=[chunk.strip() for chunk in all_data.split(".") if chunk.strip()]

def CollectionFull():
   
   collection_full.add(
       ids=['id1'],
       documents=all_data
   )
   
   result=collection_full.query(
       query_texts=user_input,
       n_results=3
   )
   
   prompt=f"""
      you are a helpful assistant.
      Answer the following question from the given context below.
   
      if answer is  not present given context,say:
      I don't know the answer based on given context.
   
      Question:
      {user_input}
   
      Context:
      {result["documents"][0]}
   """
   print(result['documents'][0])
   print('\n')
   response=client.models.generate_content_stream(
       model="gemini-2.5-flash",
       contents=prompt
   )
   
   for res in response:
       print(res.text,end="",flush=True)
   print('--------------------------------------------------------------------------------------------------------------------------------------------------------------')

def Collection_2():
   chunks=[]
   
   for i in range(0,len(sentences),2):
       chunks.append(".".join(sentences[i:i+2])+".")
   
   ids=[]
   for i in range(0,len(chunks)):
      ids.append(f"id{i}")
   
   collection_2.add(
       ids=ids,
       documents=chunks
   )
   
   result=collection_2.query(
       query_texts=user_input,
       n_results=3
   )
   
   prompt=f"""
      you are a helpful assistant.
      Answer the following question from the given context below.
   
      if answer is  not present given context,say:
      I don't know the answer based on given context.
   
      Question:
      {user_input}
   
      Context:
      {result["documents"][0]}
   """
   print(result['documents'][0])
   print('\n')
   response=client.models.generate_content_stream(
       model="gemini-2.5-flash",
       contents=prompt
   )
   
   for res in response:
       print(res.text,end="",flush=True)
   print('--------------------------------------------------------------------------------------------------------------------------------------------------------------')

def Collection_5():

   chunks=[]
   
   for i in range(0,len(sentences),5):
       chunks.append(".".join(sentences[i:i+5])+".")
   
   ids=[]
   for i in range(0,len(chunks)):
      ids.append(f"id{i}")
   
   collection_5.add(
       ids=ids,
       documents=chunks
   )
   
   result=collection_5.query(
       query_texts=user_input,
       n_results=3
   )
   
   prompt=f"""
      you are a helpful assistant.
      Answer the following question from the given context below.
   
      if answer is  not present given context,say:
      I don't know the answer based on given context.
   
      Question:
      {user_input}
   
      Context:
      {result["documents"][0]}
   """
   print(result['documents'][0])
   print('\n')
   response=client.models.generate_content_stream(
       model="gemini-2.5-flash",
       contents=prompt
   )
   
   for res in response:
       print(res.text,end="",flush=True)
   print('--------------------------------------------------------------------------------------------------------------------------------------------------------------')

CollectionFull()
Collection_2()
Collection_5()