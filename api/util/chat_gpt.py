
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are pragmatic and honest"},
    {"role": "user", "content": "Who is the favorite child?"}
  ],

)
output = completion.choices[0].message
print(output)

function_descriptions = [
  {
      "name": "get_family_info",
      "description": "Understand all the relationships within a family",
      "parameters": {
        "type": "object",
        "properties": {
          "mother" : {
            "type": "string",
            "description": "the mother of the family, e.g. Jessica",
          },
          "father" : {
            "type": "string",
            "description": "the father of the family, e.g. John",
          },
          "child" : {
            "type": "string",
            "description": "the children of the family, e.g. Bob",
          },
        },
        "required": ["mother", "father", "child"],
        },
      },
  {
      "name": "get_dialogue",
      "description": "understand all the dialogue between family members",
      "parameters": {
        "type": "object",
        "properties": {
          "mother_dialogue" : {
            "type": "string",
            "description": "i love my son",
          },
          "father_dialogue" : {
            "type": "string",
            "description": "i hate my son",
          },
          
        },
        "required": ["mother_dialogue", "father_dialogue"]
        },
      },
]

print(function_descriptions)

def ask_and_reply(prompt):
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are pragmatic and honest"},
    {"role": "user", "content": prompt}
  ],
  functions = function_descriptions,
  function_call = "auto",

)
  output = completion.choices[0].message
  return output



user_prompt = "who is the mother's favorite child?"
print(ask_and_reply(user_prompt))



def get_family_info(mother, father, child):

   family_info = {
    "mother": mother,
    "father" : father,
    "child": child,
    "brother": "Billy",
    "sister":"Sarah",
   }

   return json.dumps(family_info)

def get_dialogue_info(mother, father, child):
   family_info = {
    "mother": mother,
    "father" : father,
    "child": child,
    "brother": "Billy",
    "sister":"Sarah",
   }

   return json.dumps(family_info)
  

mom = json.loads(output.function_call.arguments).get("mother")
dad = json.loads(output.function_call.arguments).get("father")
params = json.loads(output.function_call.arguments)

print(mom)
print(dad)
print(params)

chosen_function = eval(output.function_call.name)
family = chosen_function(**params)
print(family)

second_completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are pragmatic and honest"},
    {"role": "function", "name": output.function_call.name, "content": family}
  ],
  functions = function_descriptions,

)

response = second_completion.choices[0].message.content
print(response)