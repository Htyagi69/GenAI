from google import genai
import os
from dotenv import load_dotenv
from google.genai import types
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

def cosine_similarity(num1,num2,num3,A,B,size):
   for i in range(0,size):
      num1+=A[i]*B[i]
      num2+=A[i]**2
      num3+=B[i]**2
   res=num1/(math.sqrt(num2)*math.sqrt(num3))
   return res

prompt=input(f">> ")
embeddings=[]
result=[]
pair=[]
for doc in document:
  response=client.models.embed_content(
      model="gemini-embedding-2",
      contents=doc,
      config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
  )
  embeddings.append(response.embeddings[0].values)

inp=client.models.embed_content(
   model="gemini-embedding-2",
   contents=prompt,
   config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
)
testcase=inp.embeddings[0].values

size=len(testcase)
for embed in embeddings:
   result.append(cosine_similarity(0,0,0,embed,testcase,size))
for i in range(len(result)):
   pair.append((result[i],document[i]))

pair.sort(reverse=True)
count=0

for key,value in pair:
   print(f"{value}\n")
   count+=1
   if count>2:
    break

   
   
   
   





























# from google import genai
# from dotenv import load_dotenv
# import os
# from google.genai import types
# import math
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity

# load_dotenv()

# client=genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )

# texts = [
#     "What is the meaning of life?",
#     "What is the purpose of existence?",
#     "How do I bake a cake?",
# ]
# embeddings=[]

# for text in texts:
#   result=client.models.embed_content(
#       model="gemini-embedding-2",
#       contents=text,
#       config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
#   )
# #   print(f"embedd:{result.embeddings[0]}")
#   embeddings.append(result.embeddings[0].values)

# df=pd.DataFrame(
#     cosine_similarity(embeddings),
#     index=texts,
#     columns=texts
# )

# print(df)

# res=cosine_similarity([embeddings[1]],[embeddings[2]])


# print(f"res:{res}")

