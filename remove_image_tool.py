import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

from units import create_dir


class RIT:

    def __init__(self, result_path, ori_path, save_path):
        """
        @param result_path:str    结果xml保存的路径
        @param ori_path:str       原始打标的图片路径
        @param save_path:str      转移保存的目标文件夹
        """
        self.logger = logging.getLogger(__name__)
        self.result_path = result_path
        self.ori_path = ori_path
        self.save_path = save_path

        self.all_result = None


    def start(self):
        create_dir(self.save_path)
        executor = ThreadPoolExecutor(8)

        self.all_result = self._find_used_img()

        for f in self.all_result:
            future = executor.submit(self.copy_img, self.ori_path, f, self.save_path)
        
        executor.shutdown(wait=True)
        self.logger.info("完成处理, 处理数量: %s", len(os.listdir(self.save_path)))


    def _find_used_img(self):
        # 查找结果中的所有文件
        all_result = os.listdir(self.result_path)
        self.logger.debug("结果数量: %s", len(all_result))
        return all_result


    def copy_img(self, ori_path, file_name, save_path, dst_ext=".jpg"):
        filename,filext = os.path.splitext(file_name)

        src = os.path.join(ori_path, f"{filename}{dst_ext}")
        dst = os.path.join(save_path, f"{filename}{dst_ext}")

        self.logger.debug("from: %s, to: %s", src, dst)

        shutil.copyfile(src, dst)



if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)

    ori_path = "/media/white/disk5/train_sample_20201222/工厂切割图/B_ocean"
    result_path = "/media/white/disk5/train_sample_20201222/工厂切割图/B_result"
    save_path = "/media/white/disk5/train_sample_20201222/工厂切割图/B_save"

    rit = RIT(result_path, ori_path, save_path)
    rit.start()
