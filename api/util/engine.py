
from openai import OpenAI
from dotenv import load_dotenv
import json
from api.util.pokemon import poke_api
from api.util.yugioh import render_card_in_console

load_dotenv()
client = OpenAI()

function_descriptions = [
  {
      "name": "get_pokemon",
      "description": "Based on the color of the pokemon, choose a random pokemon name",
      "parameters": {
        "type": "object",
        "properties": {
          "pokemon_name" : {
            "type": "string",
            "description": "name of the pokemon with no spaces",
          },
        },
        "required": ["pokemon_name"],
        },
      },
    {
        "name": "get_card",
        "description": "choose a card like a heart or a diamond and I will render it in the console for you.",
        "parameters": {
          "type": "object",
          "properties": {
            "card_suit" : {
              "type": "string",
              "description": "the suit of a card",
            },
            "card_value" : {
              "type": "string",
              "description": "the value of a card",
            },
          },
          "required": ["card_suit", "card_value"],
          },
    }
]

def ask_and_reply(prompt):
  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a pokemon master"},
    {"role": "user", "content": prompt}
  ],
  functions = function_descriptions,
  function_call = "auto",
)
  output = completion.choices[0].message #output is chatcompletion type (Chatgpt's own type)
  print(output)
  print(type(output))
  if (output.function_call.name == "get_pokemon"):
    print(output.function_call.arguments) #output.function_call.arguments returns ChatGPT response as STR
    print(type(output.function_call.arguments)) #ChatCompletionMessage(content=None, role='assistant', function_call=FunctionCall(arguments='{"pokemon_name":"squirtle"}', name='get_pokemon'), tool_calls=None)
    json_data = json.loads(output.function_call.arguments) 
    pokemon_stats = poke_api(json_data.get('pokemon_name'))
    return pokemon_stats
  elif (output.function_call.name == "get_card"):
    print(output.function_call.arguments)
    print(type(output.function_call.arguments))
    json_data = json.loads(output.function_call.arguments)
    card_name = json_data.get('card_suit')
    card_value = json_data.get('card_value')
    return render_card_in_console(card_name, card_value) #array of card name and value



#print(ask_and_reply("give me a black pokemon"))