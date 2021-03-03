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

response = requests.get("https://api.guildwars2.com/v2/skills/", params=parameters)

if response.status_code == 200:
    skillsJson = response.json()
    text = json.dumps(skillsJson, sort_keys=True, indent=4)
    skills = json.loads(text)

# RE Pattern
pattern = re.compile(r'[\W_]+', re.UNICODE)

skill_set = set()
skill_count = 1

for skill in skills:

    url = "https://api.guildwars2.com/v2/skills/" + str(skill)
    current_skill_request = requests.get(url)

    if current_skill_request.status_code == 200:

        current_skill = current_skill_request.json()

        skill_name = current_skill['name']
        skill_name = re.sub(r'[\W_]+', ' ', skill_name)

        if 'icon' in current_skill:

            icon_url = current_skill['icon']

            if 'professions' in current_skill:
                if len(current_skill['professions']) > 1:
                    subdirectory = "\\Shared\\"
                elif len(current_skill['professions']) == 1:
                    subdirectory = "\\Profession\\" + current_skill['professions'][0] + "\\"
                else:
                    subdirectory = "\\Shared\\"
            else:
                subdirectory = "\\Shared\\"

            directory = input_directory + subdirectory

            print("Skill Name: " + skill_name)
            print("Skill ID: " + str(skill))
            print("Icon URL: " + icon_url)
            print("Directory: " + directory)
            print("Subdirectory: " + subdirectory)
            print("Skill Collect #" + str(skill_count))
            skill_count += 1

            if icon_url in skill_set:
                print(icon_url + " already exists! Skipping...\n")
            else:
                urllib.request.urlretrieve(icon_url, directory + skill_name + ".png")
                print("\n")
                skill_set.add(icon_url)
        else:
            print("No Icon!")    
    else:
        print("Could not request current skill, status code: " + str(current_skill_request.status_code))

print("Program complete.")









