import csv
import random
import sys
import traceback

from pearl_plat.pearl_plat_seed import PearlPlatSeedEngine, get_natures_list
import tkinter as tk
from os import path
import json
import os
import datetime

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
            if item in ["type", "is_grass_var"]:
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
        if key in ["is_grass"]:
            continue
        if key in ["is_grass_var"]:
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
                        if key in ["is_grass_var"]:
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

    variable3 = tk.BooleanVar(master)
    button3 = tk.Checkbutton(master, variable=variable3)

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
        "is_grass": button3,
        "is_grass_var": variable3,
        "min_level_surf": entry16,
        "max_level_surf": entry19,
        "min_avail_level_surf": entry17,
        "max_avail_level_surf": entry18
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


def try_get(key, details, type_to_cast):
    try:
        return type_to_cast(details[key])
    except Exception as e:
        raise ValueError(f"No valid argument for field {key} with error {e}")


def verify_pkrs(seed_engine, pkrs):
    min_frame = try_get("min_frame", pkrs, int)
    max_frame = try_get("max_frame", pkrs, int)
    if min_frame > max_frame:
        raise ValueError("Min frame must be lower or equal")

    if min_frame < 0 or max_frame > 15000:
        raise ValueError("Frames must be between 0 and 15k")

    good = False
    for frame in range(min_frame, max_frame + 1):
        if seed_engine.has_pokerus(frame):
            if not good:
                good = []
            good.append(frame)

    return good


def verify_method_1(seed_engine, method_1):
    min_frame = try_get("min_frame", method_1, int)
    max_frame = try_get("max_frame", method_1, int)
    if min_frame > max_frame:
        raise ValueError("Min frame must be lower or equal")

    if min_frame < 0 or max_frame > 15000:
        raise ValueError("Frames must be between 0 and 15k")

    natures = None
    if "natures" in method_1.keys() and method_1["natures"].strip() != "":
        natures = method_1["natures"].strip().split("/")

    hidden_power_types = None
    if "hidden_power_types" in method_1.keys() and method_1["hidden_power_types"].strip() != "":
        hidden_power_types = method_1["hidden_power_types"].strip().split("/")

    min_hidden_power = None
    if "min_hidden_power" in method_1.keys() and method_1["min_hidden_power"].strip() != "":
        try:
            min_hidden_power = int(method_1["min_hidden_power"])
            if min_hidden_power < 0 or min_hidden_power > 70:
                raise ValueError("Min hidden power value must be within 0 and 70")
        except Exception as e:
            raise ValueError(f"Bad hidden power power: {e}")

    min_ivs = None
    if "min_ivs" in method_1.keys() and method_1["min_ivs"].strip() != "":
        try:
            min_ivs = []
            for x in method_1["min_ivs"].strip().split("/"):
                x = int(x)
                if x < 0 or x > 31:
                    raise ValueError("IV value must be within 0 and 31")
                min_ivs.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad IV: {e}")

    max_ivs = None
    if "max_ivs" in method_1.keys() and method_1["max_ivs"].strip() != "":
        try:
            max_ivs = []
            for x in method_1["max_ivs"].strip().split("/"):
                x = int(x)
                if x < 0 or x > 31:
                    raise ValueError("IV value must be within 0 and 31")
                max_ivs.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad IV: {e}")

    ability = None
    if "ability" in method_1.keys() and method_1["ability"].strip() != "":
        try:
            ability = int(method_1["ability"])
            if ability not in [0, 1]:
                raise ValueError("Ability value must be 0 or 1")
        except Exception as e:
            raise ValueError(f"Bad ability: {e}")

    good = False
    for frame in range(min_frame, max_frame + 1):
        poke = seed_engine.get_method_one_pokemon(frame)

        if natures is not None and poke.nature not in natures:
            continue

        hidden_power = poke.get_hidden_power()

        if hidden_power_types is not None and hidden_power[0] not in hidden_power_types:
            continue

        if hidden_power_types is not None and min_hidden_power > int(hidden_power[1]):
            continue

        poke_ivs = poke.ivs

        if min_ivs is not None:
            low_ivs = [int(a) - b for a, b in zip(poke_ivs, min_ivs)]

            if min(low_ivs) < 0:
                continue

        if max_ivs is not None:
            high_ivs = [b - int(a) for a, b in zip(poke_ivs, max_ivs)]

            if min(high_ivs) < 0:
                continue

        if ability is not None and ability != int(poke.ability):
            continue

        if not good:
            good = []
        good.append(frame)

    return good


def verify_method_j(seed_engine, method_j):
    min_frame = try_get("min_frame", method_j, int)
    max_frame = try_get("max_frame", method_j, int)
    if min_frame > max_frame:
        raise ValueError("Min frame must be lower or equal")

    if min_frame < 0 or max_frame > 15000:
        raise ValueError("Frames must be between 0 and 15k")

    enc_slots = None
    if "enc_slots" in method_j.keys() and method_j["enc_slots"].strip() != "":
        try:
            enc_slots = []
            for x in method_j["enc_slots"].strip().split("/"):
                x = int(x)
                if x < 0 or x > 11:
                    raise ValueError("Enc slot value must be within 0 and 11")
                enc_slots.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad enc slot: {e}")

    natures = None
    if "natures" in method_j.keys() and method_j["natures"].strip() != "":
        natures = method_j["natures"].strip().split("/")

    hidden_power_types = None
    if "hidden_power_types" in method_j.keys() and method_j["hidden_power_types"].strip() != "":
        hidden_power_types = method_j["hidden_power_types"].strip().split("/")

    min_hidden_power = None
    if "min_hidden_power" in method_j.keys() and method_j["min_hidden_power"].strip() != "":
        try:
            min_hidden_power = int(method_j["min_hidden_power"])
            if min_hidden_power < 0 or min_hidden_power > 70:
                raise ValueError("Min hidden power value must be within 0 and 70")
        except Exception as e:
            raise ValueError(f"Bad hidden power power: {e}")

    min_ivs = None
    if "min_ivs" in method_j.keys() and method_j["min_ivs"].strip() != "":
        try:
            min_ivs = []
            for x in method_j["min_ivs"].strip().split("/"):
                x = int(x)
                if x < 0 or x > 31:
                    raise ValueError("IV value must be within 0 and 31")
                min_ivs.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad IV: {e}")

    max_ivs = None
    if "max_ivs" in method_j.keys() and method_j["max_ivs"].strip() != "":
        try:
            max_ivs = []
            for x in method_j["max_ivs"].strip().split("/"):
                x = int(x)
                if x < 0 or x > 31:
                    raise ValueError("IV value must be within 0 and 31")
                max_ivs.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad IV: {e}")

    min_item_deter = None
    if "min_item_deter" in method_j.keys() and method_j["min_item_deter"].strip() != "":
        try:
            min_item_deter = int(method_j["min_item_deter"])
            if min_item_deter < 0 or min_item_deter > 100:
                raise ValueError("Min item determinant value must be within 0 and 70")
        except Exception as e:
            raise ValueError(f"Bad min item determinant: {e}")

    max_item_deter = None
    if "max_item_deter" in method_j.keys() and method_j["max_item_deter"].strip() != "":
        try:
            max_item_deter = int(method_j["max_item_deter"])
            if max_item_deter < 0 or max_item_deter > 100:
                raise ValueError("Max item determinant value must be within 0 and 70")
        except Exception as e:
            raise ValueError(f"Bad max item determinant: {e}")

    ability = None
    if "ability" in method_j.keys() and method_j["ability"].strip() != "":
        try:
            ability = int(method_j["ability"])
            if ability not in [0, 1]:
                raise ValueError("Ability value must be 0 or 1")
        except Exception as e:
            error_message.set(f"Bad ability: {e}")
            return

    enc_rate = try_get("enc_rate", method_j, int)

    movement_rate = try_get("movement_rate", method_j, int)

    is_surfing = not method_j["is_grass_var"]

    min_level_surf = 0
    max_level_surf = 0
    min_avail_level_surf = 0
    max_avail_level_surf = 0
    if is_surfing:
        try:
            min_level_surf = int(method_j["min_level_surf"])
            max_level_surf = int(method_j["max_level_surf"])
            min_avail_level_surf = int(method_j["min_avail_level_surf"])
            max_avail_level_surf = int(method_j["max_avail_level_surf"])
            if min_level_surf < min_avail_level_surf:
                raise ValueError("Min surfing level below minimum")
            if max_level_surf < min_level_surf:
                raise ValueError("Max surfing level below min")
            if max_level_surf > max_avail_level_surf:
                raise ValueError("Max surfing level above maximum")
        except Exception as e:
            error_message.set(f"Bad surf level range: {e}")
            return

    is_grass = method_j["is_grass_var"]

    good = False

    synchronize_target = method_j["synchronize_target"]
    synchronize_natures = [None]

    if synchronize_target is not None and synchronize_target.strip() != "":
        synchronize_natures_list = synchronize_target.split("/")
        target_natures = [x for x in synchronize_natures_list if x in get_natures_list()]

        if len(target_natures) == 0:
            target_query = [x for x in queries if "label" in x.keys() and x["label"].get() == synchronize_target]
            if len(target_query) == 1:
                raw_query = get_raws_from_query(target_query[0])
                if raw_query["type"] == "MethodJ":
                    result = verify_method_j(seed_engine, raw_query)
                    if result:
                        for x in result:
                            query_result = seed_engine.get_method_j_pokemon(x, raw_query["is_grass_var"])
                            synchronize_natures.append(query_result[0].nature)
                elif raw_query["type"] == "Method1":
                    result = verify_method_1(seed_engine, raw_query)
                    if result:
                        for x in result:
                            query_result = seed_engine.get_method_one_pokemon(x)
                            synchronize_natures.append(query_result[0].nature)
        else:
            synchronize_natures += target_natures

    for frame in range(min_frame, max_frame + 1):
        for sync_nature in synchronize_natures:
            result = seed_engine.get_method_j_pokemon(frame, is_grass, sync_nature)

            poke = result[0]

            slot = result[1]

            if enc_slots is not None and int(slot) not in enc_slots:
                continue

            if not seed_engine.has_encounter(frame, enc_rate, movement_rate):
                continue

            if natures is not None and poke.nature not in natures:
                continue

            hidden_power = poke.get_hidden_power()

            if hidden_power_types is not None and hidden_power[0] not in hidden_power_types:
                continue

            if hidden_power_types is not None and min_hidden_power > int(hidden_power[1]):
                continue

            poke_ivs = poke.ivs

            if min_ivs is not None:
                low_ivs = [int(a) - b for a, b in zip(poke_ivs, min_ivs)]

                if min(low_ivs) < 0:
                    continue

            if max_ivs is not None:
                high_ivs = [b - int(a) for a, b in zip(poke_ivs, max_ivs)]

                if min(high_ivs) < 0:
                    continue

            poke_item = poke.item_determinator
            if min_item_deter is not None and int(poke_item) < min_item_deter:
                continue

            if max_item_deter is not None and int(poke_item) > max_item_deter:
                continue

            if ability is not None and ability != int(poke.ability):
                continue

            if is_surfing:
                level = seed_engine.get_level(frame, min_avail_level_surf, max_avail_level_surf)
                if level < min_level_surf or level > max_level_surf:
                    continue

            if not good:
                good = []

            good.append(frame)
            break

    return good


def search_details(details):
    min_month_internal = try_get("Minmonth", details, int)
    max_month_internal = try_get("Maxmonth", details, int)
    min_day_internal = try_get("Minday", details, int)
    max_day_internal = try_get("Maxday", details, int)
    min_hour_internal = try_get("Minhour", details, int)
    max_hour_internal = try_get("Maxhour", details, int)
    min_mins_internal = try_get("Minmins", details, int)
    max_mins_internal = try_get("Maxmins", details, int)
    min_secs_internal = try_get("Minsecs", details, int)
    max_secs_internal = try_get("Maxsecs", details, int)
    min_delay_internal = try_get("Mindelay", details, int)
    max_delay_internal = try_get("Maxdelay", details, int)

    if min_month_internal > max_month_internal:
        raise ValueError("Min month larger than max month")

    if min_month_internal < 1 or max_month_internal > 12:
        raise ValueError("Month must be in between 1, 12")

    if min_day_internal > max_day_internal:
        raise ValueError("Min day larger than max day")

    if min_day_internal < 1 or max_day_internal > 31:
        raise ValueError("Day must be in between 1, 31")

    if min_hour_internal > max_hour_internal:
        raise ValueError("Min hour larger than max hour")

    if min_hour_internal < 0 or max_hour_internal > 23:
        raise ValueError("Hour must be in between 0, 23")

    if min_mins_internal > max_mins_internal:
        raise ValueError("Min mins larger than max mins")

    if min_mins_internal < 0 or max_mins_internal > 59:
        raise ValueError("Mins must be in between 0, 59")

    if min_secs_internal > max_secs_internal:
        raise ValueError("Min secs larger than max secs")

    if min_secs_internal < 0 or max_secs_internal > 59:
        raise ValueError("Secs must be in between 0, 59")

    if min_delay_internal > max_delay_internal:
        raise ValueError("Min delay larger than max delay")

    if min_delay_internal < 0:
        raise ValueError("Delay must not be lower than 0")

    values = []
    ab_combinations = []

    for month in range(min_month_internal, max_month_internal + 1):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            if max_day_internal > 31:
                max_day_internal = 31
        elif month == 2:
            if max_day_internal > 28:
                max_day_internal = 28
        else:
            if max_day_internal > 30:
                max_day_internal = 30

        for day in range(min_day_internal, max_day_internal + 1):
            for minute in range(min_mins_internal, max_mins_internal + 1):
                for secs in range(min_secs_internal, max_secs_internal + 1):
                    ab = month * day + minute + secs
                    ab = hex(ab & 0xff)[2:]

                    while len(ab) < 2:
                        ab = "0" + ab

                    if ab not in values:
                        ab_combinations.append([month, day, minute, secs])
                        values.append(ab)

    combinations = []

    for ab_combination in ab_combinations:
        for hour in range(min_hour_internal, max_hour_internal + 1):
            for delay in range(min_delay_internal, max_delay_internal + 1):
                combinations.append([ab_combination[0], ab_combination[1], hour, ab_combination[2],
                                     ab_combination[3], delay])

    del values
    del ab_combinations

    checked = 0
    log_file_name = f'{datetime.datetime.now().strftime("%Y_%b_%d_%H_%M_%S")}.csv'
    progress_file_name = f'{datetime.datetime.now().strftime("%Y_%b_%d_%H_%M_%S")}_progress.csv'
    if "queries" not in details.keys():
        return

    random.shuffle(combinations)

    time = datetime.datetime.now()

    total_combinations = len(combinations)

    for combination in combinations:
        checked += 1

        seed_engine = PearlPlatSeedEngine(combination[0], combination[1], combination[2], combination[3],
                                          combination[4], combination[5])

        if checked % 100 == 0:
            current_time = datetime.datetime.now()
            total_seconds = (current_time - time).total_seconds()
            with open(progress_file_name, 'a+') as progress_file:
                progress = csv.writer(progress_file, lineterminator='\n')
                progress.writerow([f"Checked {checked} of {total_combinations}, Elapsed {total_seconds:.2f}s, ETA "
                                   f"{((total_seconds / checked) * (total_combinations - checked)):.2f}s"])

        try:
            frames = {}
            for query in details["queries"]:
                if query["type"] == "MethodJ":
                    verify_result = verify_method_j(seed_engine, query)
                    if not verify_result:
                        raise WindowsError("")
                    else:
                        if "MethodJ" in frames.keys():
                            temp = frames["MethodJ"]
                            temp.append(verify_result)
                            frames["MethodJ"] = temp
                        else:
                            frames["MethodJ"] = [verify_result]

                if query["type"] == "Method1":
                    verify_result = verify_method_1(seed_engine, query)
                    if not verify_result:
                        raise WindowsError("")
                    else:
                        if "Method1" in frames.keys():
                            temp = frames["Method1"]
                            temp.append(verify_result)
                            frames["Method1"] = temp
                        else:
                            frames["Method1"] = [verify_result]

                if query["type"] == "PKRS":
                    verify_result = verify_pkrs(seed_engine, query)
                    if not verify_result:
                        raise WindowsError("")
                    else:
                        if "PKRS" in frames.keys():
                            temp = frames["PKRS"]
                            temp.append(verify_result)
                            frames["PKRS"] = temp
                        else:
                            frames["PKRS"] = [verify_result]

            with open(log_file_name, 'a+') as outfile:
                f = csv.writer(outfile, lineterminator='\n')
                f.writerow([seed_engine.get_initial_seed()])
                f.writerow([str(frames)])

            del seed_engine

        except WindowsError:
            del seed_engine
            continue


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

    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1]) as json_file:
                existing = json.load(json_file)
                search_details(existing)

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
        "Max delay": max_delay
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
