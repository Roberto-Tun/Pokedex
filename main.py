from flask import Flask, render_template, request
import requests, json, random


# function that takes the name of the pokemon and returns the raw data of the pokemon
def get_pokemon_data(PokemonName):
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    url = base_url + PokemonName
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

# function that takes the name of the pokemon and returns the image url, name, type, weight, height and description of the pokemon
def pokemon_display_data(PokemonName):
    pokemon_info = get_pokemon_data(PokemonName) # get the raw data of the pokemon
    pokemon_img_url = pokemon_info['sprites']['front_default']
    pokemon_name = pokemon_info['name']
    pokemon_type = pokemon_info['types'][0]['type']['name']
    pokemon_weight = pokemon_info['weight']
    pokemon_height = pokemon_info['height']
    return pokemon_img_url, pokemon_name, pokemon_type, pokemon_weight, pokemon_height

# Flask app
app = Flask(__name__)


@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():

    action = request.form['action']

    if action == 'guess':
        pokemon_search = request.form['pokemon_name']
        pokemon_img_url, pokemon_name, pokemon_type, pokemon_weight, pokemon_height = pokemon_display_data(pokemon_search)
        return render_template('index.html', pokemon_pic=pokemon_img_url, pokemon_name=pokemon_name, pokemon_type=pokemon_type, pokemon_weight=pokemon_weight, pokemon_height=pokemon_height,)
    


    #pokemon_search = request.form['pokemon_name']
    #pokemon_img_url, pokemon_name, pokemon_type, pokemon_weight, pokemon_height = pokemon_display_data(pokemon_search)
    #return render_template('index.html', pokemon_pic=pokemon_img_url, pokemon_name=pokemon_name, pokemon_type=pokemon_type, pokemon_weight=pokemon_weight, pokemon_height=pokemon_height,)

@app.route('/')
def index():
    random_pokemon = random.randint(1, 1025)
    pokemon_img_url, pokemon_name, pokemon_type, pokemon_weight, pokemon_height = pokemon_display_data(str(random_pokemon))
    return render_template('index.html', pokemon_pic=pokemon_img_url, pokemon_name=pokemon_name, pokemon_type=pokemon_type, pokemon_weight=pokemon_weight, pokemon_height=pokemon_height,)

app.run(port=5000)