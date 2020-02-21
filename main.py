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
import time

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
            self.get_armor_page(armor_list[i][1])
        pass

    def get_armor_page(self, url):
        self.browser.get(url)

        soup = BeautifulSoup(self.browser.page_source, "lxml")
        # print(soup.prettify())

        ls_table = soup.find_all("table", class_="t1")
        num = len(ls_table[1].find_all("tr")) - 2
        armors = [armor_c() for i in range(num)]

        # basic infos
        version = ls_table[0].find_all("tr")[1].find("span").string
        rare = int(ls_table[0].find_all("tr")[1].find_all("td")[1].string)
        gender = ls_table[0].find_all("tr")[1].find_all("td")[2].string

        for armor in armors:
            armor.set_version(version)
            armor.set_rare(rare)
            armor.set_gender(gender)

        # defence and element resistence
        table = ls_table[1]
        rows = table.find_all("tr")[1:num+1]
        for i in range(num):
            columns = rows[i].find_all("td")
            armors[i].set_defence_original(int(columns[1].string))
            armors[i].set_defence_elements([int(columns[x].find("span", class_="b").string) for x in range(2, 7)])

        # type, and defence after enhance
        table = ls_table[2]
        rows = table.find_all("tr")[1:num+1]
        for i in range(num):
            columns = rows[i].find_all("td")
            armors[i].set_type(columns[0].string)
            armors[i].set_defence_after_enhance(int(columns[1].find("span", class_="b").string))
            armors[i].set_defence_after_custom(int(columns[2].find("span", class_="b").string))

        # custom enhance
        table = ls_table[3]
        items = table.find_all("a")
        for item in items:
            item_id = int(re.search("[1-9][0-9]*", item.attrs["href"]).group(0))
            tmp = re.search(r"(.*)( x)([1-9][0-9]*)", item.string)
            item_name = tmp.group(1)
            item_num = int(tmp.group(3))
            for armor in armors:
                armor.add_custom_item(item_name, item_id, item_num)
            pass
        for armor in armors:
            pa = table.find("td").text
            money = int(re.search(r"([1-9][0-9]*)(z)", pa).group(1))
            armor.fee_custom = money

        # name, slots, and skills
        table = ls_table[4]
        rows = table.find_all("tr")[1:num+1]
        for i in range(num):
            columns = rows[i].find_all("td")
            name = columns[0].text.replace("\n", "").replace(" ", "")
            armors[i].name = name

            slots = list(columns[1].string.replace("\n", "").replace(" ", ""))
            for slot in slots:
                armors[i].add_slot(slot)

            skills = columns[2].find_all("a")
            levels = columns[2].find_all("span")
            for j in range(len(skills)):
                skill_id = int(re.search("[1-9][0-9]*", skills[j].attrs["href"]).group(0))
                skill_level = int(re.search("[1-9][0-9]*", levels[j].string).group(0))
                skill_name = skills[j].string
                armors[i].add_skill(skill_id, skill_level, skill_name)
            pass

        # set skills
        table = ls_table[6]
        if table.find_all("tr")[1].find("td").string == None:
            skills = table.find_all("tr")
            for i in range(1, len(skills)):
                skill = skills[i].find("a")
                skill_id = int(re.search("[1-9][0-9]*", skill.attrs["href"]).group())
                skill_name = skill.string
                for armor in armors:
                    armor.add_skill(skill_id, 1, skill_name)

        # items 
        table = ls_table[7]
        if table.find("td").string != None:
            for armor in armors:
                armor.fee = int(re.search("[1-9][0-9]*",table.find("td").string).group(0))


        table = ls_table[8]
        rows = table.find_all("tr")[1:num+1]
        pattern = re.compile(r"\d+")

        # a = rows[0].find("td")
        if rows[0].find("td").text == "頭":
            for i in range(num):
                columns = rows[i].find_all("td")
                if len(columns) == 2:
                    column = columns[1]

                try: 
                    items = column.find_all("a")
                    nums = pattern.findall(column.text)
                    for j in range(len(nums)):
                        item_id = int(re.search(r"[1-9][0-9]*", items[j].attrs["href"]).group(0))
                        item_name = items[j].string
                        armors[i].add_item(item_name, item_id, nums[j])
                except:
                    print("special armor")

        for armor in armors:
            print(armor)
        pass

    def get_skills(self):
        self.browser.get("http://mhwg.org/data/4103.html")

    @staticmethod
    def clean_string(char):
        return char.replace("\n", "").replace(" ", "")

    @staticmethod
    def mkdir(dir):
        if not os.path.exists(dir):
            os.mkdir(dir)
        return True

if __name__ == "__main__":
    a = spider()
    # a.get_armor()
    # a.get_armor_page("http://mhwg.org/ida/226849.html")
    a.get_armor_page("http://mhwg.org/ida/246519.html")
    pass