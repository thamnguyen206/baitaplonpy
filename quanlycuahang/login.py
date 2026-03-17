import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

# ===== XỬ LÝ LOGIN =====
def login():
    user = entry_user.get()
    pwd = entry_pass.get()

    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM taikhoan WHERE username=? AND password=?",
                   (user, pwd))

    if cursor.fetchone():
        messagebox.showinfo("OK", "Đăng nhập thành công")
        root.destroy()
        subprocess.run(["python", "main.py"])
    else:
        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")

# ===== HIỆN MẬT KHẨU =====
def toggle_pass():
    if show_pass.get():
        entry_pass.config(show="")
    else:
        entry_pass.config(show="*")

# ===== WINDOW =====
root = tk.Tk()
root.title("Đăng nhập")
root.geometry("600x400")
root.resizable(False, False)

# ===== ẢNH NỀN =====
bg_image = Image.open("background.jpg")  # đổi tên ảnh của bạn
bg_image = bg_image.resize((600, 400))
bg = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ===== KHUNG LOGIN =====
frame = tk.Frame(root, bg="#ffffff")
frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=250)

# ===== TITLE =====
tk.Label(frame, text="ĐĂNG NHẬP",
         font=("Arial", 14, "bold"),
         bg="#ffffff").pack(pady=10)

# ===== USER =====
tk.Label(frame, text="Tài khoản:", bg="#ffffff").pack()
entry_user = tk.Entry(frame)
entry_user.pack(pady=5)

# ===== PASS =====
tk.Label(frame, text="Mật khẩu:", bg="#ffffff").pack()
entry_pass = tk.Entry(frame, show="*")
entry_pass.pack(pady=5)

# ===== CHECKBOX =====
show_pass = tk.BooleanVar()
tk.Checkbutton(frame, text="Hiện mật khẩu",
               variable=show_pass,
               command=toggle_pass,
               bg="#ffffff").pack()

# ===== BUTTON =====
tk.Button(frame,
          text="Đăng nhập",
          bg="green",
          fg="white",
          width=15,
          command=login).pack(pady=10)

root.mainloop()