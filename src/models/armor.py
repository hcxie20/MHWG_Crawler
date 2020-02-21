class armor_c(object):
    MHW = 0
    MHWI = 1
    GENDER_ALL = 0
    MALE_ONLY = 1
    FEMALE_ONLY = 2
    HAT = 0
    CHEST = 1
    GLOVES = 2
    SKIRT = 3
    SHOES = 4
    ArmorType = {0:"頭", 1:"胴", 2:"腕", 3:"腰", 4:"脚",}
    GenderType = {0:"男女共用"}
    def __init__(self):
        # basic info
        self.name = ""
        self.game_version = None # 0 MHW 1 MHWI
        self.rare = None
        self.gender = None # 0 all 1 male 2 female
        self.type = None
    
        self.defence = defence_c()

        # custome enhance items
        self.custom_items = []

        # skills
        self.slots = []
        self.skills = []

        # items and fee
        self.items = []
        self.fee = None
        self.fee_custom = None
    
    def __str__(self):
        [x.lv for x in self.slots]
        [x.name + str(x.lv) for x in self.skills]
        [str(x.id) + "x" + str(x.num) for x in self.items]
        return "Name: {0}, Type: {9},  Rare: {1}, gender: {2}, Def: {3}, Ele-resist: {4}\n    Fee: {10}, Custom-Fee: {11}\n    Slots: {5}, Skills: {6}\n    Items: {7}\n    Custom-enhancement Items: {8}\n".format(self.name, self.rare, self.gender, [self.defence.def_org, self.defence.def_enhance, self.defence.def_custom], self.defence.element_resist, [x.lv for x in self.slots], [x.name + str(x.lv) for x in self.skills], [str(x.name) + "x" + str(x.num) for x in self.items], [str(x.name) + "x" + str(x.num) for x in self.custom_items], self.ArmorType[self.type], self.fee, self.fee_custom)


    def add_slot(self, char):
        tmp = slots_c()
        lv = None
        if char == "④":
            lv = 4
        elif char == "③":
            lv = 3
        elif char == "②":
            lv = 2
        elif char == "①":
            lv = 1
        if lv != None: 
            tmp.lv = lv
            self.slots.append(tmp)

    def add_skill(self, id, lv, name):
        tmp = skills_c()
        tmp.id = id
        tmp.lv = lv
        tmp.name = name
        self.skills.append(tmp)

    def add_item(self, name, id, num):
        tmp = items_c()
        tmp.name = name
        tmp.id = id
        tmp.num = num
        self.items.append(tmp)
    
    def add_custom_item(self, name, id, num):
        tmp = items_c()
        tmp.name = name
        tmp.id = id
        tmp.num = num
        self.custom_items.append(tmp)

    def set_type(self, _type):
        if _type == "頭":
            self.type = self.HAT
        elif _type == "胴":
            self.type = self.CHEST
        elif _type == "腕":
            self.type = self.GLOVES
        elif _type == "腰":
            self.type = self.SKIRT
        else:
            self.type = self.SHOES

    def set_version(self, version):
        if version == "MHW":
            self.game_version = self.MHW
        elif version == "MHWI":
            self.game_version = self.MHWI

    def set_rare(self, rare):
        self.rare = rare

    def set_gender(self, gender):
        if gender == "男女共用":
            self.gender = self.GENDER_ALL

    def set_defence_original(self, defn):
        self.defence.def_org = defn

    def set_defence_after_enhance(self, defn):
        self.defence.def_enhance = defn

    def set_defence_after_custom(self, defn):
        self.defence.def_custom = defn

    def set_defence_elements(self, rist):
        self.defence.element_resist = rist


class defence_c(object):
    def __init__(self):
        self.def_org = None
        self.def_enhance = None
        self.def_custom = None

        self.element_resist = [None, None, None, None, None]

class slots_c(object):
    def __init__(self):
        self.lv = None

    def __str__(self):
        return str(self.lv)

class skills_c(object):
    def __init__(self):
        self.id = None
        self.lv = None
        self.name = ""
        pass

    def __str__(self):
        return str(self.name) + str(self.lv)

class items_c(object):
    def __init__(self):
        self.name = None
        self.id = None
        self.num = None
