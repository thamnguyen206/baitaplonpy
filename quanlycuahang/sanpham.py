import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import sqlite3

def giao_dien_sanpham(frame):

    # ===== CLEAR =====
    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame, text="QUẢN LÝ SẢN PHẨM",
             font=("Arial", 20, "bold"),
             bg="#ecf0f1").pack(pady=10)

    main = tk.Frame(frame, bg="#ecf0f1")
    main.pack(fill="both", expand=True, padx=20)

    # ===== FORM =====
    form = tk.Frame(main, bg="#ecf0f1")
    form.pack(pady=10)

    def row(label, r):
        tk.Label(form, text=label, bg="#ecf0f1").grid(row=r, column=0, padx=5, pady=5, sticky="w")
        e = tk.Entry(form, width=25)
        e.grid(row=r, column=1, pady=5)
        return e

    ten = row("Tên", 0)
    gia = row("Giá", 1)
    sl = row("Số lượng", 2)

    # ===== ẢNH =====
    img_label = tk.Label(form, bg="#ecf0f1")
    img_label.grid(row=0, column=2, rowspan=4, padx=20)

    img_path = None

    def chon_anh():
        nonlocal img_path
        path = filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg *.jpeg")])
        if path:
            img_path = path
            img = Image.open(path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)

            img_label.config(image=img)
            img_label.image = img

    tk.Button(form, text="📷 Chọn ảnh",
              bg="#2980b9", fg="white",
              command=chon_anh).grid(row=3, column=2)

    # ===== DATABASE =====
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sanpham(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten TEXT,
            gia INTEGER,
            soluong INTEGER,
            anh TEXT
        )
    """)
    conn.commit()

    # ===== TABLE =====
    tree = ttk.Treeview(main, columns=("id","ten","gia","sl"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("ten", text="Tên")
    tree.heading("gia", text="Giá")
    tree.heading("sl", text="Số lượng")

    tree.pack(fill="both", expand=True, pady=10)

    selected_id = None

    # ===== LOAD =====
    def load():
        tree.delete(*tree.get_children())
        for row in cursor.execute("SELECT id,ten,gia,soluong FROM sanpham"):
            tree.insert("", "end", values=row)

    # ===== CLICK =====
    def on_select(event):
        nonlocal selected_id, img_path

        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            data = item["values"]

            selected_id = data[0]

            ten.delete(0, tk.END)
            gia.delete(0, tk.END)
            sl.delete(0, tk.END)

            ten.insert(0, data[1])
            gia.insert(0, data[2])
            sl.insert(0, data[3])

            # load ảnh
            cursor.execute("SELECT anh FROM sanpham WHERE id=?", (selected_id,))
            result = cursor.fetchone()

            if result and result[0]:
                img_path = result[0]
                try:
                    img = Image.open(img_path)
                    img = img.resize((100, 100))
                    img = ImageTk.PhotoImage(img)

                    img_label.config(image=img)
                    img_label.image = img
                except:
                    pass

    tree.bind("<<TreeviewSelect>>", on_select)

    # ===== THÊM =====
    def them():
        cursor.execute(
            "INSERT INTO sanpham(ten,gia,soluong,anh) VALUES(?,?,?,?)",
            (ten.get(), gia.get(), sl.get(), img_path)
        )
        conn.commit()
        load()

    # ===== SỬA =====
    def sua():
        if selected_id is None:
            return

        cursor.execute("""
            UPDATE sanpham
            SET ten=?, gia=?, soluong=?, anh=?
            WHERE id=?
        """, (ten.get(), gia.get(), sl.get(), img_path, selected_id))

        conn.commit()
        load()

    # ===== XÓA =====
    def xoa():
        if selected_id is None:
            return

        cursor.execute("DELETE FROM sanpham WHERE id=?", (selected_id,))
        conn.commit()
        load()

    # ===== BUTTON =====
    btn_frame = tk.Frame(main, bg="#ecf0f1")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Thêm", bg="#27ae60", fg="white",
              width=12, command=them).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Sửa", bg="#f39c12", fg="white",
              width=12, command=sua).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Xóa", bg="red", fg="white",
              width=12, command=xoa).pack(side="left", padx=5)

    load()