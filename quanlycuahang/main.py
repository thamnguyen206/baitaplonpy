import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

from sanpham import giao_dien_sanpham
from khachhang import giao_dien_khachhang
from doanhthu import giao_dien_doanhthu
from hoadon import giao_dien_hoadon   # 👈 THÊM

# ================= ROOT =================
root = tk.Tk()
root.title("Quản lý cửa hàng")
root.geometry("1100x650")
root.configure(bg="#ecf0f1")

# ================= STYLE =================
BG_MENU = "#2c3e50"
BTN_COLOR = "#34495e"
BTN_HOVER = "#1abc9c"

# ================= MENU =================
frame_menu = tk.Frame(root, bg=BG_MENU, height=50)
frame_menu.pack(fill="x")

# ================= CONTENT =================
frame_content = tk.Frame(root, bg="#ecf0f1")
frame_content.pack(fill="both", expand=True)

# ================= CLEAR =================
def clear_frame():
    for w in frame_content.winfo_children():
        w.destroy()

# ================= HOVER =================
def hover(btn):
    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_COLOR))

# ================= TRANG CHỦ =================
def trangchu():
    clear_frame()

    main = tk.Frame(frame_content, bg="#ecf0f1")
    main.pack(fill="both", expand=True, padx=30, pady=20)

    tk.Label(main, text="Thông tin cá nhân",
             font=("Arial", 20, "bold"),
             bg="#ecf0f1").pack(anchor="w")

    content = tk.Frame(main, bg="#ecf0f1")
    content.pack(fill="both", expand=True)

    # ===== AVATAR =====
    left = tk.Frame(content, bg="#ecf0f1")
    left.pack(side="left", padx=40)

    avatar_label = tk.Label(left, bg="#ecf0f1")
    avatar_label.pack()

    def make_circle(img):
        size = (150, 150)
        img = img.resize(size)

        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        result = Image.new('RGBA', size)
        result.paste(img, (0, 0), mask)
        return result

    def chon_anh():
        path = filedialog.askopenfilename(
            filetypes=[("Image", "*.png *.jpg *.jpeg")]
        )
        if path:
            img = Image.open(path)
            img = make_circle(img)
            img = ImageTk.PhotoImage(img)

            avatar_label.config(image=img)
            avatar_label.image = img

    tk.Button(left, text="📷 Thêm hình ảnh",
              command=chon_anh,
              bg=BTN_COLOR, fg="white").pack(pady=10)

    # ===== INFO =====
    right = tk.Frame(content, bg="#ecf0f1")
    right.pack(side="left", padx=50)

    def row(label, r):
        tk.Label(right, text=label, bg="#ecf0f1").grid(row=r, column=0, sticky="w")
        e = tk.Entry(right, width=30)
        e.grid(row=r, column=1, pady=5)
        return e

    row("Tên", 0)
    row("Email", 1)
    row("SĐT", 2)
    row("Địa chỉ", 3)

    tk.Button(main, text="Lưu thông tin",
              bg="#27ae60", fg="white",
              font=("Arial", 12)).pack(pady=20)

# ================= MENU FUNCTIONS =================
def sanpham():
    giao_dien_sanpham(frame_content)

def khachhang():
    giao_dien_khachhang(frame_content)

def hoadon():
    giao_dien_hoadon(frame_content)   # 👈 GỌI FILE HOADON

def doanhthu():
    giao_dien_doanhthu(frame_content)

# ================= BUTTON MENU =================
buttons = [
    ("Trang chủ", trangchu),
    ("Sản phẩm", sanpham),
    ("Khách hàng", khachhang),
    ("Hóa đơn", hoadon),
    ("Doanh thu", doanhthu)
]

for i, (text, cmd) in enumerate(buttons):
    btn = tk.Button(frame_menu, text=text,
                    bg=BTN_COLOR, fg="white",
                    font=("Arial", 11),
                    command=cmd)
    btn.grid(row=0, column=i, sticky="nsew", padx=2, pady=5)
    hover(btn)
    frame_menu.columnconfigure(i, weight=1)

# ================= RUN =================
trangchu()
root.mainloop()