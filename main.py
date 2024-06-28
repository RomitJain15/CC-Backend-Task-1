import requests

pokemon_name = input("Enter a Pokemon name: ")


try:
    if pokemon_name == "": # Takes care of empty input
        print("\033[91mPokemon not found\033[0m") # Using \033[91m to color the text red
        exit()

    try:
        int(pokemon_name) # Handles the case where ID is inputted since we only need name input
        print("\033[91mPokemon not found\033[0m")
        exit()
    except ValueError: # Only passes when the pokemon name is inputted 
        pass

    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"

    response = requests.get(api_url)
    response.raise_for_status()

    data = response.json()

    print()

    # Using \033[1m and \033[0m to bold and unbold the text in all the following print statements

    print(f"\033[1mName:\033[0m {data['name'][0].upper() + data['name'][1:]}")

    print(f"\033[1mNational Number:\033[0m {data['id']}")

    if data['types']:
        print("\033[1mType:\033[0m", end="")
        for type in data['types']:
            print(f" {type['type']['name'].upper()} ", end="")
        print()

    if data['abilities']:
        print("\033[1mAbilities:\033[0m", end="")
        for ability in data['abilities']:
            print(f" {ability['ability']['name'][0].upper() + ability['ability']['name'][1:]} ", end="")
        print()

    print(f"\033[1mHeight:\033[0m {data['height'] / 10} m")

    print(f"\033[1mWeight:\033[0m {data['weight'] / 10} kg")

    print()

    if data['stats']:
        total = 0
        print("\033[1mBase Stats:\033[0m")
        for stat in data['stats']:
            total += stat['base_stat']
            if len(stat['stat']['name']) <= 2:
                print(f"\033[1m{stat['stat']['name'].upper()}:\033[0m {stat['base_stat']}")
            elif '-' in stat['stat']['name']:
                space_index = stat['stat']['name'].find('-')
                print(f"\033[1m{stat['stat']['name'][0].upper() + stat['stat']['name'][1:space_index] + ' ' + stat['stat']['name'][space_index+1].upper() + stat['stat']['name'][space_index+2:]}:\033[0m {stat['base_stat']}")
            else:
                print(f"\033[1m{stat['stat']['name'][0].upper() + stat['stat']['name'][1:]}:\033[0m {stat['base_stat']}")
        print(f"\033[1mTotal:\033[0m {total}")
        print()

        sprite_url = data['sprites']['other']['official-artwork']['front_default']
        sprite_data = requests.get(sprite_url)
        
        with open('sprite.png', 'wb') as f:
            f.write(sprite_data.content)
        print("\033[32mImage downloaded\033[0m")

except requests.exceptions.HTTPError as e:
    print("\033[91mPokemon not found\033[0m")
    exit()