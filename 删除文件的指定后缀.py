import os

# 指定目录
directory = "D:\\BaiduNetdiskDownload\\001.黑马Java2022在线就业课V12.5版本（推荐）\\05阶段五：项目实战-瑞吉外卖\\05-瑞吉外卖-项目优化\\03-讲义\瑞吉外卖项目优化-day03\\assets"  # 替换为您的目录路径

# 指定要删除的后缀
suffix_to_remove = "【瑞客论坛 www.ruike1.com】"

# 循环遍历目录中的文件
for filename in os.listdir(directory):
    if filename.endswith(f"{suffix_to_remove}.png"):
        # 构建新文件名，去掉指定后缀部分
        new_filename = filename.replace(f"{suffix_to_remove}.png", ".png")

        # 构建完整的旧文件路径和新文件路径
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, new_filename)

        # 重命名文件
        os.rename(old_filepath, new_filepath)
        print(f"重命名文件: {old_filepath} 到 {new_filepath}")
