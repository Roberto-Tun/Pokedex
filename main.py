from flask import Flask, render_template, request
import requests, json

def get_pokemon_data(PokemonName):
    base_url = "https://pokeapi.co/api/v2/pokemon/"
    url = base_url + PokemonName
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def pokemon_image_url(PokemonName):
    pokemon_info = get_pokemon_data(PokemonName)
    return pokemon_info['sprites']['front_default']


app = Flask(__name__)


@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    pokemon_name = request.form['pokemon_name']
    pokemon_info = get_pokemon_data(pokemon_name)
    pokemon_image_url = pokemon_info['sprites']['front_default']
    return render_template('index.html', meme_pic=pokemon_image_url, subreddit=pokemon_info['name'])

@app.route('/')
def index():
    pokemon_info = get_pokemon_data("pikachu")
    pokemon_image_url = pokemon_info['sprites']['front_default']
    return render_template('index.html', meme_pic=pokemon_image_url, subreddit=pokemon_info['name'])

app.run(port=5000)