#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
'''
@author:MrSprint
@file:Verification_Code.py
@time:2016 16-12-1 上午11:38
'''
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random,math,copy

char_width=40
width=char_width*4
height=40

samples='ABCDEFGHJKLMNPRSTUVWXYabcdefghjkmnpqrtuvwxy34578'

def sampling():
    global sample
    sample=random.sample(samples,4)

def randChar():
    global sample
    return sample.pop()

def randColor():
    return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

def randColor2():
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

def regular_start_position(i):
    sign=1
    if random.randint(0,100) > 60:
        sign=-1
    start=char_width*i+random.randint(5,15)*sign
    if start-10<0:
        start=random.randint(1,5)
    elif start+char_width+10>width:
        start=width-char_width-random.randint(1,5)
    return (start,random.randint(-10,0))

def twist(img): #不会写
    src_img = img.copy()  # 将原始图像复制一个副本，这是关键。开始的时候忘记将原始像素复制出来一份，下边的代码里在原始像素里覆盖来覆盖去,总是没有满意的效果，我还以为公式写错了。
    cycle = 2.5  # sin函数2*PI一个周期，这里设置要整几个周期
    y_amp = 3  # y跟随正弦曲线变化的幅度,4就不少了。在本例中5像素以上数字会碎。
    for y in range(0, height):
        for x in range(0, char_width):
            new_y = y + round(math.sin(x * 2 * math.pi * cycle / char_width) * y_amp)
            # 三角函数是高中学的,(x/char_width*2*pi)代表(x/char_width)个周期,这样就把像素坐标(x,y)的变化与正弦曲线扯上了关系.
            if new_y < height and new_y > 0:
                img.putpixel((x, new_y), src_img.getpixel((x, y)))
    return img

def gen_bg():
    img_bg=Image.new('RGBA',(width,height),(255,255,255,255))
    draw=ImageDraw.Draw(img_bg)
    for x in range(width):
        for y in range(height):
            draw.point((x,y),fill=randColor())
    return img_bg

def rotate(img,deg_left,deg_right):
    return img.rotate(random.randint(deg_left,deg_right),expand=False)

def gen_captcha_img():
    sampling()
    text_layer=Image.new('RGBA',(width,height),(255,255,255,0)) #创建文字透明层
    draw=ImageDraw.Draw(text_layer)
    for t in range(4):#在透明层写字
        font=ImageFont.truetype('ukai.ttc',random.randint(40,48))
        draw.text((char_width*t,0),randChar(),font=font,fill=randColor2())
    img_bg=gen_bg()#创建杂色背景层
    for  t in range(4):
        box=(char_width*t,0,char_width*(t+1),height)
        region=text_layer.crop(box) #从文字层上切文字
        region=rotate(region,-30,30) #把切出的文字旋转一下
        region=twist(region)
        *drop,alpha=region.split() #取出alpha通道备用,我也不知道为什么会这样
        img_bg.paste(region,regular_start_position(t),mask=alpha) #这里不传alpha通道进来,文字切片的周围透明部分会显示成黑色

    #img_bg=img_bg.filter(ImageFilter.BLUR)
    #img_bg.show()
    img_bg.save(r'/home/sprint/桌面/captcha.jpg','jpeg')


gen_captcha_img()