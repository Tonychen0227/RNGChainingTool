from models.enums import EncounterArea
from pearl_plat_seed import PearlPlatSeedEngine


class Test:
    def __init__(self):
        seed_engine = PearlPlatSeedEngine(7, 1, 18, 32, 46, 5719)  # DemoPlat
        seed_engine.populate(20000)

        assert seed_engine.initial_seed == "55121657"

        assert 1218, 16914 == seed_engine.get_tid_sid()

        # region MethodJ

        # region methodJ No Synchronize 1

        frame = 1285  # Actual frame 1826

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Grass)
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

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Grass)
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

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Grass)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "2c166ac5"

        assert poke.ivs == (17, 4, 31, 15, 2, 14)

        assert poke.nature == "Naughty"

        assert poke.ability == 1

        assert slot == 8

        assert poke.get_hidden_power() == ("Bug", 68)

        assert seed_engine.is_shiny(poke)
        # endregion

        # region MethodJ Synchronize success
        frame = 1326  # Actual frame 1327

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Grass, "Quiet")
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

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Grass, "Quiet")
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

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Surfing)
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

        # region MethodJ surfing 2

        frame = 1784  # Actual frame 1785

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Surfing)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "e0903636"

        assert poke.ivs == (11, 20, 0, 27, 4, 20)

        assert poke.nature == "Gentle"

        assert poke.ability == 0

        assert slot == 2

        assert poke.get_hidden_power() == ("Rock", 40)

        assert poke.occid == 1835

        # endregion

        # region MethodJ surfing synchronize 1

        frame = 1790  # Actual frame 1791

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Surfing, "Impish")
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

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Surfing, "Impish")
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

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Surfing, "Impish")
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

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.Surfing)
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

        # region MethodJ old rod

        frame = 3  # Actual frame 4

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.FishingOld)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "41cbabbc"

        assert poke.ivs == (2, 8, 31, 25, 24, 14)

        assert poke.nature == "Serious"

        assert poke.ability == 0

        assert slot == 1

        assert poke.get_hidden_power() == ("Rock", 38)

        assert poke.occid == 13

        # endregion

        # region MethodJ old rod synchronize 1

        frame = 3  # Actual frame 4

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.FishingOld, "Impish")
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "21577f16"

        assert poke.ivs == (31, 18, 16, 30, 21, 0)

        assert poke.nature == "Rash"

        assert poke.ability == 0

        assert slot == 1

        assert poke.get_hidden_power() == ("Steel", 42)

        assert poke.occid == 68

        # endregion

        # region MethodJ good rod

        frame = 14  # Actual frame 15

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.FishingGood)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "69f1f443"

        assert poke.ivs == (1, 13, 2, 25, 27, 12)

        assert poke.nature == "Serious"

        assert poke.ability == 1

        assert slot == 3

        assert poke.get_hidden_power() == ("Psychic", 52)

        assert poke.occid == 20

        # endregion

        # region MethodJ super rod

        frame = 3  # Actual frame 4

        poke_result = seed_engine.get_method_j_pokemon(frame, EncounterArea.FishingGood)
        poke = poke_result[0]
        slot = poke_result[1]

        assert poke.pid == "41cbabbc"

        assert poke.ivs == (2, 8, 31, 25, 24, 14)

        assert poke.nature == "Serious"

        assert poke.ability == 0

        assert slot == 2

        assert poke.get_hidden_power() == ("Rock", 38)

        assert poke.occid == 13

        # endregion

        # region Rods

        for x in [1, 4, 7, 9, 11, 15, 16]:
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingOld) is None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingGood) is None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingSuper) is None

        for x in [5, 6, 10, 12, 13, 17]:
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingOld) is None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingGood) is None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingSuper) is not None

        for x in [8, 14, 18, 21]:
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingOld) is None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingGood) is not None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingSuper) is not None

        for x in [0, 2, 3, 22]:
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingOld) is not None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingGood) is not None
            assert seed_engine.get_method_j_pokemon(x, EncounterArea.FishingSuper) is not None

        # region Fishing Slots
        for i in range(0, 10):
            frames = [72, 77, 90, 95, 97, 101, 103, 107, 108, 110]
            expected = [1, 0, 3, 1, 1, 1, 3, 0, 0, 1]
            assert seed_engine.get_method_j_pokemon(frames[i], EncounterArea.FishingOld)[1] == expected[i]

        for i in range(0, 10):
            frames = [2, 3, 8, 14, 18, 21, 22, 23, 24, 27]
            expected = [0, 2, 1, 3, 1, 0, 1, 1, 1, 2]
            assert seed_engine.get_method_j_pokemon(frames[i], EncounterArea.FishingGood)[1] == expected[i]

        for i in range(0, 10):
            frames = [80, 81, 82, 83, 86, 87, 88, 89, 90, 92]
            expected = [0, 1, 1, 4, 0, 1, 0, 0, 3, 0]
            assert seed_engine.get_method_j_pokemon(frames[i], EncounterArea.FishingSuper)[1] == expected[i]
        # endregion

        # endregion Rods

        # endregion MethodJ

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
