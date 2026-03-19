import tkinter as tk
conn_str = """
Driver={ODBC Driver 17 for SQL Server};
Server=LAPTOP-12OGD3V1;
Database=ShopQuanAo;
Trusted_Connection=yes;
"""

def giao_dien_hoadon(parent):
    # Xóa nội dung cũ
    for w in parent.winfo_children():
        w.destroy()

    main = tk.Frame(parent, bg="white")
    main.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(main, text="HÓA ĐƠN",
             font=("Arial", 20, "bold"),
             bg="white").pack(pady=10)

    # ===== FORM =====
    form = tk.Frame(main, bg="white")
    form.pack(pady=10)

    def row(label, r):
        tk.Label(form, text=label, bg="white").grid(row=r, column=0, sticky="w", padx=5, pady=5)
        e = tk.Entry(form, width=25)
        e.grid(row=r, column=1, pady=5)
        return e

    entry_ten = row("Tên khách", 0)
    entry_sdt = row("SĐT", 1)
    entry_diachi = row("Địa chỉ", 2)
    entry_sp = row("Sản phẩm", 3)
    entry_sl = row("Số lượng", 4)

    # ===== DATA =====
    danh_sach = []

    # ===== THÊM SẢN PHẨM =====
    def them():
        sp = entry_sp.get()
        sl = entry_sl.get()

        if sp == "" or sl == "":
            return

        try:
            sl = int(sl)
        except:
            return

        gia = 100  # demo giá
        thanh_tien = gia * sl

        danh_sach.append((sp, gia, sl, thanh_tien))

        cap_nhat_bang()

    tk.Button(form, text="Thêm",
              bg="#27ae60", fg="white",
              command=them).grid(row=5, columnspan=2, pady=10)

    # ===== BẢNG =====
    table = tk.Frame(main, bg="white")
    table.pack(pady=10)

    headers = ["Sản phẩm", "Giá", "Số lượng", "Thành tiền"]

    for i, h in enumerate(headers):
        tk.Label(table, text=h, width=20,
                 bg="#bdc3c7").grid(row=0, column=i)

    # ===== TỔNG TIỀN =====
    tong_label = tk.Label(main, text="Tổng tiền: 0",
                          font=("Arial", 12),
                          bg="white")
    tong_label.pack(pady=10)

    # ===== CẬP NHẬT BẢNG =====
    def cap_nhat_bang():
        # xóa dòng cũ
        for widget in table.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        tong = 0

        for i, (sp, gia, sl, tt) in enumerate(danh_sach, start=1):
            tk.Label(table, text=sp, width=20).grid(row=i, column=0)
            tk.Label(table, text=gia, width=20).grid(row=i, column=1)
            tk.Label(table, text=sl, width=20).grid(row=i, column=2)
            tk.Label(table, text=tt, width=20).grid(row=i, column=3)

            tong += tt

        tong_label.config(text=f"Tổng tiền: {tong}")

   
     # ===== XỬ LÝ NÚT =====
    def luu_hoa_don():
         import pyodbc
         from datetime import datetime

         if len(danh_sach) == 0:
            print("Chưa có sản phẩm")
            return

         ten = entry_ten.get()
         sdt = entry_sdt.get()
         diachi = entry_diachi.get()

         tong_tien = sum(tt for _, _, _, tt in danh_sach)

         conn = pyodbc.connect(conn_str)
         cursor = conn.cursor()

    # ===== Lưu hóa đơn =====
         cursor.execute("""
            INSERT INTO HoaDonPy (TenKhach, SDT, DiaChi, TongTien)
            VALUES (?, ?, ?, ?)
         """, (ten, sdt, diachi, tong_tien))

         cursor.execute("SELECT @@IDENTITY")
         ma_hd = cursor.fetchone()[0]

    # ===== Lưu chi tiết =====
         for sp, gia, sl, tt in danh_sach:
           cursor.execute("""
               INSERT INTO ChiTietHoaDonPy
               (MaHoaDon, TenSanPham, Gia, SoLuong, ThanhTien)
               VALUES (?, ?, ?, ?, ?)
             """, (ma_hd, sp, gia, sl, tt))

         conn.commit()
         conn.close()

         print("✅ Lưu thành công vào DB Python")
         
         
    def mo_thong_ke():
        print("Mở thống kê doanh thu")

        try:
            from doanhthu import giao_dien_doanh_thu
            giao_dien_doanh_thu(parent)
        except:
            print("Chưa có giao diện doanh thu")

    # ===== BUTTON =====
    tk.Button(main, text="Lưu hóa đơn",
              bg="#3498db", fg="white",
              command=luu_hoa_don).pack(pady=5)

    tk.Button(main, text="Thống kê doanh thu",
              bg="#f39c12", fg="white",
              command=mo_thong_ke).pack(pady=5)
