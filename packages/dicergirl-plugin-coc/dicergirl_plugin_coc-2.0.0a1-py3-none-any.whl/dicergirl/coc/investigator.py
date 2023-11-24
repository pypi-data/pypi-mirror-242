import random

build_dict = {64: -2, 84: -1, 124: 0, 164: 1,
              204: 2, 284: 3, 364: 4, 444: 5, 524: 6}
db_dict = {-2: "-2", -1: "-1", 0: "0", 1: "1d4",
           2: "1d6", 3: "2d6", 4: "3d6", 5: "4d6", 6: "5d6"}

def randattr(time: int = 3, ex: int = 0):
    r = 0
    for _ in range(time):
        r += random.randint(1, 6)
    return (r+ex)*5

class Investigator(object):
    """ COC 调查员人物卡 """
    def __init__(self) -> None:
        self.name = "无名调查员"
        self.age = 20
        self.sex = "女"
        self.str = randattr()
        self.con = randattr()
        self.siz = randattr(2, 6)
        self.dex = randattr()
        self.app = randattr()
        self.int = randattr(2, 6)
        self.pow = randattr()
        self.edu = randattr(2, 6)
        self.luc = randattr()
        self.san = self.pow
        self.hp = self.lp_max()
        self.skills = {}
        self.tools = {}

    def body_build(self) -> int:
        build = self.str + self.con
        for i, j in build_dict.items():
            if build <= i:
                return j
        return

    def db(self) -> str:
        return db_dict[self.body_build()]

    def lp_max(self) -> int:
        return (self.con+self.siz)//10

    def mov(self) -> int:
        r = 8
        if self.age >= 80:
            r -= 5
        elif self.age >= 70:
            r -= 4
        elif self.age >= 60:
            r -= 3
        elif self.age >= 50:
            r -= 2
        elif self.age >= 40:
            r -= 1
        if self.str < self.siz and self.dex < self.siz:
            return r-1
        elif self.str > self.siz and self.dex > self.siz:
            return r+1
        else:
            return r

    def edu_up(self) -> str:
        edu_check = random.randint(1, 100)
        if edu_check > self.edu:
            edu_en = random.randint(1, 10)
            self.edu += edu_en
        else:
            return "教育成长检定D100=%d, 小于%d, 无增长。" % (edu_check, self.edu)
        if self.edu > 99:
            self.edu = 99
            return "教育成长检定D100=%d, 成长1D10=%d, 成长到了最高值99！" % (edu_check, edu_en)
        else:
            return "教育成长检定D100=%d, 成长1D10=%d, 成长到了%d" % (edu_check, edu_en, self.edu)

    def edu_ups(self, times) -> str:
        r = ""
        for _ in range(times):
            r += self.edu_up()
        return r

    def sum_down(self, sum) -> str:
        if self.str + self.con + self.dex-45 < sum:
            self.str = 15
            self.con = 15
            self.dex = 15
        else:
            str_lost = random.randint(0, min(sum, self.str-15))
            while sum - str_lost > self.con + self.dex-30:
                str_lost = random.randint(0, min(sum, self.str-15))
            self.str -= str_lost
            sum -= str_lost
            con_lost = random.randint(0, min(sum, self.con-15))
            while sum - con_lost > self.dex-15:
                con_lost = random.randint(0, min(sum, self.con-15))
            self.con -= con_lost
            sum -= con_lost
            self.dex -= sum
        return

    def age_change(self, age: int = 20) -> str:
        if self.age != 20:
            return  # 防止多次年龄增强判定
        if age < 15:
            return "年龄过小, 无法担当调查员"
        elif age >= 90:
            return "该调查员已经作古, 他(或者她)由于年龄过大, 遭到了神祇「克苏鲁」的注视."
        self.age = age
        if 15 <= age < 20:
            self.str -= 5
            self.siz -= 5
            self.edu -= 5
            luc = randattr()
            self.luc = luc if luc > self.luc else self.luc
            return "力量、体型、教育值-5, 幸运增强判定一次"
        elif age < 40:
            self.edu_up()
            return "教育增强判定一次"
        elif age < 50:
            self.app -= 5
            self.sum_down(5)
            self.edu_ups(2)
            return "外貌-5, 力量、体型、敏捷合计降低5, 教育增强判定两次"
        elif age < 60:
            self.app -= 10
            self.sum_down(10)
            self.edu_ups(3)
            return "外貌-10, 力量、体型、敏捷合计降低10, 教育增强判定三次"
        elif age < 70:
            self.app -= 15
            self.sum_down(20)
            self.edu_ups(4)
            return "外貌-15, 力量、体型、敏捷合计降低20, 教育增强判定四次"
        elif age < 80:
            self.app -= 20
            self.sum_down(40)
            self.edu_ups(4)
            return "外貌-20, 力量、体型、敏捷合计降低40, 教育增强判定四次"
        elif age < 90:
            self.app -= 25
            self.sum_down(80)
            self.edu_ups(4)
            return "外貌-25, 力量、体型、敏捷合计降低80, 教育增强判定四次"

    def __repr__(self):
        data = "姓名: %s\n" % self.name
        data += "性别: %s 年龄: %d\n" % (self.sex, self.age)
        data += "力量: %d 体质: %d 体型: %d\n" % (self.str, self.con, self.siz)
        data += "敏捷: %d 外貌: %d 智力: %d\n" % (self.dex, self.app, self.int)
        data += "意志: %d 教育: %d 幸运: %d\n" % (self.pow, self.edu, self.luc)
        data += "DB: %s 移动速度: %d SAN: %d\n" % (self.db(), self.mov(), self.san)
        data += "生命值: %d/%d" % (self.hp, self.lp_max())
        return data

    def skills_output(self) -> str:
        if not self.skills:
            return "%s 当前无任何技能数据。" % self.name
        r = "%s技能数据: " % self.name
        for k, v in self.skills.items():
            r += "\n%s: %d" % (k, v)
        return r

    def output(self) -> str:
        return self.__repr__()

    def rollcount(self) -> tuple:
        return (self.__count(), self.__count() + self.luc)

    def __count(self):
        return self.str + self.con + self.siz + self.dex + self.app + self.int + self.pow + self.edu

    def load(self, data: dict):
        self.__dict__.update(data)
        return self
