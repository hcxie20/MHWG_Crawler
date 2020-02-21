# MHWG_Crawler

An Python script to crawl http://mhwg.org/ for database of MHWI sets generator

# models

## Skill
- id: int, id of a skill. index of the html file on mhwg.org
- name: string
- lv_max: int, maxmum level of this skill
- description: string
- isSet: int
    - 0: not a set skill
    - 1: a set skill

## Weapon
armorc:
- name: string
- game_version: int
    - 0 -> MHW
    - 1 -> MHWI
- rare: int, rare
- sex: int
    - 0: all
    - 1: male
    - 2: female
- type: int
    - 0: hat
    - 1: chest
    - 2: gloves
    - 3: skirt
    - 4: shoes
- defence: class defence_c, as listed below
- item_custom: list of class items_c item for custome enhancement
- slots: list of class slots_c
- skills: list of class skills_c, skills this armor has. 
    Regard set skills as a special skill
- fee: int, money to build
- fee_custom: int, money for custom enhance
- items: list of class items_c, items to build this armor
    - if id == 0 and num == 0: special armor which cannot be built, often a gift from certain quest
        if there is a such item, it's a special armor

- [Method] add_slot(lv)
- [Method] add_skill(id, lv)
- [Method] add_item(name, id, num)
- [Method] add_custom_item(name, id, num)
- [Method] set_type(_type)
- [Method] add_slot
- [Method] set_version(version)
- [Method] set_rare(rare)
- [Method] set_gender(gender)
- [Method] set_defence_original(defence)
- [Method] set_defence_after_enhance(defence)
- [Method] set_defence_after_custom(defence)
- [Method] set_defence_elements([defence])


defence_c:
- def_org: int original defence
- def_enhance: int defence after enhancement
- def_custom: int defence after custome enhancement
- element_resist: list
    - 0: fire
    - 1: water
    - 2: electric
    - 3: ice
    - 4: dragon

skills_c:
- id: int
- lv: int
- name: string

items_c:
- name: string
- id: int
- num: num of items needed
    (money: id=0)



