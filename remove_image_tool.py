import os
import logging

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

	def start(self):
		create_dir(self.save_path)

	def _find_used_img(self):
		...


if __name__=="__main__":
	result_path = "/media/white/disk5/train_sample_20201222/工厂切割图/A_result"
	ori_path = "/media/white/disk5/train_sample_20201222/工厂切割图/A_fido"
	save_path = "/media/white/disk5/train_sample_20201222/工厂切割图/A_save"

	rit = RIT(result_path, ori_path, save_path)
	rit.start()