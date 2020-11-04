from typing import Tuple

from models.pokemon import Pokemon


class PearlPlatSeedEngine:
    def __init__(self, month, day, hour, minute, second, delay):
        ab = month * day + minute + second
        ab = hex(ab & 0xff)[2:]

        while len(ab) < 2:
            ab = "0" + ab

        cd = hex(hour)[2:]

        while len(cd) < 2:
            cd = "0" + cd

        delay = delay

        efgh = hex(delay)[2:]

        while len(efgh) < 4:
            efgh = "0" + efgh

        self.initial_seed = ab + cd + efgh

        self.populated_frames = False
        self.populated_tid_sid = False

        self.frames = None
        self.cached_method_1 = {}

        self.sid = -1
        self.tid = -1

        self.max_frames = -1

    def populate(self, frames):
        if self.populated_frames:
            return

        self.max_frames = frames

        self.frames = {0: int(self.initial_seed, 16)}

        for x in range(1, self.max_frames):
            self.frames[x] = (self.frames[x - 1] * 0x41c64e6d + 0x6073) & 0xFFFFFFFF

        self.populated_frames = True

    def get_tid_sid(self):
        if not self.populated_tid_sid:
            # MTFast(u32 seed, u32 advances=0)
            mt = [0] * 400

            seed = int(self.initial_seed.lower(), 16)

            mt[0] = seed

            bits_32 = 1 << 32

            for index in range(1, 399):
                seed = (0x6c078965 * (seed ^ (seed >> 30)) + index) & (bits_32 - 1)
                mt[index] = seed

            # Shuffle
            for i in range(0, 2):
                m0 = mt[i]
                m1 = mt[i + 1]

                y = (m0 & 0x80000000) | (m1 & 0x7fffffff)

                y1 = y >> 1

                if y & 1:
                    y1 ^= 0x9908b0df
                    y1 = y1

                mt[i] = y1 ^ mt[i + 397]

            y = mt[1]
            y ^= (y >> 11)
            y ^= ((y << 7) & 0x9d2c5680)
            y ^= ((y << 15) & 0xefc60000)
            y ^= (y >> 18)

            tid = y & 0xFFFF
            sid = y >> 16

            del mt

            self.tid = tid
            self.sid = sid

            self.populated_tid_sid = True

        return self.tid, self.sid

    def get_initial_seed(self):
        return self.initial_seed.upper()

    def get(self, frame):
        if frame >= self.max_frames:
            current_frame = self.frames[self.max_frames - 1]
            while frame >= self.max_frames:
                current_frame = (current_frame * 0x41c64e6d + 0x6073) & 0xFFFFFFFF
                self.frames[self.max_frames] = current_frame
                self.max_frames += 1
        elif frame < 0:
            raise ValueError("You cannot ask for a frame smaller than 0")
        return self.frames[frame]

    def call(self, frame: int) -> str:
        value = str(hex((self.get(frame) * 0x41c64e6d + 0x6073) & 0xFFFFFFFF))[2:][:-4]
        while len(value) < 4:
            value = "0" + value

        return value

    def get_level(self, frame: int, min_level: int, max_level: int):
        call = self.call(frame + 1)
        level_range = max_level - min_level + 1
        increment = int(call, 16) % level_range
        return increment + min_level

    def has_encounter(self, frame: int, enc_rate: int, movement_rate: int) -> bool:
        if frame <= 2:
            return False

        current_frame = frame - 2

        first_call = int(self.call(current_frame), 16)
        current_frame += 1
        second_call = int(self.call(current_frame), 16)

        return first_call / 0x290 < movement_rate and second_call / 0x290 < enc_rate

    def has_pokerus(self, frame):
        if self.call(frame) in ["4000", "8000", "c000"]:
            return True
        else:
            return False

    def is_shiny(self, pokemon: Pokemon, tid=None, sid=None) -> bool:
        top_call = int(pokemon.pid[:4].lower(), 16)
        bottom_call = int(pokemon.pid[4:].lower(), 16)

        if tid and sid:
            self.tid = tid
            self.sid = sid
        elif not self.populated_tid_sid:
            self.get_tid_sid()
        else:
            return False

        return self.tid ^ self.sid ^ top_call ^ bottom_call < 8

    def get_method_one_pokemon(self, frame) -> Pokemon:
        if frame in self.cached_method_1:
            return self.cached_method_1[frame]

        current_frame = frame
        first_call = self.call(current_frame)
        current_frame += 1
        second_call = self.call(current_frame)
        current_frame += 1
        third_call = self.call(current_frame)
        current_frame += 1
        fourth_call = self.call(current_frame)

        pid = second_call + first_call

        nature_value = int(pid, 16) % 25

        while nature_value > 24:
            nature_value -= 25

        nature = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish",
               "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful",
               "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"][nature_value]

        ability = int(pid, 16) % 2

        big_hex = third_call + fourth_call
        big_binary = bin(int(big_hex, 16))[2:].zfill(32)

        def_iv = int(big_binary[1:6], 2)
        atk_iv = int(big_binary[6:11], 2)
        hp_iv = int(big_binary[11:16], 2)
        spdef_iv = int(big_binary[17:22], 2)
        spatk_iv = int(big_binary[22:27], 2)
        spe_iv = int(big_binary[27:32], 2)

        ivs = (hp_iv, atk_iv, def_iv, spatk_iv, spdef_iv, spe_iv)

        determinator = int(pid[-2:], 16)

        new_pokemon = Pokemon(frame, pid, ability, ivs, nature, determinator, frame + 4, 0)

        self.cached_method_1[frame] = new_pokemon

        return new_pokemon

    def get_method_j_pokemon(self, frame, encounter_area: int, synchronize_nature: str = None) -> Tuple[Pokemon, int] or None:
        current_frame = frame

        if encounter_area >= 1:
            encounter_call = int(self.call(current_frame), 16)
            if encounter_area == 1:
                target_slots = [60, 90, 95, 99, 100]
            elif encounter_call / 656 >= (encounter_area - 1)*25:
                return None
            else:
                if encounter_area >= 3:
                    target_slots = [40, 80, 95, 99, 100]
                else:
                    target_slots = [60, 90, 95, 99, 100]
        else:
            target_slots = [20, 40, 50, 60, 70, 80, 85, 90, 94, 98, 99, 100]

        slot = 255

        if encounter_area >= 2:
            slots_call = int(self.call(current_frame+1), 16)
        else:
            slots_call = int(self.call(current_frame), 16)

        for x in range(0, len(target_slots)):
            if slots_call / 656 < target_slots[x]:
                slot = x
                break

        if encounter_area >= 1:
            current_frame += 1

        if encounter_area >= 2:
            current_frame += 1

        current_frame += 1

        call = self.call(current_frame)

        if synchronize_nature is not None:
            if int(call, 16) >> 15 == 0:
                nature_value = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish",
               "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful",
               "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"].index(synchronize_nature)
            else:
                current_frame += 1
                call = self.call(current_frame)
                nature_value = int(call, 16) // 0xA3E
        else:
            nature_value = int(call, 16) // 0xA3E

        nature = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish",
               "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful",
               "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"][nature_value]

        call_1 = current_frame + 1
        call_2 = current_frame + 2

        pid = int(self.call(call_2), 16) << 16 | int(self.call(call_1), 16)

        while pid % 25 != nature_value:
            call_1 += 2
            call_2 += 2

            pid = int(self.call(call_2), 16) << 16 | int(self.call(call_1), 16)

        pid = hex(pid)[2:]

        ability = int(pid, 16) % 2

        while len(pid) < 8:
            pid = "0" + pid

        item_determinator = int(pid[-2:], 16)

        big_hex = self.call(call_1 + 2) + self.call(call_2 + 2)
        big_binary = bin(int(big_hex, 16))[2:].zfill(32)

        def_iv, atk_iv, hp_iv = int(big_binary[1:6], 2), int(big_binary[6:11], 2), int(big_binary[11:16], 2)
        spdef_iv, spatk_iv, spe_iv = int(big_binary[17:22], 2), int(big_binary[22:27], 2), int(big_binary[27:32], 2)

        ivs = (hp_iv, atk_iv, def_iv, spatk_iv, spdef_iv, spe_iv)

        occid = call_1

        method_one = self.get_method_one_pokemon(occid)

        while method_one.nature != nature:
            occid += 1
            method_one = self.get_method_one_pokemon(occid)

        occid_item = occid + 4

        return Pokemon(frame, pid, ability, ivs, nature, item_determinator, occid,
                       int(self.call(occid_item), 16) % 100), slot
