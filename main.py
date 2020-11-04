import csv
import datetime
import sys
import traceback

import tkinter as tk
from os import path
import json
import os

from benchmark import Benchmark
from search import search_details
from tests import Test


def fill_labels(list_labels, start_row):
    current_column = 0
    for label in list_labels.keys():
        tk.Label(master, text=label).grid(row=start_row, column=current_column)
        current_column += 1
        labels[label].grid(row=start_row, column=current_column)
        current_column += 1
        if current_column == 8:
            start_row += 1
            current_column = 0

    return start_row


def fill_queries():
    start_row = queries_start_row
    current_column = 0
    total_queries = queries

    for query in total_queries:
        tk.Label(master, text=query["type"]).grid(row=start_row, column=current_column)
        tk.Label(master, text="Leave query empty to not search for it").grid(row=start_row, column=current_column + 1)

        if query["type"] == "MethodJ":
            tk.Label(master, text="Type in the label of the query pokemon you get for synchronize ability") \
                .grid(row=start_row, column=current_column + 5, columnspan=2)

        start_row += 1
        for item in query.keys():
            if item in ["type", "encounter_area_var", "is_shiny_var", "ignore_encounter_check_var"]:
                continue
            tk.Label(master, text=item).grid(row=start_row, column=current_column)
            current_column += 1
            query[item].grid(row=start_row, column=current_column)
            current_column += 1
            if current_column == 8:
                start_row += 1
                current_column = 0
        start_row += 1
        current_column = 0

    return start_row


def get_raws_from_query(query):
    ret = {}
    for key in query.keys():
        if key == "type":
            ret[key] = query[key]
            continue
        if key in ["encounter_area", "is_shiny", "ignore_encounter_check"]:
            continue
        if key in ["encounter_area_var", "is_shiny_var", "ignore_encounter_check_var"]:
            ret[key] = query[key].get()
            continue
        ret[key] = query[key].get()
    return ret


def extract_details():
    saveable = {
        "queries": []
    }

    for label in labels.keys():
        key = ''.join(label.split(' '))
        saveable[key] = labels[label].get()

    for y in queries:
        temp = saveable["queries"]
        temp.append(get_raws_from_query(y))
        saveable["queries"] = temp

    return saveable


def save_file():
    file = file_name.get()
    if path.exists(f'{file}.json'):
        os.remove(f'{file}.json')

    saveable = extract_details()

    with open(f'{file}.json', "w+") as fp:
        json.dump(saveable, fp)

    x = 1
    backup_file_name = f'{file}_BACKUP{x}.json'

    while os.path.exists(backup_file_name):
        x += 1
        backup_file_name = f'{file}_BACKUP{x}.json'

    with open(f'{backup_file_name}', "w+") as fp:
        json.dump(saveable, fp)


def load_file():
    file = file_name.get()
    if path.exists(f'{file}.json'):
        with open(f'{file}.json') as json_file:
            existing = json.load(json_file)
    else:
        error_message.set(f"Cannot find file named {file}.json")
        return

    global queries
    queries = []

    for label in labels.keys():
        key = ''.join(label.split(' '))
        if key in existing:
            labels[label].delete(0, tk.END)
            labels[label].insert(0, existing[key])

    if "queries" in existing:
        for query in existing["queries"]:
            if query["type"] == "MethodJ":
                add_method_j()
                current = queries[-1]
                for key in query.keys():
                    if key in current.keys():
                        if key == "type":
                            current[key] = query[key]
                            continue
                        if key in ["encounter_area_var", "is_shiny_var", "ignore_encounter_check_var"]:
                            current[key].set(query[key])
                            continue
                        current[key].delete(0, tk.END)
                        current[key].insert(0, query[key])

            if query["type"] == "Method1":
                add_method_1()
                current = queries[-1]
                for key in query.keys():
                    if key in current.keys():
                        if key == "type":
                            current[key] = query[key]
                            continue
                        if key in ["is_shiny_var"]:
                            current[key].set(query[key])
                            continue
                        current[key].delete(0, tk.END)
                        current[key].insert(0, query[key])

            if query["type"] == "PKRS":
                add_pokerus()
                current = queries[-1]
                for key in query.keys():
                    if key in current.keys():
                        if key == "type":
                            current[key] = query[key]
                            continue
                        current[key].delete(0, tk.END)
                        current[key].insert(0, query[key])


queries = []


def add_method_j():
    entry14 = tk.Entry(master)
    entry14.insert(0, "Poke Name :)")

    entry1 = tk.Entry(master)
    entry1.insert(0, "1/3/5/7/9")

    entry2 = tk.Entry(master)
    entry2.insert(0, "Adamant/Modest")

    entry15 = tk.Entry(master)
    entry15.insert(0, "PokeLabel/Nature1/Nature2")

    entry3 = tk.Entry(master)
    entry3.insert(0, "Fire/Psychic")

    entry4 = tk.Entry(master)
    entry4.insert(0, "60")

    entry5 = tk.Entry(master)
    entry5.insert(0, "0/0/0/0/0/0")

    entry6 = tk.Entry(master)
    entry6.insert(0, "31/31/31/31/31/31")

    entry7 = tk.Entry(master)
    entry7.insert(0, 0)

    entry8 = tk.Entry(master)
    entry8.insert(0, 100)

    entry9 = tk.Entry(master)
    entry9.insert(0, 0)

    entry10 = tk.Entry(master)
    entry10.insert(0, 1000)

    entry11 = tk.Entry(master)
    entry11.insert(0, 2000)

    entry12 = tk.Entry(master)
    entry12.insert(0, 30)

    entry13 = tk.Entry(master)
    entry13.insert(0, 70)

    variable3 = tk.StringVar(master)
    variable3.set("Surfing")  # default value
    menu3 = tk.OptionMenu(master, variable3, "Grass", "Surfing", "FishingOld", "FishingGood", "FishingSuper")

    variable4 = tk.BooleanVar(master)
    button4 = tk.Checkbutton(master, variable=variable4)

    variable5 = tk.BooleanVar(master)
    button5 = tk.Checkbutton(master, variable=variable5)

    entry16 = tk.Entry(master)
    entry16.insert(0, 20)

    entry19 = tk.Entry(master)
    entry19.insert(0, 40)

    entry17 = tk.Entry(master)
    entry17.insert(0, 20)

    entry18 = tk.Entry(master)
    entry18.insert(0, 40)

    new_query = {
        "type": "MethodJ",
        "label": entry14,
        "enc_slots": entry1,
        "natures": entry2,
        "synchronize_target": entry15,
        "hidden_power_types": entry3,
        "min_hidden_power": entry4,
        "min_ivs": entry5,
        "max_ivs": entry6,
        "min_item_deter": entry7,
        "max_item_deter": entry8,
        "ability": entry9,
        "min_frame": entry10,
        "max_frame": entry11,
        "enc_rate": entry12,
        "movement_rate": entry13,
        "encounter_area": menu3,
        "encounter_area_var": variable3,
        "ignore_encounter_check": button4,
        "ignore_encounter_check_var": variable4,
        "is_shiny": button5,
        "is_shiny_var": variable5,
        "min_level_water": entry16,
        "max_level_water": entry19,
        "min_avail_level_water": entry17,
        "max_avail_level_water": entry18
    }

    queries.append(new_query)

    fill_queries()


def add_method_1():
    entry13 = tk.Entry(master)
    entry13.insert(0, "Poke name :)")

    entry2 = tk.Entry(master)
    entry2.insert(0, "Adamant/Modest")

    entry3 = tk.Entry(master)
    entry3.insert(0, "Fire/Psychic")

    entry4 = tk.Entry(master)
    entry4.insert(0, "60")

    entry5 = tk.Entry(master)
    entry5.insert(0, "0/0/0/0/0/0")

    entry6 = tk.Entry(master)
    entry6.insert(0, "31/31/31/31/31/31")

    entry9 = tk.Entry(master)
    entry9.insert(0, 0)

    variable = tk.BooleanVar(master)
    button = tk.Checkbutton(master, variable=variable)

    entry10 = tk.Entry(master)
    entry10.insert(0, 1000)

    entry11 = tk.Entry(master)
    entry11.insert(0, 2000)

    new_query = {
        "type": "Method1",
        "label": entry13,
        "natures": entry2,
        "hidden_power_types": entry3,
        "min_hidden_power": entry4,
        "min_ivs": entry5,
        "max_ivs": entry6,
        "ability": entry9,
        "is_shiny": button,
        "is_shiny_var": variable,
        "min_frame": entry10,
        "max_frame": entry11
    }

    queries.append(new_query)

    fill_queries()


def add_pokerus():
    entry1 = tk.Entry(master)
    entry1.insert(0, 0)

    entry2 = tk.Entry(master)
    entry2.insert(0, 1000)

    new_query = {
        "type": "PKRS",
        "min_frame": entry1,
        "max_frame": entry2
    }

    queries.append(new_query)

    fill_queries()


def search():
    details = extract_details()
    try:
        search_details(details)
    except Exception as e:
        error_message.set(str(e))
        traceback.print_exc()

    return


if __name__ == "__main__":
    Test()

    '''
    time = datetime.datetime.now()
    for x in range(0, 10):
        Benchmark()

    current_time = datetime.datetime.now()
    total_seconds = (current_time - time).total_seconds()

    progress_file_name = f'benchmarks/{datetime.datetime.now().strftime("%Y_%b_%d_%H:%M:%S")}.csv'

    with open(progress_file_name, 'w+') as progress_file:
        progress = csv.writer(progress_file, lineterminator='\n')
        progress.writerow([f"{total_seconds} seconds"])
    '''

    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1]) as json_file:
                existing = json.load(json_file)
                search_details(existing)
        exit()

    current_row = 0

    master = tk.Tk()

    tk.Label(master, text="Metadata").grid(row=0, column=0)
    tk.Label(master, text="All queries are INCLUSIVE").grid(row=0, column=1)
    tk.Label(master, text="https://Tonychen0227.github.io").grid(row=0, column=4, columnspan=4)

    current_row += 1

    master.title('RNG Chaining Tool by xSLAY3RL0Lx#0630 - BETA')

    min_month = tk.Entry(master)
    max_month = tk.Entry(master)
    min_day = tk.Entry(master)
    max_day = tk.Entry(master)
    min_hour = tk.Entry(master)
    max_hour = tk.Entry(master)
    min_mins = tk.Entry(master)
    max_mins = tk.Entry(master)
    min_secs = tk.Entry(master)
    max_secs = tk.Entry(master)
    min_delay = tk.Entry(master)
    max_delay = tk.Entry(master)
    tid = tk.Entry(master)
    sid = tk.Entry(master)

    labels = {
        "Min month": min_month,
        "Max month": max_month,
        "Min day": min_day,
        "Max day": max_day,
        "Min hour": min_hour,
        "Max hour": max_hour,
        "Min mins": min_mins,
        "Max mins": max_mins,
        "Min secs": min_secs,
        "Max secs": max_secs,
        "Min delay": min_delay,
        "Max delay": max_delay,
        "tid": tid,
        "sid": sid
    }

    current_row = fill_labels(labels, current_row + 1)

    queries_start_row = current_row + 1

    fill_queries()

    current_row = 1000

    tk.Button(master,
              text='Add Method J',
              command=add_method_j).grid(row=current_row, column=0)

    tk.Button(master,
              text='Add Method 1',
              command=add_method_1).grid(row=current_row, column=1)

    tk.Button(master,
              text='Add PKRS',
              command=add_pokerus).grid(row=current_row, column=2)

    tk.Button(master,
              text='Start Search',
              command=search).grid(row=current_row, column=3)

    tk.Label(master, text="File name: ").grid(row=current_row, column=4)
    file_name = tk.Entry(master)
    file_name.insert(0, "DemoPlat")
    file_name.grid(row=current_row, column=5)

    tk.Button(master,
              text='Load',
              command=load_file).grid(row=current_row, column=6)

    tk.Button(master,
              text='Save',
              command=save_file).grid(row=current_row, column=7)

    current_row += 1
    error_message = tk.StringVar()
    error_entry = tk.Label(master, textvariable=error_message)
    error_message.set("Error message will go here")
    error_entry.grid(row=current_row, column=0, columnspan=4)

    seeds_message = tk.StringVar()
    seeds_entry = tk.Label(master, textvariable=seeds_message)
    seeds_message.set("Found seeds go to date.csv")
    seeds_entry.grid(row=current_row, column=4, columnspan=4)

    tk.mainloop()
