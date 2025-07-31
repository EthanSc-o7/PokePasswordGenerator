import random
import requests
import secrets

base_url = "https://pokeapi.co/api/v2/"


class Pokemon:
    def __init__(self, name, pid, ability):
        self.name = name
        self.pid = pid
        self.ability = ability

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
    for x in roster:
        password += str(x.pid)
        if count != 3:
            password += ":"

        if count == 3:
            finishingTouch = "@" + secrets.choice(roster).ability.capitalize()
            password += finishingTouch
        count += 1

    print(password)
    return password


def prompt():
    roster = []
    print("To create a password, enter 4 Pokemon")
    i = 0
    while i < 4:
        pokemon_name = input()
        pokemon_info = get_pokemon_info(pokemon_name)
        if pokemon_info:
            i += 1
            name = pokemon_info['name'].capitalize()
            pokeID = pokemon_info['id']
            ability = secrets.choice(pokemon_info['abilities']).get('ability')['name']
            sprite = pokemon_info['sprites']['front_default']
            roster.append(Pokemon(name, pokeID, ability))

        else:
            print("Please enter a valid pokemon")
    generate_password(roster)


# prompt()


def random_generate():
    roster = []
    print("Generate a password using 4 Pokemon...")
    i = 0
    while i < 4:
        pokemon_name = random.randrange(1, 1026)
        pokemon_info = get_pokemon_info(pokemon_name)
        if pokemon_info:
            i += 1
            # print(f"Name: {pokemon_info['name'].capitalize()}")
            # print(f"Id: {pokemon_info['id']}")
            # print(f"Ability: {pokemon_info['abilities'][0].get('ability')['name']}")

            name = pokemon_info['name'].capitalize()
            pokeID = pokemon_info['id']
            ability = secrets.choice(pokemon_info['abilities']).get('ability')['name']

            roster.append(Pokemon(name, pokeID, ability))

        else:
            print("Please enter a valid pokemon")
    newpass = generate_password(roster)
    return newpass

# random_generate()

def main():
    print("Welcome to Poke Password, to start enter 1 to randomly generate password or 2 to enter pokemon one by one")
    userinput = input()
    if userinput == '1':
        random_generate()
    elif userinput == '2':
        prompt()
    else:
        main()

    print("Run Again? 1 for Yes, 2 for No")
    secondinput = input()

    if secondinput == '1':
        main()
    elif secondinput =='2':
        print("Bye Bye")

main()