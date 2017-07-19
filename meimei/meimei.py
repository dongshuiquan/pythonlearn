#coding=utf-8

import sys
import os
import _io
from collections import namedtuple
from PIL import Image

class Nude(object):
    def __init__(self, path_or_image):
        if isinstance(path_or_image, Image.Image):
            self.image = path_or_image
        elif isinstance(path_or_image, str):
            self.image = Image.open(path_or_image)

        #获取图片所有颜色通道
        bands = self.image.getbands()
        if len(bands) == 1:
            new_img = Image.new('RGB', self.image.size)
            new_img.paste(self.image)
            f = self.image.filename
            self.image = new_img
            self.image.filename = f

        self.skin_map = []
        self.detected_regions = []
        self.merge_region = []
        self.skin_regions = []
        self.last_from, self.last_to = -1, -1
        self.result = None
        self.message = None
        self.width, self.height = self.image.size
        self.total_pixels = self.width * self.height

    def resize(self, maxwidth = 1000, maxheight = 1000):
        """
        基于最大宽高按比例重设图片大小，
        注意： 这可能影响检测算法的结果

        如果没有变化 返回0
        原宽度大于 maxwidth 返回1
        原高度大于 maxheight 返回2
        原宽高大于 maxwidth, maxheight 返回3

        maxwidht -图片最大宽度
        maxheight - 图片最大高度
        传递参数时都设置为 False 来忽略
        """
        #返回值
        ret = 0
        if maxwidth:
            if self.width > maxwidth:
                wpercent = maxwidth / self.width
                hsize = (int)(self.width * wpercent)
                fname = self.image.filename
                self.image = self.image.resize((maxwidth, hsize), Image.LANCZOS)
                self.image.filename = fname
                self.width, self.height = self.image.size
                self.total_pixels = self.width * self.height
                ret += 1
        if maxheight:
            if self.height > maxheight:
                hpercent = ( maxheight / float(self.height))
                wsize = int((float(self.width) * float(hpercent)))
                fname = self.image.filename
                self.image = self.image.resize((wsize, maxheight), Image.LANCZOS)
                self.image.filename = fname
                self.width, self.height = self.image.size
                self.total_pixels = self.width * self.height
                ret += 2
        return ret

    #分析函数
    def parse(self):
        #如果有结果，返回本对象
        if self.result is not None:
            return self
        pixels = self.image.load()
        #遍历图片所有像素数据
        for y in range(self.height):
            for x in range(self.width):
                #得到像素的 RGB 三个通道的值
                #[x ,y] 是[(x, y)]的简便写法
                r = pixels[x, y][0] #red
                g = pixels[x, y][1]
                b = pixels[x, y][2]
                #判断当前像素是否为肤色像素
                isSkin = True if self._classfify_skin(r, g, b) else False
                _id = x + y * self.width + 1
                self.skin_map.append(self.Skin(_id, isSkin, None, x, y))
                if not isSkin:
                    continue

                

        
