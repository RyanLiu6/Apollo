import copy
import json
import random
import datetime

from models.secret_santa import Santa, SecretSantas

def get_secret_santas():
    # Load previous year's secret santa
    current_year = datetime.datetime.now().year

    with open("previous_years.json") as read_file:
        data = json.load(read_file)

    previous_year = data[str(current_year - 1)]

    previous_santas = SecretSantas()

    for k, v in enumerate(previous_year):
        if k < len(previous_year) - 1:
            index = k + 1
        else:
            index = 0

        previous_santas.add_santa(Santa(
            name=v,
            recipient=previous_year[index]))

    this_year = copy.deepcopy(previous_year)
    random.shuffle(this_year)

    this_santas = SecretSantas()
    for k, v in enumerate(this_year):
        if k < len(this_year) - 1:
            index = k + 1
        else:
            index = 0

        # Need to redo if previous and current years are the same
        name = v
        current = this_year[index]
        previous = previous_santas.get_santa(name).recipient

        if current == previous:
            no_nos = [k, index]
            rand_int = -1
            while not rand_int in no_nos:
                rand_int = random.randint(0, len(this_year))

            current = this_year[rand_int]

        this_santas.add_santa(Santa(
            name=name,
            recipient=current))

    # Store it in the json file
    this_year_json = []
    for k, v in this_santas.santas.items():
        this_year_json.append(v.name)

    data[str(current_year)] = this_year_json

    with open("previous_years.json", "w") as write_file:
        json.dump(data, write_file, indent=4)

    return this_santas
