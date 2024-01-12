import os
import concurrent.futures
import imageio
from PIL import Image

# 设置生成的视频文件名和路径
filename = "output.mp4"
filepath = os.path.join(os.getcwd(), filename)


def process_image(file_name):
    if file_name.endswith(".jpg"):
        image = Image.open(file_name)
    return image.convert("RGB")


with concurrent.futures.ThreadPoolExecutor() as executor:
    # 寻找所有 png 文件
    image_files = [file for file in os.listdir() if file.endswith(".jpg")]

    # 利用线程池并行处理图像
    images = list(executor.map(process_image, image_files))


# 将图片转换为视频文件
fps = 30  # 每秒钟30帧
with imageio.get_writer(filepath, fps=fps) as video:
    for image in images:
        video.append_data(image)
