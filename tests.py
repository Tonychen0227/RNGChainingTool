from pearl_plat_seed import PearlPlatSeedEngine


class Test:
    def __init__(self):
        seed_engine = PearlPlatSeedEngine(7, 1, 18, 32, 46, 5719)  # DemoPlat

        assert seed_engine.initial_seed == "55121657"

        assert seed_engine.tid == 1218
        assert seed_engine.sid == 16914

        # region methodJ No Synchronize 1

        frame = 1285  # Actual frame 1826

        poke_result = seed_engine.get_method_j_pokemon(frame, True)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "f13c13cb"

        assert poke.ivs == (26, 31, 25, 16, 18, 28)

        assert poke.nature == "Impish"

        assert poke.ability == 1

        assert slot == 5

        assert seed_engine.has_encounter(frame, 30, 40)

        assert poke.get_hidden_power() == ("Flying", 52)

        assert poke.occid == 1353

        # endregion

        # region methodJ No Synchronize 2

        frame = 1326  # Actual frame 1327

        poke_result = seed_engine.get_method_j_pokemon(frame, True)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "6596354d"

        assert poke.ivs == (0, 18, 31, 30, 4, 19)

        assert poke.nature == "Hasty"

        assert poke.ability == 1

        assert slot == 4

        assert seed_engine.has_encounter(frame, 30, 40)

        assert poke.get_hidden_power() == ("Poison", 49)

        assert poke.occid == 1338

        # endregion

        # region Shiny MethodJ
        frame = 17471  # Actual frame 17472

        poke_result = seed_engine.get_method_j_pokemon(frame, True)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "2c166ac5"

        assert poke.ivs == (17, 4, 31, 15, 2, 14)

        assert poke.nature == "Naughty"

        assert poke.ability == 1

        assert slot == 8

        assert poke.get_hidden_power() == ("Bug", 68)

        assert poke.is_shiny()
        # endregion

        # region MethodJ Synchronize success
        frame = 1326  # Actual frame 1327

        poke_result = seed_engine.get_method_j_pokemon(frame, True, "Quiet")
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "166cbed4"

        assert poke.ivs == (17, 7, 11, 25, 8, 19)

        assert poke.nature == "Quiet"

        assert poke.ability == 0

        assert slot == 4

        assert seed_engine.has_encounter(frame, 30, 40)

        assert poke.get_hidden_power() == ("Steel", 38)

        assert poke.occid == 1374

        # endregion

        # region MethodJ Synchronize failure

        frame = 1327  # Actual frame 1328

        poke_result = seed_engine.get_method_j_pokemon(frame, True, "Quiet")
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "24f55a7a"

        assert poke.ivs == (16, 12, 18, 17, 13, 27)

        assert poke.nature == "Impish"

        assert poke.ability == 0

        assert slot == 2

        assert not seed_engine.has_encounter(frame, 30, 40)

        assert poke.get_hidden_power() == ("Ice", 37)

        assert poke.occid == 1386

        # endregion

        # region MethodJ surfing

        frame = 1790  # Actual frame 1791

        poke_result = seed_engine.get_method_j_pokemon(frame, False)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "1374028b"

        assert poke.ivs == (21, 16, 10, 17, 23, 29)

        assert poke.nature == "Docile"

        assert poke.ability == 1

        assert slot == 1

        assert seed_engine.has_encounter(frame, 10, 40)

        assert poke.get_hidden_power() == ("Ice", 52)

        assert poke.occid == 1837

        # endregion

        # region MethodJ surfing synchronize 1

        frame = 1790  # Actual frame 1791

        poke_result = seed_engine.get_method_j_pokemon(frame, False, "Impish")
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "3858fe2d"

        assert poke.ivs == (12, 31, 31, 21, 14, 20)

        assert poke.nature == "Impish"

        assert poke.ability == 1

        assert slot == 1

        assert seed_engine.has_encounter(frame, 10, 40)

        assert poke.get_hidden_power() == ("Bug", 54)

        assert seed_engine.get_level(frame, 20, 30) == 30

        # endregion

        # region MethodJ surfing synchronize 2

        frame = 1811  # Actual frame 1812

        poke_result = seed_engine.get_method_j_pokemon(frame, False, "Impish")
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "1c0f4623"

        assert poke.ivs == (13, 0, 20, 9, 20, 18)

        assert poke.nature == "Bashful"

        assert poke.ability == 1

        assert slot == 1

        assert not seed_engine.has_encounter(frame, 10, 40)

        assert poke.get_hidden_power() == ("Rock", 35)

        # endregion

        # region MethodJ surfing synchronize 3

        frame = 1381  # Actual 1382

        poke_result = seed_engine.get_method_j_pokemon(frame, False, "Impish")
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "9f9d1268"

        assert poke.ivs == (26, 14, 4, 13, 14, 30)

        assert poke.nature == "Impish"

        assert poke.ability == 0

        assert slot == 0

        assert seed_engine.has_encounter(frame, 10, 40)

        assert poke.get_hidden_power() == ("Ground", 57)

        assert poke.occid == 1407

        # endregion

        # region MethodJ surfing

        frame = 1381  # Actual 1382

        poke_result = seed_engine.get_method_j_pokemon(frame, False)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "648f23bb"

        assert poke.ivs == (1, 12, 21, 6, 4, 19)

        assert poke.nature == "Calm"

        assert poke.ability == 1

        assert slot == 0

        assert seed_engine.has_encounter(frame, 10, 40)

        assert poke.get_hidden_power() == ("Ground", 45)

        assert poke.occid == 1464

        # endregion

        # region Method1

        frame = 103  # Actual frame 104

        poke = seed_engine.get_method_one_pokemon(frame)

        assert poke.pid == "fce62d93"

        assert poke.ivs == (31, 30, 31, 29, 28, 30)

        assert poke.nature == "Naughty"

        assert poke.ability == 1

        assert poke.get_hidden_power() == ("Bug", 39)

        # endregion

        # region PKRS

        assert seed_engine.has_pokerus(609)

        # endregion
