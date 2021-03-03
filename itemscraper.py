import requests
import shutil
import json
import urllib.request
import re

# YOUR DIRECTORY OF CHOICE
input_directory = ""

parameters = {
    "lang":"english"
}

# get reponse
response = requests.get("https://api.guildwars2.com/v2/items", params=parameters)

# get list of all item ids
if response.status_code == 200:
    itemsJson = response.json()
    text = json.dumps(itemsJson, sort_keys=True, indent=4)
    items = json.loads(text)

# Regular Expression patterns
pattern = re.compile(r'[\W_]+', re.UNICODE)

# Set of existing icons already downloaded
icon_set = set()

# loop through each item
for item in items:

    # get item api url
    url = "https://api.guildwars2.com/v2/items/" + str(item)

    # make request
    current_item_request = requests.get(url)

    # if success
    if current_item_request.status_code == 200:
        try:
            current_item = current_item_request.json()

            # Clear non-alphanumeric
            item_name = current_item["name"]
            item_name = re.sub(r'[\W_]+', ' ', item_name)
            # Get icon url
            icon_url = current_item["icon"]
            item_type = current_item["type"]

            # Print details to console for tracking purposes
            print("Name: " + item_name)
            print("ID: " + str(item))
            print("Type: " + item_type)
            print("URL: " + icon_url)

            try:
                # Armors
                if item_type == "Armor":
                    try:
                        directory = "Armor\\" + current_item['details']['weight_class'] + "\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in Armor Directory")
                        directory = "Armor\\"

                # Backs
                elif item_type == "Back":
                    directory = "Back\\"

                # Bags
                elif item_type == "Bag":
                    directory = "Bag\\"

                # Consumables
                elif item_type == "Consumable":
                    try:
                        directory = "Consumable\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in Consumables Directory")
                        directory = "Consumable\\"

                # Container
                elif item_type == "Container":
                    try:
                        directory = "Container\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in Container Directory")
                        directory = "Container\\"
                
                # CraftingMaterial
                elif item_type == "CraftingMaterial":
                    directory = "CraftingMaterial\\"

                # Gathering
                elif item_type == "Gathering":
                    try:
                        directory = "Gathering\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in Gathering Directory")
                        directory = "Gathering\\"

                # Gizmo
                elif item_type == "Gizmo":
                    try:
                        directory = "Gizmo\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in Gizmo Directory")
                        directory = "Gizmo\\"
                
                # Key
                elif item_type == "Key":
                    directory = "Key\\"

                # MiniPet   
                elif item_type == "MiniPet":
                    directory = "MiniPet\\"

                # Tool   
                elif item_type == "Tool":
                    directory = "Tool\\"

                # Trait   
                elif item_type == "Trait":
                    directory = "Trait\\"

                # Trinket
                elif item_type == "Trinket":
                    try:
                        directory = "Trinket\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in Trinket Directory")
                        directory = "Trinket\\"

                # Trophy   
                elif item_type == "Trophy":
                    directory = "Trophy\\"

                # UpgradeComponent
                elif item_type == "UpgradeComponent":
                    try:
                        directory = "UpgradeComponent\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in UpgradeComponent Directory")
                        directory = "UpgradeComponent\\"

                # Weapons
                elif item_type == "Weapon":
                    try:
                        directory = "Weapon\\" + current_item['details']['type'] + "\\"
                    except:
                        print("Error in Weapon Directory")
                        directory = "Weapon\\"

                # Get Image and place in directory
                full_directory = input_directory + directory + item_name + ".png"

                print("Full Directory: " + full_directory)
                print("Sub Directory: " + directory)

                if icon_url in icon_set:
                    print(icon_url + " already exists.")
                    pass

                else:
                    urllib.request.urlretrieve(icon_url, input_directory + directory + item_name + ".png")
                    icon_set.add(icon_url)

                print("\n \n")

            except:
                print("Could not get .png of " + str(item) + ". \n")

        except:
            pass

    else:
        print("Error making a API request for item " + str(item) + ".\n")





