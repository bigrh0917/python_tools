import os
import tkinter as tk
from tkinter import filedialog, messagebox
try:
    from PIL import Image
except ImportError:
    # 尝试安装 Pillow 库
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image
import math

class PhotoResizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("照片尺寸修改工具")
        self.geometry("500x400")
        self.resizable(False, False)
        
        # 设置DPI（每英寸点数）
        # 1英寸 = 2.54厘米
        self.dpi = 300
        
        # 创建界面元素
        self.create_widgets()
        
    def create_widgets(self):
        # 标题标签
        title_label = tk.Label(self, text="照片尺寸修改工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 创建框架
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)
        
        # 文件选择
        file_frame = tk.Frame(input_frame)
        file_frame.pack(fill="x", pady=5)
        
        file_label = tk.Label(file_frame, text="图片文件：", width=10)
        file_label.pack(side="left")
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, width=30)
        file_entry.pack(side="left", padx=5)
        
        browse_button = tk.Button(file_frame, text="浏览", command=self.browse_file)
        browse_button.pack(side="left")
        
        # 宽度输入
        width_frame = tk.Frame(input_frame)
        width_frame.pack(fill="x", pady=5)
        
        width_label = tk.Label(width_frame, text="宽度(厘米)：", width=10)
        width_label.pack(side="left")
        
        self.width_var = tk.DoubleVar(value=10.0)
        width_entry = tk.Entry(width_frame, textvariable=self.width_var, width=10)
        width_entry.pack(side="left", padx=5)
        
        # 高度输入
        height_frame = tk.Frame(input_frame)
        height_frame.pack(fill="x", pady=5)
        
        height_label = tk.Label(height_frame, text="高度(厘米)：", width=10)
        height_label.pack(side="left")
        
        self.height_var = tk.DoubleVar(value=15.0)
        height_entry = tk.Entry(height_frame, textvariable=self.height_var, width=10)
        height_entry.pack(side="left", padx=5)
        
        # 保持纵横比选项
        self.keep_ratio_var = tk.BooleanVar(value=True)
        keep_ratio_check = tk.Checkbutton(input_frame, text="保持原始纵横比", variable=self.keep_ratio_var)
        keep_ratio_check.pack(pady=5)
        
        # 图片信息显示区域
        info_frame = tk.LabelFrame(self, text="图片信息")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        self.info_text = tk.Text(info_frame, height=5, width=50)
        self.info_text.pack(padx=10, pady=10)
        self.info_text.config(state="disabled")
        
        # 按钮区域
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        resize_button = tk.Button(button_frame, text="调整尺寸", command=self.resize_image, width=15)
        resize_button.pack(side="left", padx=10)
        
        exit_button = tk.Button(button_frame, text="退出", command=self.quit, width=15)
        exit_button.pack(side="left", padx=10)
    
    def browse_file(self):
        filetypes = [
            ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("所有文件", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.file_path_var.set(file_path)
            self.show_image_info(file_path)
    
    def show_image_info(self, file_path):
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                # 计算厘米尺寸 (像素/DPI*2.54)
                width_cm = (width / self.dpi) * 2.54
                height_cm = (height / self.dpi) * 2.54
                
                self.info_text.config(state="normal")
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, f"原始尺寸: {width}x{height} 像素\n")
                self.info_text.insert(tk.END, f"原始尺寸(厘米): {width_cm:.2f}x{height_cm:.2f} 厘米\n")
                self.info_text.insert(tk.END, f"文件格式: {img.format}\n")
                self.info_text.insert(tk.END, f"颜色模式: {img.mode}")
                self.info_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取图片信息: {str(e)}")
    
    def resize_image(self):
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("错误", "请先选择一个有效的图片文件")
            return
        
        try:
            # 获取用户输入的厘米尺寸
            width_cm = self.width_var.get()
            height_cm = self.height_var.get()
            
            # 将厘米转换为像素 (厘米*DPI/2.54)
            width_px = math.ceil((width_cm * self.dpi) / 2.54)
            height_px = math.ceil((height_cm * self.dpi) / 2.54)
            
            with Image.open(file_path) as img:
                original_width, original_height = img.size
                
                # 如果选择保持纵横比
                if self.keep_ratio_var.get():
                    # 计算原始纵横比
                    ratio = original_width / original_height
                    
                    # 根据宽度计算高度
                    calculated_height_px = math.ceil(width_px / ratio)
                    
                    # 使用计算出的高度
                    height_px = calculated_height_px
                    height_cm = (height_px * 2.54) / self.dpi
                    
                    # 更新高度输入框
                    self.height_var.set(round(height_cm, 2))
                
                # 调整图片尺寸
                resized_img = img.resize((width_px, height_px), Image.LANCZOS)
                
                # 获取原始文件名和扩展名
                file_name, file_ext = os.path.splitext(file_path)
                output_path = f"{file_name}_resized{file_ext}"
                
                # 保存调整后的图片
                resized_img.save(output_path)
                
                messagebox.showinfo("成功", f"图片已调整尺寸并保存为:\n{output_path}")
                
                # 更新图片信息显示
                self.info_text.config(state="normal")
                self.info_text.insert(tk.END, f"\n\n调整后尺寸: {width_px}x{height_px} 像素")
                self.info_text.insert(tk.END, f"\n调整后尺寸(厘米): {width_cm:.2f}x{height_cm:.2f} 厘米")
                self.info_text.config(state="disabled")
                
        except Exception as e:
            messagebox.showerror("错误", f"调整图片尺寸时出错: {str(e)}")

if __name__ == "__main__":
    app = PhotoResizer()
    app.mainloop()