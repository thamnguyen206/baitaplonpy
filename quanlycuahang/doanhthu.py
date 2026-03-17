import tkinter as tk
from tkinter import ttk
import sqlite3
import random
from datetime import datetime

def giao_dien_doanhthu(frame):

    # ===== CLEAR =====
    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame, text="DOANH THU THEO THÁNG",
             font=("Arial", 20, "bold"),
             bg="#ecf0f1").pack(pady=10)

    main = tk.Frame(frame, bg="#ecf0f1")
    main.pack(fill="both", expand=True, padx=20)

    # ===== DATABASE =====
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doanhthu(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ten TEXT,
            tongtien INTEGER,
            ngay TEXT
        )
    """)

    # ===== TẠO DATA RANDOM =====
    cursor.execute("SELECT COUNT(*) FROM doanhthu")
    if cursor.fetchone()[0] == 0:
        for i in range(50):  # 50 dòng dữ liệu
            thang = random.randint(1, 12)
            ngay = f"2026-{str(thang).zfill(2)}-{random.randint(1,28)}"
            tien = random.randint(100000, 2000000)

            cursor.execute(
                "INSERT INTO doanhthu(ten, tongtien, ngay) VALUES(?,?,?)",
                (f"Khách {i}", tien, ngay)
            )

        conn.commit()

    # ===== CHỌN THÁNG =====
    top = tk.Frame(main, bg="#ecf0f1")
    top.pack(pady=10)

    tk.Label(top, text="Tháng:", bg="#ecf0f1").pack(side="left")

    thang_cb = ttk.Combobox(top, values=[str(i) for i in range(1,13)], width=5)
    thang_cb.pack(side="left", padx=5)

    # ===== TỔNG =====
    tong_label = tk.Label(main, text="0 VND",
                          font=("Arial", 30, "bold"),
                          fg="red", bg="#ecf0f1")
    tong_label.pack(pady=10)

    # ===== TABLE =====
    tree = ttk.Treeview(main,
                        columns=("ten","tien","ngay"),
                        show="headings",
                        height=10)

    tree.heading("ten", text="Tên")
    tree.heading("tien", text="Tiền")
    tree.heading("ngay", text="Ngày")

    tree.pack(fill="both", expand=True, pady=10)

    # ===== MÀU =====
    tree.tag_configure("even", background="#ecf0f1")
    tree.tag_configure("odd", background="#d5dbdb")

    # ===== LOAD =====
    def load():
        tree.delete(*tree.get_children())

        thang = thang_cb.get().zfill(2)
        if not thang:
            return

        tong = 0

        for i, row in enumerate(cursor.execute(
            "SELECT ten, tongtien, ngay FROM doanhthu WHERE strftime('%m', ngay)=?",
            (thang,)
        )):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
            tong += row[1]

        tong_label.config(text=f"{tong:,} VND")

    tk.Button(top, text="Xem",
              bg="#3498db", fg="white",
              command=load).pack(side="left", padx=10)