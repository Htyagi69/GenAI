from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
import json
import math

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

document=[
    "Python is a highly popular programming language known for its clean, readable syntax and extensive library support.Many developers prefer using Python for data analysis, automation scripts, and web development backend systems.",
    "Football is a globally celebrated team sport where players score goals by moving a ball across a grass field.Millions of passionate fans gather in massive stadiums or watch broadcasts to support their favourite football clubs.",
    "Cooking is both a practical daily skill and a creative art form that uses heat to transform raw ingredients into meals.Blending unique spices and fresh herbs allows chefs to craft complex flavour profiles in traditional cultural dishes.",
    "Machine learning is a specific branch of computer science where algorithms find patterns in data to make accurate predictions.Training a machine learning model requires feeding it large amounts of high-quality data so it can learn autonomously.",
    "Travelling to new countries opens your mind to diverse cultures, historical traditions, and breathtaking natural landscapes.Many modern travellers prefer packing light and exploring hidden local spots instead of crowded tourist destinations.",
    "Movies combine visual storytelling, acting, and audio design to evoke powerful emotions and entertain global audiences.Film directors spend months in post-production editing scenes and mixing sound to perfect the final cinematic cut.",
    "Artificial intelligence focuses on creating smart computer systems capable of performing tasks that usually require human intelligence.Generative AI technologies can create entirely new text, realistic images, and computer code from simple human prompts.",
    "Music uses structured sound, rhythm, and melody to express deep human emotions across different cultures.Learning to play a musical instrument like the guitar or piano can greatly improve cognitive focus and memory.",
    "Space exploration relies on advanced telescopes and robotic rovers to search for signs of life on distant planets.The observable universe contains billions of massive galaxies, mysterious black holes, and vast clouds of cosmic dust.",
    "History is the systematic study of past human events, ancient civilisations, and the evolution of global societies.Analysing primary historical documents helps researchers understand the complex causes of major world conflicts.",
    "Physics is the fundamental science that studies matter, energy, space, and time to understand how the universe behaves.Quantum mechanics is a branch of physics that explores the strange and counterintuitive behavior of subatomic particles",
    "Dogs are incredibly loyal companion animals known for their strong sense of smell and close bond with human families.Working dog breeds are frequently trained by professionals to assist in search and rescue missions or guide the visually impaired.",
    "JavaScript is the core scripting language used to build interactive and dynamic features on modern websites.Developers use JavaScript framework environments like Node.js to run code directly on servers instead of web browsers.",
    "Cats are agile, independent pets that communicate using a variety of subtle vocalizations and body language signs.Domestic felines retain their natural hunting instincts, often chasing small toys or climbing to high vantage points.",
    "Modern cars rely heavily on advanced electronic sensors, onboard computers, and hybrid or fully electric drivetrains.The automotive industry is rapidly shifting toward autonomous driving technologies to improve road safety and efficiency.",
]

embeddings=[]
Json=[]
all_data=[]
docs=[]
similarity=[]
any_change=False

def cosine_similarity(A,B,size):
  dot=0
  mag1=0
  mag2=0
  for i in range(0,size):
    dot+=A[i]*B[i]
    mag1+=A[i]**2
    mag2+=B[i]**2

  return dot/(math.sqrt(mag1)*math.sqrt(mag2))

try:
  with open("RAG_embeddings.json","r",encoding="utf-8") as f:
   all_data=json.load(f)
  
  embeddings=[item["embedding"] for item in all_data]
  docs=[item["document"] for item in all_data]
except Exception as e:
  print(e)

#Initial fillup
if len(embeddings)==0 or docs!=document:
 embeddings=[]
 try:
   for doc in document:
     embedd=client.models.embed_content(
         model="gemini-embedding-2",
         contents=doc,
         config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
     )
     embeddings.append(embedd.embeddings[0].values)
     Json.append({"document":doc,"embedding":embedd.embeddings[0].values})

   with open("RAG_embeddings.json","w",encoding="utf-8") as f:
     json.dump(Json,f,indent=4,ensure_ascii=False)
   print("Successfully Wrote🎉")
 except Exception as e:
   print(e)


user_input=input(f">> ")
test_case=None
try:
  inp=client.models.embed_content(
    model="gemini-embedding-2",
    contents=user_input,
    config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
  )
  test_case=inp.embeddings[0].values
except Exception as e:
  print(e)

size=len(test_case)
for i in range(0,len(document)):
  similarity.append((cosine_similarity(embeddings[i],test_case,size),document[i]))
  
similarity.sort(reverse=True)

top_docs=[]
for embed,doc in similarity[:3]:
  top_docs.append(doc) 

context=f"\n\n".join(top_docs)

prompt=f"""
     you are an helpful assistant.
     Answer only using given context below.

     if answer is not present in the context,say:
     "I don't know based on the provided documents."

     Context:
     {context}
     
     Question:
     {user_input}
     """

response=client.models.generate_content_stream(
  model="gemini-2.5-flash",
  contents=prompt,
)

for chunk in response:
  print(chunk.text,end="")

