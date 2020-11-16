import abc

from models.enums import EncounterArea
from pearl_plat_seed import PearlPlatSeedEngine


class VerifiableQuery:
    @abc.abstractmethod
    def verify_frames(self, seed_engine: PearlPlatSeedEngine) -> []:
        return


class PKRS(VerifiableQuery):
    def __init__(self):
        self.min_frame = 0
        self.max_frame = 0
        self.label = "PKRS"

    def verify_frames(self, seed_engine: PearlPlatSeedEngine):
        good = False
        for frame in range(self.min_frame, self.max_frame + 1):
            if seed_engine.call(frame) in ["4000", "8000", "c000"]:
                if not good:
                    good = []
                good.append(frame)

        return good


class Method1(VerifiableQuery):
    def __init__(self):
        self.min_frame = 0
        self.max_frame = 0
        self.natures = []
        self.hidden_power_types = []
        self.min_hidden_power = 0
        self.min_ivs = []
        self.max_ivs = []
        self.ability = 0
        self.is_shiny = False
        self.gives_pokerus = False
        self.label = "Method1"
        self.tid = 0
        self.sid = 0

    def verify_frames(self, seed_engine: PearlPlatSeedEngine):
        good = False
        for frame in range(self.min_frame, self.max_frame + 1):
            poke = seed_engine.get_method_one_pokemon(frame)

            if self.natures is not None and poke.nature not in self.natures:
                continue

            if self.hidden_power_types is not None and poke.get_hidden_power()[0] not in self.hidden_power_types:
                continue

            if self.min_hidden_power is not None and self.min_hidden_power > int(poke.get_hidden_power()[1]):
                continue

            poke_ivs = poke.ivs

            if self.min_ivs is not None:
                low_ivs = [poke_ivs[x] - self.min_ivs[x] for x in range(0, 6)]

                if min(low_ivs) < 0:
                    continue

            if self.max_ivs is not None:
                high_ivs = [self.max_ivs[x] - poke_ivs[x] for x in range(0, 6)]

                if min(high_ivs) < 0:
                    continue

            if self.ability is not None and self.ability != int(poke.ability):
                continue

            if self.is_shiny and not seed_engine.is_shiny(poke, self.tid, self.sid):
                continue

            if self.gives_pokerus and not seed_engine.has_pokerus(poke.occid):
                continue

            if not good:
                good = []
            good.append(frame)

        return good


class MethodJ(VerifiableQuery):
    def __init__(self):
        self.min_frame = 0
        self.max_frame = 0
        self.natures = []
        self.hidden_power_types = []
        self.min_hidden_power = 0
        self.min_ivs = []
        self.max_ivs = []
        self.ability = 0
        self.is_shiny = False
        self.gives_pokerus = False
        self.enc_slots = []
        self.min_item_deter = 0
        self.max_item_deter = 100
        self.enc_rate = 70
        self.movement_rate = 30
        self.encounter_area = 0
        self.min_level_water = 0
        self.max_level_water = 100
        self.min_avail_level_water = 0
        self.max_avail_level_water = 100
        self.ignore_encounter_check = False
        self.synchronize_target = []
        self.synchronize_natures = []
        self.label = "MethodJ"
        self.tid = 0
        self.sid = 0

    def verify_frames(self, seed_engine: PearlPlatSeedEngine):
        good = False
        for frame in range(self.min_frame, self.max_frame + 1):
            for synchronize_nature in self.synchronize_natures:
                poke_result = seed_engine.get_method_j_pokemon(frame, self.encounter_area, synchronize_nature)

                if poke_result is None:
                    continue

                poke = poke_result[0]
                slot = poke_result[1]

                if self.natures is not None and poke.nature not in self.natures:
                    continue

                hidden_power = poke.get_hidden_power()

                if self.hidden_power_types is not None and hidden_power[0] not in self.hidden_power_types:
                    continue

                if self.hidden_power_types is not None and self.min_hidden_power > int(hidden_power[1]):
                    continue

                poke_ivs = poke.ivs

                if self.min_ivs is not None:
                    low_ivs = [int(a) - b for a, b in zip(poke_ivs, self.min_ivs)]

                    if min(low_ivs) < 0:
                        continue

                if self.max_ivs is not None:
                    high_ivs = [b - int(a) for a, b in zip(poke_ivs, self.max_ivs)]

                    if min(high_ivs) < 0:
                        continue

                if self.ability is not None and self.ability != int(poke.ability):
                    continue

                if self.is_shiny and not seed_engine.is_shiny(poke, self.tid, self.sid):
                    continue

                poke_item = poke.item_determinator
                if self.min_item_deter is not None and int(poke_item) < self.min_item_deter:
                    continue

                if not self.ignore_encounter_check and not \
                        seed_engine.has_encounter(frame, self.enc_rate, self.movement_rate):
                    continue

                if self.enc_slots is not None and int(slot) not in self.enc_slots:
                    continue

                if self.gives_pokerus and not seed_engine.has_pokerus(poke.occid):
                    continue

                if self.encounter_area >= 1:
                    if self.encounter_area >= 2:
                        level = seed_engine.get_level(frame+1, self.min_avail_level_water, self.max_avail_level_water)
                    else:
                        level = seed_engine.get_level(frame, self.min_avail_level_water, self.max_avail_level_water)
                    if level < self.min_level_water or level > self.max_level_water:
                        continue

                if not good:
                    good = []
                good.append(frame)

        return good
