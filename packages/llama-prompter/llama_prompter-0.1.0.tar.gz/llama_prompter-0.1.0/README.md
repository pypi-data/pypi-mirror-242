<div align="center">
   <img alt="logo" height="100px" src="https://gitlab.com/uploads/-/system/project/avatar/51880384/llama-prompt2.png">
</div>

# llama-prompter
llama-prompter is a Python library designed to facilitate the crafting of prompts for Large Language Models (LLMs) and the retrieval of structured responses.
It transcribes prompt templates into llama_cpp grammars, guiding the LLM to produce more structured and relevant outputs.

## Features

- **Prompt Templates to llama_cpp Grammar**: Transcribe templates into grammars that guide the LLM output, ensuring more structured and relevant responses.
- **Support for Pydantic Types**: Define complex variables using Pydantic classes for more detailed and specific model outputs.
- **Decode LLM output to populate predefined variables**: Variables defined in prompt templates will be automatically populated by decoding the LLM output.

## Installation

```
pip install llama-prompter
```

## Usage

### Basic example
```
import json
from llama_cpp import Llama
from llama_prompter.prompt import Prompt

model = Llama(model_path="<path_to_your_model>", verbose=False)
prompt = Prompt(
    """[INST] Describe the moon[/INST]
Short description: {description:str}
Distance from Earth in miles: {distance:int}
Diameter in miles: {diameter:int}
Gravity in Gs: {gravity:float}"""
)

response = model(
    prompt.prompt,
    grammar=prompt.grammar,
    stop=["[INST]", "[/INST]"],
    temperature=0,
    max_tokens=2048
)
completion = response['choices'][0]['text']
variables = prompt.decode_response(completion)

print(prompt.prompt)
print(completion)
print('\nVariables:')
print(json.dumps(variables, indent=4))
```
Output:
```
[INST] Describe the moon[/INST]
Short description:
"The Moon is Earth's only permanent natural satellite, orbiting our planet at an average distance of about 384,400 kilometers. It is roughly spherical in shape with a diameter of about 3,474 kilometers and has no atmosphere or magnetic field. The surface of the Moon is rocky and dusty, and it is covered in impact craters, mountains, and vast, flat plains called maria."
Distance from Earth in miles: 238855
Diameter in miles: 2159
Gravity in Gs: 0.1655

Variables:
{
    "description": "The Moon is Earth's only permanent natural satellite, orbiting our planet at an average distance of about 384,400 kilometers. It is roughly spherical in shape with a diameter of about 3,474 kilometers and has no atmosphere or magnetic field. The surface of the Moon is rocky and dusty, and it is covered in impact craters, mountains, and vast, flat plains called maria.",
    "distance": 238855,
    "diameter": 2159,
    "gravity": 0.1655
}
```
### Advanced example with pydantic

```import json
from pydantic import BaseModel
from llama_cpp import Llama
from llama_prompter.prompt import Prompt

class Planet(BaseModel):
    name: str
    short_description: str
    diameter_miles: int
    distance_from_earth_miles: int
    gravity: float

model = Llama(model_path="<path_to_your_model>", verbose=False)
prompt = Prompt(
    """[INST] Describe the moon[/INST]
{moon:Planet}"""
)

response = model(
    prompt.prompt,
    grammar=prompt.grammar,
    stop=["[INST]", "[/INST]"],
    temperature=0,
    max_tokens=2048
)
completion = response['choices'][0]['text']
variables = prompt.decode_response(completion)
planet = variables['moon']

print(prompt.prompt)
print(completion)

print('\nPlanet model:')
print(planet.model_dump_json(indent=4))
```
Output:
```
[INST] Describe the moon[/INST]

{"name":"Moon","short_description":"The Moon is Earth's only permanent natural satellite and is about one-quarter the size of our planet. It orbits around Earth at an average distance of about 238,900 miles (384,400 kilometers) and takes approximately 27.3 days to complete one orbit.","diameter_miles":2159,"distance_from_earth_miles":238900,"gravity":0.165}

Planet model:
{
    "name": "Moon",
    "short_description": "The Moon is Earth's only permanent natural satellite and is about one-quarter the size of our planet. It orbits around Earth at an average distance of about 238,900 miles (384,400 kilometers) and takes approximately 27.3 days to complete one orbit.",
    "diameter_miles": 2159,
    "distance_from_earth_miles": 238900,
    "gravity": 0.165
}
```

## Development

```
python -m pip install poetry poethepoet
```


## License

llama-prompter is released under the MIT License.
