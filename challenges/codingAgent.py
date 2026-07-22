from google import genai
from dotenv import load_dotenv
import subprocess
from pathlib import Path
import shutil
import os

load_dotenv()

client =genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

path=input()

query=input(f">>")

list_tool={
   "type":"function",
   "name":"list_function",
   "description":"List every file inside the project.",
   "parameters": {
        "type": "object",
        "properties": {}
    }
}
create_tool={
   "type":"function",
   "name":"create_function",
   "description":"create a fresh file in given folder at a given path",
   "parameters": {
        "type": "object",
        "properties": {
           "fileName":{
              "type":"string",
              "description":"the name of a new file"
           }
        },
         "required": ["fileName"]
    }
}
read_tool={
   "type":"function",
   "name":"read_function",
   "description":"Read the whole content inside the file",
   "parameters": {
        "type": "object",
        "properties": {
           "filePath":{
              "type":"string",
              "description":"a path to reach the file content"
           }
        },
         "required": ["filePath"]
    }
}
delete_tool = {
    "type": "function",
    "name": "delete_function",
    "description": "delete the given file or folder",
    "parameters": {
        "type": "object",
        "properties": {
            "target_Path": {
                "type": "string",
                "description": "path of the file or folder"
            },
        },
        "required": ["target_Path"]
    }
}
test_tool = {
    "type": "function",
    "name": "run_tests",
    "description": " a tool that run basic tests or the provided one in test_file ",
    "parameters": {
        "type": "object",
        "properties": {
            "test_file": {
                "type": "string",
                "description": "a path of test_file"
            },
        },
        "optional":["test_file"]
    }
}
run_tool = {
    "type": "function",
    "name": "run_function",
    "description": "run a given file and get the output",
    "parameters": {
        "type": "object",
        "properties": {
            "fileName": {
                "type": "string",
                "description": "name of the file"
            },
            "args": {
                "type": "string",
                "description": "a input needed to pass to script"
            },
        },
        "required": ["fileName"],
        "optional":["args"]
    }
}
write_tool = {
    "type": "function",
    "name": "write_function",
    "description": "write the provided content in a existing file",
    "parameters": {
        "type": "object",
        "properties": {
            "fileName": {
                "type": "string",
                "description": "name of the file"
            },
            "content": {
                "type": "string",
                "description": "content to be delivered to file"
            }
        },
        "required": ["fileName","content"]
    }
}
search_tool = {
    "type": "function",
    "name": "search_function",
    "description": "Search every project file for a keyword and return matching file names, line numbers and text.",
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "Word or phrase to search."
            }
        },
        "required": ["keyword"]
    }
}

def create_function(fileName):
  try:
    with open(f"{path}/{fileName}","x") as f:
      pass
  except Exception as e:
    print(e)
    return e
  
def write_function(fileName,content):
  try:
    with open(f"{path}/{fileName}","w",encoding="utf-8") as f:
      f.write(content)
  except Exception as e:
    print(e)
    return e

def list_function():
 try: 
  files=[]
  for file in os.listdir(path):
      files.append(file)
  return files
 except Exception as e:
   return e
 
def read_function(filePath):
 try:  
   data=[]
   with open(f"{path}/{filePath}","r",encoding="utf-8") as f:
      data.append(f.read())
   return data
 except Exception as e:
   return e 
 
def search_function(keyword):
 try:
    res_format=[]
    files=list_function()
    for file in files:
      with open(f"{path}/{file}","r",encoding="utf-8") as f:
        for line_no,line in enumerate(f,start=1):
         if keyword.lower() in line.lower():
           res_format.append({
             "fileName":file,
             "line":line_no,
             "text":line.strip()
           })
    return res_format

 except Exception as e:
   print(e)
   return e

def run_function(fileName,args):
  try:
    full_path=f"{path}/{fileName}"
    command=["python",full_path]
    if args:
      res=subprocess.run(command,check=True,input=args,text=True,capture_output=True)
    else:
      res=subprocess.run(command,check=True,text=True,capture_output=True)
    # print(f"output:{res.stdout}")
    return res.stdout
  except subprocess.CalledProcessError as e:
    print(res.stderr)
    return res.stderr

def delete_function(target_Path):
  try:
    path=Path(target_Path)
    if not path.exists():
      return "invalid path"
    if path.is_file():
      path.unlink()
      print(f"{target_Path} is deleted✅" )
    if path.is_dir():
      shutil.rmtree(path)
      print(f"{target_Path} is deleted✅" )
  except Exception as e:
    return e

def run_tests(test_file=None):
 try:
   cmd=["pytest"]
   if test_file:
     cmd.append(test_file)
   result=subprocess.run(
     cmd,
     text=True,
     capture_output=True
   )
   return{
     "stdout":result.stdout,
     "stderr":result.stderr,
     "returncode":result.returncode
   }
 
 except Exception as e:
   return e

Tools={
   "list_function":list_function,
   "read_function":read_function,
   "search_function":search_function,
   "create_function":create_function,
   "write_function":write_function,
   "run_function":run_function,
   "delete_function":delete_function,
   "run_tests":run_tests
}

def execute_tool(response):
    function_results =[]
    for function_call in response.steps:
       if function_call.type=="function_call":
           if function_call.name=="delete_function":
              user_permission=input('Allow this action (yes/no)?: ').strip().lower()
              if user_permission!="yes":
                return "Abort"
           print(f"Calling:{function_call.name},{function_call.arguments}")
           result=str(Tools[function_call.name](**function_call.arguments))
           function_results.append({
               "type": "function_result",
               "name": function_call.name,
               "id": function_call.id,
               "result": result
           })
    return function_results

conversation=[query]
response = client.interactions.create(
    model="gemini-2.5-flash",
    input=query,
    tools=[list_tool,read_tool,search_tool,create_tool,write_tool,run_tool,delete_tool,test_tool]
)

while True:
  function_results=execute_tool(response)
  if not function_results:
    print(response.output_text)
    break
  response = client.interactions.create(
      model="gemini-2.5-flash",
      previous_interaction_id=response.id,
      input=function_results,
      tools=[list_tool,read_tool,search_tool,create_tool,write_tool,run_tool,delete_tool,test_tool]
  )

     