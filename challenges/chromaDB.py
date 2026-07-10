import os
from google import genai
from dotenv import load_dotenv
import chromadb

load_dotenv()

chroma_client = chromadb.PersistentClient(path="../chroma_db")

collection=chroma_client.get_or_create_collection(name="docs")

collection.add(
    ids=["id1","id2","id3","id4","id5","id6","id7","id8","id9","id10","id11","id12","id13","id14","id15"],
    documents=[
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