from flask import Flask, render_template, request, session
import requests, json, random

app = Flask(__name__)
app.secret_key = '12312asdas5'

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


@app.route('/check_pokemon', methods=['POST'])
def get_pokemon():

    # the action is taken from the form in the index.html to determine if the user wants to guess or skip the pokemon
    action = request.form['action']

    # the pokemon_search is taken from the form in the index.html to determine if the user's guess is correct
    pokemon_search = request.form['pokemon_name']

    # if the user's guess is correct, the score is incremented by 1 and a new random pokemon is displayed
    if action == 'guess':
        if pokemon_search.lower() != session['current_pokemon']:
            return None
        else:
            session['score'] += 1
            random_pokemon = random.randint(1, 1025)
            pokemon_img_url, pokemon_name, pokemon_type, pokemon_weight, pokemon_height = pokemon_display_data(str(random_pokemon))
            session['current_pokemon'] = pokemon_name
            return render_template('index.html', pokemon_pic=pokemon_img_url, pokemon_name=pokemon_name, pokemon_type=pokemon_type, pokemon_weight=pokemon_weight, pokemon_height=pokemon_height)
    
    # if the user wants to skip the pokemon, a new random pokemon is displayed
    elif action == 'skip':
        random_pokemon = random.randint(1, 1025)
        pokemon_img_url, pokemon_name, pokemon_type, pokemon_weight, pokemon_height = pokemon_display_data(str(random_pokemon))
        session['current_pokemon'] = pokemon_name
        return render_template('index.html', pokemon_pic=pokemon_img_url, pokemon_name=pokemon_name, pokemon_type=pokemon_type, pokemon_weight=pokemon_weight, pokemon_height=pokemon_height)

@app.route('/')
def index():
    random_pokemon = random.randint(1, 1025)
    pokemon_img_url, pokemon_name, pokemon_type, pokemon_weight, pokemon_height = pokemon_display_data(str(random_pokemon))
    session['current_pokemon'] = pokemon_name
    session['score'] = 0
    return render_template('index.html', pokemon_pic=pokemon_img_url, pokemon_name=pokemon_name, pokemon_type=pokemon_type, pokemon_weight=pokemon_weight, pokemon_height=pokemon_height)

if __name__ == '__main__':
    app.run(port=5000)