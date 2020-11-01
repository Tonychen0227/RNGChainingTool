import math


class Pokemon:
    def __init__(self, frame, pid, ability, ivs, nature, gender_determinator, occid, item_determinator):
        self.frame = frame
        self.pid = pid
        self.ability = ability
        self.hp_iv = ivs[0]
        self.atk_iv = ivs[1]
        self.def_iv = ivs[2]
        self.spatk_iv = ivs[3]
        self.spdef_iv = ivs[4]
        self.spe_iv = ivs[5]
        self.ivs = ivs
        self.nature = nature
        self.gender_determinator = gender_determinator
        self.occid = occid
        self.item_determinator = item_determinator

    def get_is_female(self, threshold: int) -> bool:
        if threshold not in [12.5, 25, 50, 75]:
            raise ValueError("Invalid gender threshold")

        if threshold == 12.5:
            return self.gender_determinator <= 30
        elif threshold == 25:
            return self.gender_determinator <= 63
        elif threshold == 50:
            return self.gender_determinator <= 126
        else:
            return self.gender_determinator < 190

    def print(self) -> None:
        print(f"Frame: {self.frame} PID: {self.pid.upper()} ({self.ability}) Occid {self.occid} {self.nature} "
              f"{self.ivs} {self.get_hidden_power()} ITEM {self.item_determinator}")
        return

    def get_hidden_power(self) -> (str, int):
        types = ["Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire",
                 "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark"]
        a = self.hp_iv % 2
        b = self.atk_iv % 2
        c = self.def_iv % 2
        d = self.spe_iv % 2
        e = self.spatk_iv % 2
        f = self.spdef_iv % 2

        type = types[math.floor((a + 2*b + 4*c + 8*d + 16*e + 32*f) * 15 / 63)]

        u = math.floor(self.hp_iv % 4 / 2)
        v = math.floor(self.atk_iv % 4 / 2)
        w = math.floor(self.def_iv % 4 / 2)
        x = math.floor(self.spe_iv % 4 / 2)
        y = math.floor(self.spatk_iv % 4 / 2)
        z = math.floor(self.spdef_iv % 4 / 2)

        damage = math.floor(((u + 2*v + 4*w + 8*x + 16*y + 32*z) * 40 / 63) + 30)

        return type, damage
