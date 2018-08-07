# coding=utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# imagefilter ：滤镜
import random
import os
import uuid


class Verify_Code:
    # 随机一个字符(ASCII码)，这个字符是字母或数字
    def random_chr(self):
        num = random.randint(1, 3)
        if num == 1:
            # 随机一个0~9的数字
            rand_chr = random.randint(97, 122)
            # return random.randint(0,9)
            pass
        elif num == 2:
            # 随机一个小写字母
            rand_chr = random.randint(65, 90)
            pass
        else:
            # 随机一个大写字母
            rand_chr = random.randint(48, 57)
            pass
        return chr(rand_chr)  # 转成对应的字符

    # 随机一个干扰字符
    def random_disturb_chr(self):
        arr = ['.', '~', '^', '_', '-', " ", '*', ' ']
        return arr[random.randint(0, len(arr) - 1)]

    # 随即一个颜色，RGB
    def random_color(self):
        return (random.randint(30, 255), random.randint(56, 255), random.randint(56, 255))

    # 生成验证码
    def create_verification_code(self):
        # 创建图片
        height = 60  # px
        weight = 240
        image = Image.new("RGB", (weight, height), (192, 192, 192))
        font_file = self.get_font()
        print(font_file)
        font_dis_chr = ImageFont.truetype(font=font_file, size=20)  # 创建字体对象，字体大小是30
        font_chr = ImageFont.truetype(font=font_file, size=30)  # 创建字体对象，字体大小是30
        draw = ImageDraw.Draw(image)
        # 添加像素点,间隔是5像素
        for x in range(0, weight, 5):  # 最后的5代表间隔
            for y in range(0, height, 5):
                draw.point((x, y), fill=self.random_color())
        # 添加干扰字符，到上下左右边缘是5像素，间隔是30
        for x in range(5, weight - 5, 30):
            for y in range(10, height - 10, 15):
                distrub_char = self.random_disturb_chr()
                draw.text((x, y), distrub_char, fill=self.random_color(), font=font_dis_chr)
        # 添加字符 --一共四个
        self.chars = ''
        for n in range(1, 5):
            self.chars += self.random_chr()
            x = (weight - 50) / 4 * n  # 横轴坐标，10*2是左右边距
            y = random.randint(10, height - 30)
            draw.text((x, y), self.chars[n - 1], fill=self.random_color(), font=font_chr)
        #字符转成小写，便于判断
        self.chars=self.chars.lower()

        #print(self.chars)
        # 添加模糊效果
        image.filter(ImageFilter.BLUR)
        # 保存
        image_name = "{}.jpeg".format(uuid.uuid4().hex)
        image_doc = os.path.join(os.path.dirname(__file__), "static{0}verifycode".format(os.sep))
        if not os.path.exists(image_doc):
            os.mkdir(image_doc)
        #图片路径属于对象
        self.image_path=os.path.join(image_doc,image_name)
        print(self.image_path)
        image.save(self.image_path, format="jpeg")
        #image.show()

    def get_font(self):
        # 获取字体
        # 获取随机的字体文件
        flag = True
        font_file = "arial.ttf"
        if flag:
            font_name = random.randint(1, 3)
            font_file=os.path.join(os.path.dirname(__file__),"static{0}fonts{0}{1}.TTF".format(os.sep,font_name),)
            pass
        else:  # Windows 系统
            myfonts = {
                "1": "AdobeGothicStd-Bold.otf",
                "2": "cambriaz.ttf",
                "3": "BASKVILL.TTF"
            }
            return myfonts["{}".format(random.randint(1, 3))]
        return font_file

# 生成图片
def create_img():
    # 创建图片
    height = 160  # px
    weight = 300
    image = Image.new("RGB", (weight, height), (192, 192, 192))
    image_name = "{}.jpeg".format("logo")
    image_doc = os.path.join(os.path.dirname(__file__), "static{0}userlogo".format(os.sep))
    if not os.path.exists(image_doc):
        os.mkdir(image_doc)
    # 图片路径属于对象
    image_path = os.path.join(image_doc, image_name)
    print(str(image_path))
    image.save(image_path, format="jpeg")
    image.show()
if __name__ == '__main__':
    c = Verify_Code()
    print(c.random_chr(), c.random_disturb_chr())
    c.create_verification_code()