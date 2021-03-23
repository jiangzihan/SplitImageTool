import os
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import cv2

from units import create_dir


class SIT:

    def __init__(self, src_path, save_path):
        self.logger = logging.getLogger(__name__)
        self.sn = 0
        self.src_path = src_path
        self.save_path = save_path

        self.ALL_IMGS = []
        self.lock = Lock()


    def start(self):
        executor = ThreadPoolExecutor(8)
        self._find_files()

        for f in self.ALL_IMGS:
            future = executor.submit(self.openimg, self.src_path, f)
        
        executor.shutdown(wait=True)
        self.logger.info("完成处理, 处理数量: %s", len(self.ALL_IMGS))


    def openimg(self, src_path, filename):
        img = self._openimg(src_path, filename)
        self._split(filename, img)

    # 读取所有图片
    def _find_files(self):
        self.ALL_IMGS = os.listdir(self.src_path)
        self.logger.info("所有图片数量:%s", len(self.ALL_IMGS))

    # 从所有图片中逐个打开图像，返回图像矩阵
    def _openimg(self, path, filename):
        with self.lock:
            self.sn += 1
        
        self.logger.info("读取图像完成: sn: %s", self.sn)

        fullpath = f"{path}/{filename}"
        img = cv2.imread(fullpath, cv2.IMREAD_COLOR)
        img_shape = img.shape
        self.logger.info("图像高度: %spx", img_shape[0])
        return img


    # 裁切图片，默认10000行，并保存分割图像
    def _split(self, filename, img, h=10000):
        img_max_height = img.shape[0]
        d, m = divmod(img_max_height, h)
        n = 1 if m > 0 else 0
        self.logger.debug("裁切%s张,剩余%spx", d, m)
        for sub_sn in range(d+n):
            s = sub_sn * h
            e = (sub_sn+1) * h
            self.logger.debug("sn: %s, s: %s ,e: %s.", sub_sn, s, e)
            self._saveimg(sub_sn, filename, img[s:e])


    def _saveimg(self, sub_sn, filename, simg):
        create_dir(self.save_path)
        dest_path = f"{self.save_path}/{os.path.splitext(filename)[0]}_{sub_sn}.jpg"
        self.logger.debug("保存文件路径: %s", dest_path)
        cv2.imwrite(dest_path, simg, [cv2.IMWRITE_JPEG_QUALITY,90])



if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    sit = SIT("/home/fido/Downloads/20210323_工厂images", "/media/ext4_data/work/20210323_工厂切割图")
    # img = sit._openimg("/media/ext4_data/work/工厂图", "202012101231_0_4887.tif")
    # sit._split("202012101231_0_4887.tif", img)
    # sit._find_files()

    sit.start()
    
