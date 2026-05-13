import cv2
import os
from tkinter import Tk, filedialog, Label, Entry, Button, StringVar, IntVar, Radiobutton, messagebox
from tkinter.ttk import Progressbar
import threading

# 主窗口配置
root = Tk()
root.title("序列帧生成器 V1.0")
root.geometry("500x400")
root.resizable(False, False)

# 全局变量
video_path = StringVar()
save_format = StringVar(value="png")  # 默认导出PNG（无损）
target_fps = IntVar(value=0)          # 0表示按视频原帧率导出
save_dir = StringVar()
progress_var = IntVar(value=0)
is_running = False

# 选择视频文件
def select_video():
    file = filedialog.askopenfilename(
        title="选择需要导出帧的视频",
        filetypes=[("视频文件", "*.mp4 *.mov *.avi *.mkv *.flv *.wmv"), ("所有文件", "*.*")]
    )
    if file:
        video_path.set(file)
        # 自动获取视频原信息并显示
        cap = cv2.VideoCapture(file)
        ori_fps = round(cap.get(cv2.CAP_PROP_FPS), 2)
        ori_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        ori_res = f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
        cap.release()
        info_label.config(text=f"视频信息：原帧率{ori_fps} | 总帧数{ori_frames} | 分辨率{ori_res}")

# 选择保存文件夹
def select_save_dir():
    dir_path = filedialog.askdirectory(title="选择帧图片保存文件夹")
    if dir_path:
        save_dir.set(dir_path)

# 核心：逐帧导出逻辑
def export_frames():
    global is_running
    # 参数校验
    if not video_path.get():
        messagebox.showwarning("提示", "请先选择需要导出的视频文件！")
        return
    if not save_dir.get():
        messagebox.showwarning("提示", "请先选择保存文件夹！")
        return
    if target_fps.get() < 0:
        messagebox.showwarning("提示", "帧率不能为负数！")
        return

    # 新增：自动创建与视频同名的子文件夹
    video_filename = os.path.basename(video_path.get())  # 获取带扩展名的文件名，如"test.mp4"
    video_name = os.path.splitext(video_filename)[0]  # 去掉扩展名，得到"test"
    # 拼接成完整的保存路径
    final_save_dir = os.path.join(save_dir.get(), video_name)
    # 如果文件夹不存在，就创建
    if not os.path.exists(final_save_dir):
        os.makedirs(final_save_dir)

    is_running = True
    start_btn.config(state="disabled")
    progress_var.set(0)

    # 打开视频
    cap = cv2.VideoCapture(video_path.get())
    ori_fps = cap.get(cv2.CAP_PROP_FPS)  # 视频原帧率
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 总帧数
    frame_interval = 1  # 帧间隔，默认1（逐帧）

    # 处理自定义帧率：如果设置了目标帧率，计算需要跳过的帧
    if target_fps.get() > 0 and target_fps.get() < ori_fps:
        frame_interval = int(ori_fps / target_fps.get())
        # 保证间隔为正整数，避免除零
        frame_interval = max(1, frame_interval)

    # 初始化计数
    frame_count = 0  # 视频实际帧计数
    save_count = 0   # 保存的帧计数

    try:
        while cap.isOpened() and is_running:
            ret, frame = cap.read()
            if not ret:
                break  # 视频读取完毕

            # 按间隔保存帧
            if frame_count % frame_interval == 0:
                save_count += 1
                # 图片命名：frame_0001.png （4位数字，补零，方便排序）
                img_name = f"frame_{save_count:04d}.{save_format.get()}"
                img_path = os.path.join(final_save_dir, img_name)
                # 保存图片（OpenCV默认BGR，转RGB保证画质）
                cv2.imwrite(img_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # 更新进度条
                progress = int((frame_count / total_frames) * 100)
                progress_var.set(progress)
                root.update_idletasks()  # 刷新界面

            frame_count += 1

        # 释放资源
        cap.release()
        cv2.destroyAllWindows()
        progress_var.set(100)
        messagebox.showinfo("成功", f"帧导出完成！共保存{save_count}张图片\n保存路径：{save_dir.get()}")
    except Exception as e:
        messagebox.showerror("错误", f"导出失败：{str(e)}")
        cap.release()
        cv2.destroyAllWindows()
    finally:
        is_running = False
        start_btn.config(state="normal")

# 开启线程导出（避免界面卡死）
def start_export():
    t = threading.Thread(target=export_frames)
    t.daemon = True
    t.start()

# 停止导出
def stop_export():
    global is_running
    is_running = False
    start_btn.config(state="normal")
    messagebox.showinfo("提示", "已停止导出！")

# 界面布局（可视化控件，按顺序排列）
# 1. 选择视频
Label(root, text="1. 选择待导出视频：", font=("微软雅黑", 10)).place(x=20, y=20)
Entry(root, textvariable=video_path, width=40, state="readonly").place(x=20, y=50)
Button(root, text="浏览", command=select_video, width=8).place(x=400, y=48)

# 视频信息显示
info_label = Label(root, text="视频信息：未选择视频", font=("微软雅黑", 9), fg="gray")
info_label.place(x=20, y=80)

# 2. 选择保存路径
Label(root, text="2. 选择保存文件夹：", font=("微软雅黑", 10)).place(x=20, y=110)
Entry(root, textvariable=save_dir, width=40, state="readonly").place(x=20, y=140)
Button(root, text="浏览", command=select_save_dir, width=8).place(x=400, y=138)

# 3. 选择导出格式（PNG无损/ JPG压缩）
Label(root, text="3. 选择导出图片格式：", font=("微软雅黑", 10)).place(x=20, y=170)
Radiobutton(root, text="PNG（无损，推荐）", variable=save_format, value="png").place(x=20, y=200)
Radiobutton(root, text="JPG（压缩，占用小）", variable=save_format, value="jpg").place(x=150, y=200)

# 4. 设置导出帧率
Label(root, text="4. 导出帧率（0=原视频帧率，推荐）：", font=("微软雅黑", 10)).place(x=20, y=230)
Entry(root, textvariable=target_fps, width=10).place(x=300, y=230)
Label(root, text="帧/秒（如30=每秒30帧，1=每秒1帧）", font=("微软雅黑", 8), fg="gray").place(x=20, y=260)

# 5. 进度条
Label(root, text="5. 导出进度：", font=("微软雅黑", 10)).place(x=20, y=290)
progress_bar = Progressbar (root, variable=progress_var, maximum=100)
progress_bar.place (x=20, y=320, width=400)
# 6. 操作按钮
start_btn = Button(root, text="开始导出", command=start_export, bg="#52c41a", fg="white", width=15, height=2)
start_btn.place(x=100, y=350)
stop_btn = Button(root, text="停止导出", command=stop_export, bg="#ff4d4f", fg="white", width=15, height=2)
stop_btn.place(x=280, y=350)

# 运行主窗口
if __name__ == "__main__":
    root.mainloop()