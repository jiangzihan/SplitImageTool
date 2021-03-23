import os


def create_dir(save_path):
    if not os.path.isdir(save_path):
        os.mkdir(save_path, mode=0o766)