import time
import urllib
import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import re

from src.models.armor import armor_c

class spider(object):
    def __init__(self, headless=True, dtLoadPicture=True, disableGPU=True):
        self.chrome_option = webdriver.ChromeOptions()

        self.mkdir("./download")

        if dtLoadPicture == True:
            prefs = {"profile.managed_default_content_settings.images":2}
            self.chrome_option.add_experimental_option("prefs",prefs)
        if headless == True:
            self.chrome_option.add_argument("--headless")
        if disableGPU == True:
            self.chrome_option.add_argument("--disable-gpu")

        self.chrome_option.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')

        self.browser = None

        self.start_browser()

    def boot_up_browser(self):
        self.browser = webdriver.Chrome(options=self.chrome_option)
        self.browser.implicitly_wait(10)

    def start_browser(self):
        self.boot_up_browser()
        pass

    def get_armor(self):
        self.browser.get("http://mhwg.org/data/3300.html")
        armor_elements = self.browser.find_element_by_css_selector("div.f_min").find_elements_by_css_selector("a")
        armor_list = [[x.text, x.get_attribute("href")] for x in armor_elements]

        for i in range(len(armor_list)):
            print("------------------------------------------------------{0}------------------------------------------------------".format(i))
            self.get_armor_page(armor_list[i][1], armor_list[i][0])
        pass

    def get_armor_page(self, url, name):
        self.browser.get(url)

        ls_table = self.browser.find_elements_by_css_selector("table.t1")
        num = len(ls_table[1].find_elements_by_css_selector("tr")) - 2

        armors = [armor_c() for i in range(num)]
        # basic info
        version = ls_table[0].find_elements_by_css_selector("tr")[1].find_element_by_css_selector("span").text
        rare = int(ls_table[0].find_elements_by_css_selector("tr")[1].find_elements_by_css_selector("td")[1].text)
        gender = ls_table[0].find_elements_by_css_selector("tr")[1].find_elements_by_css_selector("td")[2].text
        for armor in armors:
            if version == "MHW":
                armor.game_version = armor.MHW
            else:
                armor.game_version = armor.MHWI
            armor.rare = rare
            if gender == "男女共用":
                armor.sex = armor.ALL_GENDER
            else:
                armor.sex = gender #------------------------------------------------------

        # names, defence, and element resistence
        defence_table = ls_table[1].find_elements_by_css_selector("tr")[1:num+1]
        for i in range(num):
            rows = defence_table[i].find_elements_by_css_selector("td")
            armors[i].defence.def_org = int(rows[1].text)
            armors[i].defence.element_resist = [int(rows[x].text) for x in range(2, 7)]


        # defence after enhance
        defence_enhance_table = ls_table[2].find_elements_by_css_selector("tr")[1:num+1]
        for i in range(num):
            rows = defence_enhance_table[i].find_elements_by_css_selector("td")
            armors[i].defence.def_enhance = int(rows[1].find_elements_by_css_selector("span")[1].text)
            armors[i].defence.def_custom = int(rows[2].find_elements_by_css_selector("span")[1].text)

        # custome enhance items
        custom_table = ls_table[3]
        items = custom_table.find_elements_by_css_selector("a")
        for item in items:
            item_id = re.search("[1-9][0-9]*", item.get_attribute("href")).group()
            item_num = re.search("(x)([1-9][0-9]*)", item.text).group(2)
            for armor in armors:
                armor.add_custom_item(int(item_id), int(item_num))
        for armor in armors:
            pa = custom_table.find_element_by_css_selector("tr td").text
            money = re.search(r"([1-9][0-9]*)(z)", pa).group(1)
            armor.add_custom_item(0, int(money)) #money
                

        # name, slots and skills
        skills_table = ls_table[4]
        rows = skills_table.find_elements_by_css_selector("tr")[1:num+1]
        for i in range(num):
            name = rows[i].find_element_by_css_selector("td").text
            armors[i].name = name

            slots = list(rows[i].find_elements_by_css_selector("td")[1].text)
            for slot in slots:
                lv = 0
                if slot == "④":
                    lv = 4
                elif slot == "③":
                    lv = 3
                elif slot == "②":
                    lv = 2
                else:
                    lv = 1
                armors[i].add_slot(lv)

            skills = rows[i].find_elements_by_css_selector("td")[2].find_elements_by_tag_name("a")
            levels = rows[i].find_elements_by_css_selector("td")[2].find_elements_by_tag_name("span")
            for j in range(len(skills)):
                skill_id = int(re.search("[1-9][0-9]*", skills[j].get_attribute("href")).group(0))
                skill_level = int(re.search("[1-9][0-9]*", levels[j].text).group(0))
                skill_name = skills[j].text
                armors[i].add_skill(skill_id, skill_level, skill_name)


        # sets skills
        set_skill_table = ls_table[6]
        if set_skill_table.find_elements_by_css_selector("tr")[1].text != "無し":
            skills = set_skill_table.find_elements_by_css_selector("tr")
            for i in range(1, len(skills)):
                skill = skills[i].find_element_by_css_selector("a")
                skill_id = re.search("[1-9][0-9]*", skill.get_attribute("href")).group()
                skill_name = skill.text
                for armor in armors:
                    armor.add_skill(int(skill_id), 1, skill_name)

        # items
        fee_table = ls_table[7]
        for armor in armors:
            armor.fee = fee_table.find_element_by_css_selector("td").text

        items_table = ls_table[8]
        rows = items_table.find_elements_by_css_selector("tr")[1:num+1]
        pattern = re.compile(r"\d+")
        for i in range(num):
            column = rows[i].find_elements_by_css_selector("td")[1]
            items = column.find_elements_by_css_selector("a")
            nums = pattern.findall(column.text)
            for j in range(len(nums)):
                item_id = re.search(r"[1-9][0-9]*", items[j].get_attribute("href")).group(0)
                item_name = items[j].text
                armors[i].add_item(item_id, nums[j])

        for armor in armors:
            print(armor)
        pass

    def get_skills(self):
        self.browser.get("http://mhwg.org/data/4103.html")

    @staticmethod
    def mkdir(dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
        return True

if __name__ == "__main__":
    a = spider()
    a.get_armor()
    pass