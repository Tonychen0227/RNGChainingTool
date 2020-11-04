import csv
import random
import datetime

from models.enums import EncounterArea
from models.queries import PKRS, Method1, MethodJ, VerifiableQuery
from pearl_plat_seed import PearlPlatSeedEngine


def try_get(key, details, type_to_cast):
    try:
        return type_to_cast(details[key])
    except Exception as e:
        raise ValueError(f"No valid argument for field {key} with error {e}")


def validate_and_transform_query(query) -> VerifiableQuery:
    min_frame = try_get("min_frame", query, int)
    max_frame = try_get("max_frame", query, int)
    if min_frame > max_frame:
        raise ValueError("Min frame must be lower or equal")

    if min_frame < 0 or max_frame > 15000:
        raise ValueError("Frames must be between 0 and 15k")

    if query["type"] == "PKRS":
        ret = PKRS()
        ret.min_frame = min_frame
        ret.max_frame = max_frame
        return ret

    label = query["label"]

    query_keys = query.keys()

    natures = None
    stripped_natures = query["natures"].strip()
    if "natures" in query_keys and stripped_natures != "":
        natures = stripped_natures.split("/")

    hidden_power_types = None
    stripped_hidden_power_types = query["hidden_power_types"].strip()
    if "hidden_power_types" in query_keys and stripped_hidden_power_types != "":
        hidden_power_types = stripped_hidden_power_types.split("/")

    min_hidden_power = None
    stripped_min_hidden_power = query["min_hidden_power"].strip()
    if "min_hidden_power" in query_keys and stripped_min_hidden_power != "":
        try:
            min_hidden_power = int(stripped_min_hidden_power)
            if min_hidden_power < 0 or min_hidden_power > 70:
                raise ValueError("Min hidden power value must be within 0 and 70")
        except Exception as e:
            raise ValueError(f"Bad hidden power power: {e}")

    min_ivs = None
    stripped_min_ivs = query["min_ivs"].strip()
    if "min_ivs" in query_keys and stripped_min_ivs != "":
        try:
            min_ivs = []
            for x in stripped_min_ivs.split("/"):
                x = int(x)
                if x < 0 or x > 31:
                    raise ValueError("IV value must be within 0 and 31")
                min_ivs.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad IV: {e}")

    max_ivs = None
    stripped_max_ivs = query["max_ivs"].strip()
    if "max_ivs" in query_keys and stripped_max_ivs != "":
        try:
            max_ivs = []
            for x in stripped_max_ivs.split("/"):
                x = int(x)
                if x < 0 or x > 31:
                    raise ValueError("IV value must be within 0 and 31")
                max_ivs.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad IV: {e}")

    ability = None
    stripped_ability = query["ability"].strip()
    if "ability" in query_keys and stripped_ability != "":
        try:
            ability = int(stripped_ability)
            if ability not in [0, 1]:
                raise ValueError("Ability value must be 0 or 1")
        except Exception as e:
            raise ValueError(f"Bad ability: {e}")

    is_shiny = query["is_shiny_var"]

    if query["type"] == "Method1":
        ret = Method1()
        ret.min_frame = min_frame
        ret.max_frame = max_frame
        ret.natures = natures
        ret.hidden_power_types = hidden_power_types
        ret.min_hidden_power = min_hidden_power
        ret.min_ivs = min_ivs
        ret.max_ivs = max_ivs
        ret.ability = ability
        ret.is_shiny = is_shiny
        ret.label = label
        return ret

    enc_slots = None
    stripped_enc_slots = query["enc_slots"].strip()
    if "enc_slots" in query_keys and stripped_enc_slots != "":
        try:
            enc_slots = []
            for x in stripped_enc_slots.split("/"):
                x = int(x)
                if x < 0 or x > 11:
                    raise ValueError("Enc slot value must be within 0 and 11")
                enc_slots.append(int(x))
        except Exception as e:
            raise ValueError(f"Bad enc slot: {e}")

    min_item_deter = None
    stripped_min_item_deter = query["min_item_deter"].strip()
    if "min_item_deter" in query_keys and stripped_min_item_deter != "":
        try:
            min_item_deter = int(stripped_min_item_deter)
            if min_item_deter < 0 or min_item_deter > 100:
                raise ValueError("Min item determinant value must be within 0 and 70")
        except Exception as e:
            raise ValueError(f"Bad min item determinant: {e}")

    max_item_deter = None
    stripped_max_item_deter = query["max_item_deter"].strip()
    if "max_item_deter" in query_keys and stripped_max_item_deter != "":
        try:
            max_item_deter = int(stripped_max_item_deter)
            if max_item_deter < 0 or max_item_deter > 100:
                raise ValueError("Max item determinant value must be within 0 and 70")
        except Exception as e:
            raise ValueError(f"Bad max item determinant: {e}")

    enc_rate = try_get("enc_rate", query, int)

    movement_rate = try_get("movement_rate", query, int)

    encounter_area = EncounterArea[query["encounter_area_var"]]

    min_level_water = 0
    max_level_water = 0
    min_avail_level_water = 0
    max_avail_level_water = 0
    if int(encounter_area) >= 1:
        min_level_water = int(query["min_level_water"])
        max_level_water = int(query["max_level_water"])
        min_avail_level_water = int(query["min_avail_level_water"])
        max_avail_level_water = int(query["max_avail_level_water"])
        if min_level_water < min_avail_level_water:
            raise ValueError("Min water level below minimum")
        if max_level_water < min_level_water:
            raise ValueError("Max water level below min")
        if max_level_water > max_avail_level_water:
            raise ValueError("Max water level above maximum")

    ignore_encounter_check = query["ignore_encounter_check_var"]

    if encounter_area >= EncounterArea.FishingOld:
        ignore_encounter_check = True

    synchronize_target = query["synchronize_target"]
    synchronize_natures = [None]

    ret = MethodJ()
    ret.min_frame = min_frame
    ret.max_frame = max_frame
    ret.natures = natures
    ret.hidden_power_types = hidden_power_types
    ret.min_hidden_power = min_hidden_power
    ret.min_ivs = min_ivs
    ret.max_ivs = max_ivs
    ret.ability = ability
    ret.is_shiny = is_shiny
    ret.enc_slots = enc_slots
    ret.min_item_deter = min_item_deter
    ret.max_item_deter = max_item_deter
    ret.enc_rate = enc_rate
    ret.movement_rate = movement_rate
    ret.encounter_area = encounter_area
    ret.min_level_water = min_level_water
    ret.max_level_water = max_level_water
    ret.min_avail_level_water = min_avail_level_water
    ret.max_avail_level_water = max_avail_level_water
    ret.ignore_encounter_check = ignore_encounter_check
    ret.synchronize_target = synchronize_target
    ret.synchronize_natures = synchronize_natures
    ret.label = label
    return ret


def search_details(details, is_dry_run : bool = False):
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
    if details["tid"] is not None and details["tid"].strip() != "":
        tid = int(details["tid"])
    else:
        tid = None

    if details["sid"] is not None and details["sid"].strip() != "":
        sid = int(details["sid"])
    else:
        sid = None

    if min_month_internal < 1 or max_month_internal > 12:
        raise ValueError("Month must be in between 1, 12")

    if min_day_internal < 1 or max_day_internal > 31:
        raise ValueError("Day must be in between 1, 31")

    if min_hour_internal < 0 or max_hour_internal > 23:
        raise ValueError("Hour must be in between 0, 23")

    if min_mins_internal < 0 or max_mins_internal > 59:
        raise ValueError("Mins must be in between 0, 59")

    if min_secs_internal < 0 or max_secs_internal > 59:
        raise ValueError("Secs must be in between 0, 59")

    if min_delay_internal > max_delay_internal:
        raise ValueError("Min delay larger than max delay")

    if min_delay_internal < 0:
        raise ValueError("Delay must not be lower than 0")

    values = []
    ab_combinations = []

    if min_month_internal > max_month_internal:
        months = [x for x in range(min_month_internal, 13)] + [x for x in range(1, max_month_internal + 1)]
    else:
        months = [x for x in range(min_month_internal, max_month_internal + 1)]

    if min_day_internal > max_day_internal:
        days = [x for x in range(min_day_internal, 32)] + [x for x in range(1, max_day_internal + 1)]
    else:
        days = [x for x in range(min_day_internal, max_day_internal + 1)]

    if min_hour_internal > max_hour_internal:
        hours = [x for x in range(min_hour_internal, 24)] + [x for x in range(1, max_hour_internal + 1)]
    else:
        hours = [x for x in range(min_hour_internal, max_hour_internal + 1)]

    if min_mins_internal > max_mins_internal:
        mins = [x for x in range(min_mins_internal, 60)] + [x for x in range(1, max_mins_internal + 1)]
    else:
        mins = [x for x in range(min_mins_internal, max_mins_internal + 1)]

    if min_secs_internal > max_secs_internal:
        secs = [x for x in range(min_secs_internal, 60)] + [x for x in range(1, max_secs_internal + 1)]
    else:
        secs = [x for x in range(min_secs_internal, max_secs_internal + 1)]

    for month in months:
        for day in days:
            if month in [1, 3, 5, 7, 8, 10, 12]:
                if day > 31:
                    continue
            elif month == 2:
                if day > 28:
                    continue
            else:
                if day > 30:
                    continue
            for minute in mins:
                for sec in secs:
                    ab = month * day + minute + sec
                    ab = hex(ab & 0xff)[2:]

                    while len(ab) < 2:
                        ab = "0" + ab

                    if ab not in values:
                        ab_combinations.append([month, day, minute, sec])
                        values.append(ab)

    combinations = []

    for ab_combination in ab_combinations:
        for hour in hours:
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

    inner_queries = [x for x in details["queries"]]

    max_frames = max([int(y["max_frame"]) for y in inner_queries])

    fixed_queries = []

    for inner_query in inner_queries:
        new_query = validate_and_transform_query(inner_query)
        new_query.tid = tid
        new_query.sid = sid
        fixed_queries.append(new_query)

    del inner_queries

    for combination in combinations:
        checked += 1

        seed_engine = PearlPlatSeedEngine(combination[0], combination[1], combination[2], combination[3],
                                          combination[4], combination[5])

        seed_engine.populate(max_frames)

        if not is_dry_run and checked % 100 == 0:
            current_time = datetime.datetime.now()
            total_seconds = (current_time - time).total_seconds()
            with open(progress_file_name, 'a+') as progress_file:
                progress = csv.writer(progress_file, lineterminator='\n')
                progress.writerow([f"Checked {checked} of {total_combinations}, Elapsed {total_seconds:.2f}s, ETA "
                                   f"{((total_seconds / checked) * (total_combinations - checked)):.2f}s"])

        try:
            frames = {}
            for query in fixed_queries:
                if isinstance(query, MethodJ):
                    query.synchronize_natures = [None]
                    populate_synchronize(seed_engine, query, fixed_queries)
                verify_result = query.verify_frames(seed_engine)
                if not verify_result:
                    raise WindowsError("")
                class_name = query.__class__.__name__
                if class_name in frames.keys():
                    temp = frames[class_name]
                    temp.append(verify_result)
                    frames[class_name] = temp
                else:
                    frames[class_name] = [verify_result]

            if not is_dry_run:
                with open(log_file_name, 'a+') as outfile:
                    f = csv.writer(outfile, lineterminator='\n')
                    f.writerow([f"Seed {seed_engine.get_initial_seed()} (Year 2000) (on {combination[0]}/{combination[1]} "
                                f"at {combination[2]}:{combination[3]}:{combination[4]} Delay {combination[5]})"])
                    four_early = PearlPlatSeedEngine(combination[0], combination[1], combination[2], combination[3],
                                                     combination[4], combination[5] - 4)
                    two_early = PearlPlatSeedEngine(combination[0], combination[1], combination[2], combination[3],
                                                    combination[4], combination[5] - 2)
                    two_late = PearlPlatSeedEngine(combination[0], combination[1], combination[2], combination[3],
                                                   combination[4], combination[5] + 2)
                    four_late = PearlPlatSeedEngine(combination[0], combination[1], combination[2], combination[3],
                                                    combination[4], combination[5] + 4)
                    f.writerow([f"SIDs: -4: {four_early.get_tid_sid()[0]} -2: {two_early.get_tid_sid()[0]} "
                                f"0: {seed_engine.get_tid_sid()[0]} "
                                f"+2: {two_late.get_tid_sid()[0]} +4: {four_late.get_tid_sid()[0]}"])
                    f.writerow([str(frames)])

                    del four_early, two_early, two_late, four_late

            del seed_engine

        except WindowsError:
            del seed_engine
            continue


def populate_synchronize(seed_engine, method_j, all_queries):
    if method_j.synchronize_target is not None and method_j.synchronize_target.strip() != "":
        synchronize_natures_list = method_j.synchronize_target.split("/")
        target_natures = [x for x in synchronize_natures_list if x in ["Hardy", "Lonely", "Brave", "Adamant",
                                                                       "Naughty", "Bold", "Docile", "Relaxed",
                                                                       "Impish", "Lax", "Timid", "Hasty",
                                                                       "Serious", "Jolly", "Naive", "Modest",
                                                                       "Mild", "Quiet", "Bashful", "Rash",
                                                                       "Calm", "Gentle", "Sassy", "Careful", "Quirky"]]

        if len(target_natures) == 0:
            raw_query = [x for x in all_queries if x.label == method_j.synchronize_target]
            if len(raw_query) == 1:
                raw_query = raw_query[0]
                result = raw_query.verify_frames(seed_engine)

                if result:
                    for x in result:
                        query_result = seed_engine.get_method_j_pokemon(x, raw_query.encounter_area)
                        method_j.synchronize_natures.append(query_result[0].nature)
        else:
            method_j.synchronize_natures = method_j.synchronize_natures + target_natures

