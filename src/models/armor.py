class armor_c(object):
    MHW = 0
    MHWI = 1
    ALL_GENDER = 0
    MALE_ONLY = 1
    FEMALE_ONLY = 2
    def __init__(self):
        # basic info
        self.name = ""
        self.game_version = 0 # 0 MHW 1 MHWI
        self.rare = 0
        self.sex = 0 # 0 all 1 male 2 female
    
        self.defence = defence_c()

        # custome enhance items
        self.custom_items = []

        # skills
        self.slots = []
        self.skills = []

        # items and fee
        self.items = []
    
    def __str__(self):
        [x.lv for x in self.slots]
        [x.name + str(x.lv) for x in self.skills]
        [str(x.id) + "x" + str(x.num) for x in self.items]
        return "Name: {0}, Rare: {1}, Sex: {2}, Def: {3}, Ele-resist: {4}\n    Slots: {5}, Skills: {6}\n    Items: {7}\n    Custom-enhancement Items: {8}\n".format(self.name, self.rare, self.sex, [self.defence.def_org, self.defence.def_enhance, self.defence.def_custom], self.defence.element_resist, [x.lv for x in self.slots], [x.name + str(x.lv) for x in self.skills], [str(x.id) + "x" + str(x.num) for x in self.items], [str(x.id) + "x" + str(x.num) for x in self.custom_items])


    def add_slot(self, lv):
        tmp = slots_c()
        self.slots.append(tmp)

    def add_skill(self, id, lv, name):
        tmp = skills_c()
        tmp.id = id
        tmp.lv = lv
        tmp.name = name
        self.skills.append(tmp)

    def add_item(self, id, num):
        tmp = items_c()
        tmp.id = id
        tmp.num = num
        self.items.append(tmp)
    
    def add_custom_item(self, id, num):
        tmp = items_c()
        tmp.id = id
        tmp.num = num
        self.custom_items.append(tmp)


class defence_c(object):
    def __init__(self):
        self.def_org = 0
        self.def_enhance = 0
        self.def_custom = 0

        self.element_resist = [0, 0, 0, 0, 0]

class slots_c(object):
    def __init__(self):
        self.lv = 0

    def __str__(self):
        return str(self.lv)

class skills_c(object):
    def __init__(self):
        self.id = 0
        self.lv = 0
        self.name = ""
        pass

    def __str__(self):
        return str(self.name) + str(self.lv)

class items_c(object):
    def __init__(self):
        self.id = 0
        self.num = 0
