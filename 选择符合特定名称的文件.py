import os
import shutil
import re

# 源文件夹和目标文件夹
source_folder = "/path/to/source/folder"  # 替换为源文件夹的实际路径
destination_folder = "/path/to/destination/folder"  # 替换为目标文件夹的实际路径

# 定义要匹配的正则表达式
regex_pattern = r'.*\.txt$'  # 例如：以.txt为扩展名的文件

# 遍历源文件夹
for root, dirs, files in os.walk(source_folder):
    for filename in files:
        if re.match(regex_pattern, filename):
            source_file = os.path.join(root, filename)
            destination_file = os.path.join(destination_folder, filename)

            # 复制文件到目标文件夹
            shutil.copy(source_file, destination_file)
            print(f"复制文件: {source_file} 到 {destination_file}")