import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def giao_dien_khachhang(frame):

    for w in frame.winfo_children():
        w.destroy()

    tk.Label(frame, text="KHÁCH HÀNG", font=("Arial", 16)).pack()

    form = tk.Frame(frame)
    form.pack()

    labels = ["Tài khoản", "Tên", "SĐT", "Địa chỉ", "SL mua", "Tổng tiền"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(form, text=text).grid(row=i, column=0)
        e = tk.Entry(form)
        e.grid(row=i, column=1)
        entries.append(e)

    tree = ttk.Treeview(frame)
    tree["columns"] = ("tk", "ten", "sdt", "dc", "sl", "tong")

    tree.heading("#0", text="ID")
    tree.heading("tk", text="TK")
    tree.heading("ten", text="Tên")
    tree.heading("sdt", text="SĐT")
    tree.heading("dc", text="Địa chỉ")
    tree.heading("sl", text="SL")
    tree.heading("tong", text="Tổng")

    tree.pack(fill="both", expand=True)

    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()

    # ================= LOAD =================
    def load():
        tree.delete(*tree.get_children())
        for row in cursor.execute("SELECT * FROM khachhang"):
            tree.insert("", "end", text=row[0], values=row[1:])

    # ================= THÊM =================
    def them():
        data = [e.get() for e in entries]

        cursor.execute(
            "INSERT INTO khachhang(taikhoan,ten,sdt,diachi,soluongmua,tongtien) VALUES(?,?,?,?,?,?)",
            data
        )
        conn.commit()
        load()

    # ================= CLICK TREE -> ĐỔ DỮ LIỆU =================
    def chon(event):
        item = tree.selection()
        if item:
            values = tree.item(item)["values"]
            for i in range(len(entries)):
                entries[i].delete(0, tk.END)
                entries[i].insert(0, values[i])

    tree.bind("<<TreeviewSelect>>", chon)

    # ================= SỬA =================
    def sua():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Lỗi", "Chọn khách hàng để sửa!")
            return

        id = tree.item(item)["text"]
        data = [e.get() for e in entries]

        cursor.execute(
            """UPDATE khachhang 
               SET taikhoan=?, ten=?, sdt=?, diachi=?, soluongmua=?, tongtien=? 
               WHERE id=?""",
            data + [id]
        )
        conn.commit()
        load()

    # ================= XOÁ =================
    def xoa():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Lỗi", "Chọn khách hàng để xoá!")
            return

        id = tree.item(item)["text"]

        cursor.execute("DELETE FROM khachhang WHERE id=?", (id,))
        conn.commit()
        load()

    # ================= BUTTON =================
    tk.Button(form, text="Thêm", command=them).grid(row=7, column=0)
    tk.Button(form, text="Sửa", command=sua).grid(row=7, column=1)
    tk.Button(form, text="Xoá", command=xoa).grid(row=7, column=2)

    load()