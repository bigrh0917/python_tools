# encoding: utf-8
import os
from hashlib import md5

def get_file_md5(filename):
    m = md5()
    with open(filename, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()

def get_file_size(filename):
    file_size = os.path.getsize(filename)
    return file_size

if __name__ == '__main__':
    print('------------------开始查找文件------------------')
    target_path = "E:\\ali\\up\\pic"
    sizedict = dict()
    md5dict = dict()
    count = 0
    for root, dirs, files in os.walk(target_path):
        for name in files:
            file_path = os.path.join(root, name)
            file_size = get_file_size(file_path)
            if file_size in sizedict:
                cur_md5 = get_file_md5(file_path)
                for path in sizedict[file_size]:
                    if path in md5dict:
                        the_md5 = md5dict[path]
                    else:
                        the_md5 = get_file_md5(path)
                        md5dict[path] = the_md5
                    if the_md5 == cur_md5:
                        try:
                            print("出现重复文件：" + file_path + " | " + path)
                            os.remove(file_path)
                            print("删除：" + file_path + "\n")
                            count += 1
                        except Exception as ex:
                            print("出错: %s" % ex)
            else:
                sizedict[file_size] = [file_path]
    if count == 0:
        print('----------------暂未发现重复文件-----------------')
    else:
        print("一共删除了 " + str(count) + " 文件")