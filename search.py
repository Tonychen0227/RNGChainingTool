import csv
import random
import datetime

from pearl_plat_seed import PearlPlatSeedEngine, get_natures_list


def try_get(key, details, type_to_cast):
    try:
        return type_to_cast(details[key])
    except Exception as e:
        raise ValueError(f"No valid argument for field {key} with error {e}")


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

    total_encounters = 0

    for combination in combinations:
        checked += 1

        seed_engine = PearlPlatSeedEngine(combination[0], combination[1], combination[2], combination[3],
                                          combination[4], combination[5])

        seed_engine.populate(max(max_frames, 1000))

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
                    verify_result = verify_method_j(seed_engine, query, details["queries"])
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

            for x in range(100, max(max_frames, 1000)):
                if seed_engine.has_encounter(x, 30, 40):
                    total_encounters += 1

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
                f.writerow([f"# of Encounters in first {max(max_frames, 1000)} frames: {total_encounters}"])
                for frame in frames["Method1"]:
                    for item in frame:
                        f.writerow([f"Method1 at frame {item}: {seed_engine.get_method_one_pokemon(item).print()}"])

                del frames["Method1"]

                if len(frames.keys()) > 0:
                    f.writerow([str(frames)])

                del four_early, two_early, two_late, four_late

            total_encounters = 0

            del seed_engine

        except WindowsError:
            del seed_engine
            continue


def verify_pkrs(seed_engine, pkrs):
    min_frame = try_get("min_frame", pkrs, int)
    max_frame = try_get("max_frame", pkrs, int)
    if min_frame > max_frame:
        raise ValueError("Min frame must be lower or equal")

    if min_frame < 0 or max_frame > 15000:
        raise ValueError("Frames must be between 0 and 15k")

    good = False
    for frame in range(min_frame, max_frame + 1):
        if seed_engine.call(frame) in ["4000", "8000", "c000"]:
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

    is_shiny = method_1["is_shiny_var"]

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

        if is_shiny and not seed_engine.is_shiny(poke):
            continue

        if not good:
            good = []
        good.append(frame)

    return good


def verify_method_j(seed_engine, method_j, all_queries):
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
        ability = int(method_j["ability"])
        if ability not in [0, 1]:
            raise ValueError("Ability value must be 0 or 1")

    enc_rate = try_get("enc_rate", method_j, int)

    movement_rate = try_get("movement_rate", method_j, int)

    is_surfing = not method_j["is_grass_var"]

    min_level_surf = 0
    max_level_surf = 0
    min_avail_level_surf = 0
    max_avail_level_surf = 0
    if is_surfing:
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

    is_grass = method_j["is_grass_var"]
    ignore_encounter_check = method_j["ignore_encounter_check_var"]
    is_shiny = method_j["is_shiny_var"]

    good = False

    synchronize_target = method_j["synchronize_target"]
    synchronize_natures = [None]

    if synchronize_target is not None and synchronize_target.strip() != "":
        synchronize_natures_list = synchronize_target.split("/")
        target_natures = [x for x in synchronize_natures_list if x in get_natures_list()]

        if len(target_natures) == 0:
            raw_query = [x for x in all_queries if "label" in x.keys() and x["label"].get() == synchronize_target]
            if len(raw_query) == 1:
                if raw_query["type"] == "MethodJ":
                    result = verify_method_j(seed_engine, raw_query, all_queries)
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

            if is_shiny and not seed_engine.is_shiny(poke):
                continue

            if not ignore_encounter_check and not seed_engine.has_encounter(frame, enc_rate, movement_rate):
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

