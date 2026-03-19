import tkinter as tk
from tkinter import ttk

from datetime import datetime
import pyodbc

conn_str = """
Driver={ODBC Driver 17 for SQL Server};
Server=LAPTOP-12OGD3V1;
Database=ShopQuanAo;
Trusted_Connection=yes;
"""

def giao_dien_doanhthu(frame):

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame, text="DOANH THU THEO THÁNG",
             font=("Arial", 20, "bold"),
             bg="#ecf0f1").pack(pady=10)

    main = tk.Frame(frame, bg="#ecf0f1")
    main.pack(fill="both", expand=True, padx=20)

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

    tree.tag_configure("even", background="#ecf0f1")
    tree.tag_configure("odd", background="#d5dbdb")

    # ===== LOAD =====
    def load():
        tree.delete(*tree.get_children())

        thang = thang_cb.get()
        if not thang:
            return

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        tong = 0

        query = """
            SELECT TenKhach, TongTien, Ngay
            FROM HoaDonPy
            WHERE MONTH(Ngay) = ?
        """

        for i, row in enumerate(cursor.execute(query, int(thang))):
            tag = "even" if i % 2 == 0 else "odd"

            tree.insert("", "end", values=row, tags=(tag,))
            tong += row[1]

        tong_label.config(text=f"{tong:,} VND")

        conn.close()

    tk.Button(top, text="Xem",
              bg="#3498db", fg="white",
              command=load).pack(side="left", padx=10)
