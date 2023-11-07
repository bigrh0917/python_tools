import os
import shutil
import re

# 源文件夹和规则-目标文件夹映射
source_folder = "/path/to/source/folder"  # 替换为源文件夹的实际路径
rules_to_destination = {
    r'.*\.txt$': "/path/to/destination_txt",  # .txt 文件匹配到这个文件夹
    r'.*\.jpg$': "/path/to/destination_jpg",  # .jpg 文件匹配到这个文件夹
    # 添加更多规则和目标文件夹
}

# 遍历源文件夹
for root, dirs, files in os.walk(source_folder):
    for filename in files:
        for rule, destination_folder in rules_to_destination.items():
            if re.match(rule, filename):
                source_file = os.path.join(root, filename)
                destination_file = os.path.join(destination_folder, filename)

                # 复制文件到目标文件夹
                shutil.copy(source_file, destination_file)
                print(f"复制文件: {source_file} 到 {destination_file}")
