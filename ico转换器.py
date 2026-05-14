"""
图片转 ICO 图标工具 — 可视化界面
直接运行: python ico转换器.py
命令行模式: python ico转换器.py input.png -s 64
"""

import argparse
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Optional, Tuple

try:
    from PIL import Image, ImageTk
except ImportError:
    print("错误：需要安装 Pillow 库，请运行: pip install Pillow")
    sys.exit(1)

DEFAULT_SIZES = (256, 128, 96, 64, 48, 40, 32, 24, 20, 16)
SUPPORTED_INPUT = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".tiff", ".tif")


# ────────────────────────── 核心转换逻辑 ──────────────────────────

def image_to_ico(
    input_path: str,
    output_path: Optional[str] = None,
    sizes: Optional[Tuple[int, ...]] = None,
) -> Path:

    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"找不到文件: {input_path}")

    if output_path is None:
        output_path = src.with_suffix(".ico")
    else:
        output_path = Path(output_path)

    if sizes is None:
        sizes = DEFAULT_SIZES

    img = Image.open(src).convert("RGBA")
    max_edge = max(img.size)
    sizes = tuple(s for s in sizes if s <= max_edge)
    if not sizes:
        sizes = (max_edge,)

    icon_images = []
    for size in sizes:
        icon_images.append(img.resize((size, size), Image.LANCZOS))

    icon_images[0].save(
        output_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=icon_images[1:],
    )
    return output_path


# ────────────────────────── 可视化界面 ──────────────────────────

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("图片转 ICO 图标工具")
        root.resizable(False, False)
        root.configure(bg="#f5f5f5")

        self.source_image: Optional[Image.Image] = None
        self.input_path: str = ""
        self.preview_tk: Optional[ImageTk.PhotoImage] = None

        self._build_ui()

    # ─── 布局 ────────────────────────────────────────────────

    def _build_ui(self):
        main = tk.Frame(self.root, bg="#f5f5f5", padx=24, pady=20)
        main.pack()

        # 标题
        tk.Label(
            main, text="🖼 图片转 ICO 图标",
            font=("Microsoft YaHei", 16, "bold"),
            bg="#f5f5f5", fg="#333",
        ).grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # ── 左侧：图片 ──────────────────────────────────────

        left = tk.LabelFrame(main, text="原始图片", font=("Microsoft YaHei", 10), bg="#f5f5f5")
        left.grid(row=1, column=0, padx=(0, 12), sticky="n")

        self.img_label = tk.Label(left, text="未选择图片", bg="#e0e0e0",
                                  width=28, height=14, font=("Microsoft YaHei", 9))
        self.img_label.pack(padx=12, pady=12)

        tk.Button(
            left, text="选择图片", command=self._pick_input, width=16,
            font=("Microsoft YaHei", 10), bg="#4a90d9", fg="white",
            activebackground="#357abd",
        ).pack(pady=(0, 10))

        self.lbl_info = tk.Label(left, text="", bg="#f5f5f5", font=("Microsoft YaHei", 8))
        self.lbl_info.pack(pady=(0, 8))

        # ── 中间：预览 ──────────────────────────────────────

        mid = tk.LabelFrame(main, text="ICO 预览 (最大 256×256)", font=("Microsoft YaHei", 10), bg="#f5f5f5")
        mid.grid(row=1, column=1, padx=(0, 12), sticky="n")

        self.preview_container = tk.Frame(mid, bg="#e0e0e0", width=260, height=260)
        self.preview_container.pack(padx=12, pady=12)
        self.preview_container.pack_propagate(False)

        self.preview_label = tk.Label(self.preview_container, bg="#e0e0e0")
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(mid, text="将生成多个尺寸，Windows 自动适配", font=("Microsoft YaHei", 8),
                 bg="#f5f5f5", fg="#888").pack(pady=(0, 10))

        # ── 右侧：设置 ──────────────────────────────────────

        right = tk.LabelFrame(main, text="输出设置", font=("Microsoft YaHei", 10), bg="#f5f5f5")
        right.grid(row=1, column=2, sticky="n")

        pad = {"bg": "#f5f5f5"}

        # 输出路径
        tk.Label(right, text="输出路径", font=("Microsoft YaHei", 9), **pad).pack(anchor="w", padx=10, pady=(10, 2))
        path_frame = tk.Frame(right, **pad)
        path_frame.pack(fill="x", padx=10)
        self.entry_output = tk.Entry(path_frame, font=("Consolas", 9), width=24)
        self.entry_output.pack(side="left")
        tk.Button(path_frame, text="...", command=self._pick_output,
                  width=3, font=("Microsoft YaHei", 9)).pack(side="left", padx=(4, 0))

        # 尺寸选择
        tk.Label(right, text="图标尺寸", font=("Microsoft YaHei", 9), **pad).pack(
            anchor="w", padx=10, pady=(14, 2))

        size_frame = tk.Frame(right, **pad)
        size_frame.pack(fill="x", padx=10)

        self.size_vars: dict[int, tk.BooleanVar] = {}
        self._build_size_checkboxes(size_frame)

        # 快捷选择按钮
        quick_frame = tk.Frame(right, **pad)
        quick_frame.pack(fill="x", padx=10, pady=(6, 2))
        tk.Button(quick_frame, text="全选", command=lambda: self._toggle_all(True),
                  font=("Microsoft YaHei", 8)).pack(side="left", padx=(0, 4))
        tk.Button(quick_frame, text="全不选", command=lambda: self._toggle_all(False),
                  font=("Microsoft YaHei", 8)).pack(side="left")

        # 自动打开目录
        self.var_open_dir = tk.BooleanVar(value=True)
        tk.Checkbutton(
            right, text="转换后打开文件位置",
            variable=self.var_open_dir, bg="#f5f5f5",
            font=("Microsoft YaHei", 9),
            activebackground="#f5f5f5",
        ).pack(anchor="w", padx=10, pady=(8, 0))

        # 转换按钮
        self.btn_convert = tk.Button(
            right, text="开始转换", command=self._convert,
            font=("Microsoft YaHei", 11, "bold"),
            bg="#27ae60", fg="white", activebackground="#1e8449",
            width=20, height=2, state="disabled",
        )
        self.btn_convert.pack(pady=(8, 14), padx=10)

        # 底部状态
        self.status_bar = tk.Label(self.root, text="请选择一张图片", relief="sunken",
                                   anchor="w", font=("Microsoft YaHei", 9), bg="#fff")
        self.status_bar.pack(fill="x", side="bottom")

    def _build_size_checkboxes(self, parent: tk.Frame):
        """排列尺寸复选框: 2 列"""
        # 预设尺寸
        row_offset = 0
        for i, s in enumerate(DEFAULT_SIZES):
            var = tk.BooleanVar(value=False)
            self.size_vars[s] = var
            cb = tk.Checkbutton(
                parent, text=f"{s}×{s}",
                variable=var, bg="#f5f5f5",
                font=("Microsoft YaHei", 9),
                activebackground="#f5f5f5",
            )
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=4, pady=2)
        row_offset = (len(DEFAULT_SIZES) + 1) // 2

        # 分隔线
        sep = ttk.Separator(parent, orient="horizontal")
        sep.grid(row=row_offset, column=0, columnspan=2, sticky="ew", pady=(8, 4))

        # 原图尺寸选项
        row_offset += 1
        self.var_original = tk.BooleanVar(value=False)
        self.cb_original = tk.Checkbutton(
            parent, text="原图尺寸",
            variable=self.var_original, bg="#f5f5f5",
            font=("Microsoft YaHei", 9, "bold"),
            activebackground="#f5f5f5",
            state="disabled",
        )
        self.cb_original.grid(row=row_offset, column=0, columnspan=2, sticky="w", padx=4, pady=2)

    # ─── 交互逻辑 ────────────────────────────────────────────

    def _pick_input(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif *.webp *.tiff *.tif")],
        )
        if path:
            self._load_image(path)

    def _pick_output(self):
        path = filedialog.asksaveasfilename(
            title="保存 ICO",
            defaultextension=".ico",
            filetypes=[("ICO 图标", "*.ico")],
        )
        if path:
            self.entry_output.delete(0, "end")
            self.entry_output.insert(0, path)

    def _toggle_all(self, check: bool):
        for var in self.size_vars.values():
            var.set(check)
        if self.source_image is not None:
            self.var_original.set(check)

    def _load_image(self, path: str):
        try:
            self.source_image = Image.open(path)
            self.input_path = path
            w, h = self.source_image.size
            self.lbl_info.config(text=f"{os.path.basename(path)}\n{w}×{h} px")

            # 更新原图尺寸选项
            orig_size = max(w, h)
            self.cb_original.config(
                text=f"原图尺寸 ({orig_size}×{orig_size})",
                state="normal",
            )
            self.var_original.set(True)
            self._original_size = orig_size

            # 缩放到预览区域
            preview_w, preview_h = 252, 200
            ratio = min(preview_w / w, preview_h / h, 1)
            display_img = self.source_image.resize(
                (int(w * ratio), int(h * ratio)), Image.LANCZOS
            )
            self.preview_tk = ImageTk.PhotoImage(display_img)
            self.img_label.config(image=self.preview_tk, text="")

            # 更新 ICO 预览
            self._update_ico_preview()

            # 默认输出路径
            if not self.entry_output.get():
                out = str(Path(path).with_suffix(".ico"))
                self.entry_output.delete(0, "end")
                self.entry_output.insert(0, out)

            self.btn_convert.config(state="normal")
            self._status("图片已加载，点击「开始转换」")

        except Exception as e:
            messagebox.showerror("打开失败", str(e))

    def _update_ico_preview(self):
        """以最大预览尺寸显示 ICO 效果"""
        if self.source_image is None:
            return
        preview_size = 256
        img = self.source_image.resize(
            (preview_size, preview_size), Image.LANCZOS
        )
        self.ico_preview_tk = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.ico_preview_tk)

    def _convert(self):
        if self.source_image is None or not self.input_path:
            return

        # 收集选中的尺寸
        sizes = tuple(s for s, var in self.size_vars.items() if var.get())
        if self.var_original.get() and hasattr(self, "_original_size"):
            sizes = sizes + (self._original_size,)
        sizes = tuple(dict.fromkeys(sizes))  # 去重保序
        if not sizes:
            messagebox.showwarning("提示", "请至少选择一个尺寸")
            return

        output = self.entry_output.get().strip()
        if not output:
            messagebox.showwarning("提示", "请指定输出路径")
            return

        self.btn_convert.config(state="disabled", text="转换中...")
        self.root.update()

        try:
            out_path = image_to_ico(
                self.input_path,
                output_path=output,
                sizes=sizes,
            )
            self._status(f"转换完成: {out_path}")
            messagebox.showinfo("完成",
                                f"已生成 {len(sizes)} 个尺寸的图标\n{out_path}")
            if self.var_open_dir.get():
                os.startfile(out_path.parent)
        except Exception as e:
            messagebox.showerror("转换失败", str(e))
            self._status("转换失败")
        finally:
            self.btn_convert.config(state="normal", text="开始转换")

    def _status(self, msg: str):
        self.status_bar.config(text=f"  {msg}")


# ────────────────────────── 入口 ──────────────────────────

def run_gui():
    root = tk.Tk()
    App(root)
    # 窗口居中
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")
    root.mainloop()


def run_cli():
    parser = argparse.ArgumentParser(description="图片转 ICO 图标工具")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("-o", "--output", help="输出路径")
    parser.add_argument("-s", "--sizes", help=f"尺寸逗号分隔 (默认: {','.join(map(str, DEFAULT_SIZES))})")
    args = parser.parse_args()

    sizes = None
    if args.sizes:
        try:
            sizes = tuple(int(x.strip()) for x in args.sizes.split(",") if x.strip())
        except ValueError:
            print("错误：尺寸必须是整数")
            sys.exit(1)

    try:
        out = image_to_ico(args.input, args.output, sizes)
        print(f"已生成: {out}")
    except Exception as e:
        print(f"转换失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] not in ("-h", "--help"):
        # 带参数 → 命令行模式
        run_cli()
    else:
        run_gui()
