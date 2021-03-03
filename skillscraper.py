import requests
import shutil
import json
import urllib.request
import re

# YOUR DIRECTORY OF CHOICE
input_directory = ""

# API call optional parameter
parameters = {
    "lang":"english"
}

# Call API for list of skills
response = requests.get("https://api.guildwars2.com/v2/skills/", params=parameters)

# Check if successful, if it is, get dump json into variable skills
if response.status_code == 200:
    skillsJson = response.json()
    text = json.dumps(skillsJson, sort_keys=True, indent=4)
    skills = json.loads(text)

# RE Pattern
pattern = re.compile(r'[\W_]+', re.UNICODE)

# set of skill icons seen already
skill_set = set()

# variable to track how many skills have been added/seen
skill_count = 1

# loop through API response of all skill ID's
for skill in skills:

    # get URL of current skill ID
    url = "https://api.guildwars2.com/v2/skills/" + str(skill)

    # make API call for current skill
    current_skill_request = requests.get(url)

    # if status code is success
    if current_skill_request.status_code == 200:

        # get json of current skill
        current_skill = current_skill_request.json()

        # get name of skill from 'name' key, strip of non-alphanumeric
        skill_name = current_skill['name']
        skill_name = re.sub(r'[\W_]+', ' ', skill_name)

        # check if 'icon' key exists. Occassional skills in API response with no icon field.
        if 'icon' in current_skill:

            # Get icon renderer URL value from 'icon' field
            icon_url = current_skill['icon']

            # Check if 'professions' key exists
            if 'professions' in current_skill:

                # More than one profession uses this skill, set subdirectory to \\Shared\\
                if len(current_skill['professions']) > 1:
                    subdirectory = "\\Shared\\"

                # Only one profession uses skill, set subdirectory to \\Profession\\ProfessionNameGoesHere\\
                elif len(current_skill['professions']) == 1:
                    subdirectory = "\\Profession\\" + current_skill['professions'][0] + "\\"

                # Edge cases go into \\Shared\\
                else:
                    subdirectory = "\\Shared\\"

            # Edge cases go into \\Shared\\ 
            else:
                subdirectory = "\\Shared\\"

            # Construct final directory
            directory = input_directory + subdirectory

            # Print skill information
            print("Skill Name: " + skill_name)
            print("Skill ID: " + str(skill))
            print("Icon URL: " + icon_url)
            print("Directory: " + directory)
            print("Subdirectory: " + subdirectory)
            print("Skill Collect #" + str(skill_count))
            skill_count += 1

            # Check if renderer url has already been seen by the script
            if icon_url in skill_set:
                print(icon_url + " already exists! Skipping...\n")

            # If icon url is new, add it to set and request the .png, storing it in the directory as skill_name.png
            else:
                urllib.request.urlretrieve(icon_url, directory + skill_name + ".png")
                print("\n")
                skill_set.add(icon_url)
        else:
            print("No Icon!")    
    else:
        print("Could not request current skill, status code: " + str(current_skill_request.status_code))

print("Program complete.")









