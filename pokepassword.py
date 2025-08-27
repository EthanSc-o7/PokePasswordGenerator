import secrets
import urllib.request
import FreeSimpleGUI as sg
import requests
import random
import pyperclip

base_url = "https://pokeapi.co/api/v2/"


class Pokemon:
    def __init__(self, name, pid, ability, sprite):
        self.name = name
        self.pid = pid
        self.ability = ability
        self.sprite = sprite

    # def __str__(self):
    #   return f"{self.name}({self.pid})"


def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")


def generate_password(roster):
    random.shuffle(roster)
    count = 0
    password = ""
    selection = "These 4 match the password, with "
    font = ("Consolas", 10)
    for x in roster:
        password += str(x.pid)

        window[str(count + 1)].update(urllib.request.urlopen(x.sprite).read())

        if count != 3:
            password += ":"

        if count == 3:
            pick = secrets.choice(roster)
            selection += f"{pick.name}'s ability"

            finishingTouch = "@" + pick.ability.capitalize()
            password += finishingTouch
        count += 1
    window['-selection-'].update(selection)
    window['-selection-'].Widget.config(font=font)
    # print(password)
    return password


def random_generate():
    roster = []
    i = 0
    while i < 4:
        pokemon_name = random.randrange(1, 1026)
        pokemon_info = get_pokemon_info(pokemon_name)
        if pokemon_info:
            i += 1
            name = pokemon_info['name'].capitalize()
            pokeID = pokemon_info['id']
            ability = secrets.choice(pokemon_info['abilities']).get('ability')['name']
            sprite = pokemon_info['sprites']['front_default']
            roster.append(Pokemon(name, pokeID, ability, sprite))
        else:
            print("Please enter a valid pokemon")
    newpass = generate_password(roster)
    return newpass

with open("names.txt", 'r') as f:
    lines = f.readlines()
pkmnList = [e.strip() for e in lines]

font = ("Consolas", 11)
sg.theme('Light Green 2')
layout = [[sg.Text('Click Generate or Submit 4 Pokemon 1 at a time')],
          [sg.Button("Generate"), sg.Combo(pkmnList, key='Pokemon', size=(30, 1)), sg.Button('Submit')],
          [sg.Push(), sg.Image(key='1'), sg.Image(key='2'), sg.Image(key='3'), sg.Image(key='4'), sg.Push(), ],
          [sg.Push(), sg.Text(key='-selection-'), sg.Push()],
          [sg.Push(),sg.Button('Reset'), sg.Text(key='-OUT-'), sg.Button('COPY'),sg.Push()]]
names = ""
pokemonRoster = []
i = 0
# Create the Window

window = sg.Window('Poke Passwords', layout, size=(500, 250), font=font, icon="logo.ico")
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    if event == "Generate":
        i = 0
        newPassword = random_generate()
        window['-OUT-'].update(newPassword)
    if event == "Submit":

        pokemon_info = get_pokemon_info(values['Pokemon'])
        if pokemon_info and values['Pokemon'] != "":

            name = pokemon_info['name'].capitalize()
            names += name
            if i != 3:
                names += ", "
            pokeID = pokemon_info['id']
            ability = secrets.choice(pokemon_info['abilities']).get('ability')['name']
            sprite = pokemon_info['sprites']['front_default']
            # window[str(i+1)].update(urllib.request.urlopen(sprite).read())
            pokemonRoster.append(Pokemon(name, pokeID, ability, sprite))
            i += 1
            window['-OUT-'].update(f"Add {4 - i} more Pokemon")
        else:
            window['-OUT-'].update("Please enter a valid pokemon")
        window['Pokemon'].update("")
    if event == "Reset":
        i = 0
        pokemonRoster = []
        window['-OUT-'].update("")
        window['-selection-'].update("")
        window['1'].update("")
        window['2'].update("")
        window['3'].update("")
        window['4'].update("")

    if event == 'COPY':
        i = 0
        text = window['-OUT-'].get()
        pyperclip.copy(text)

    if i == 4:
        newPassword = generate_password(pokemonRoster)
        window['-OUT-'].update(newPassword)

window.close()
