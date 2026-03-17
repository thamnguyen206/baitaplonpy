import sqlite3

# Kết nối database
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# ================= TÀI KHOẢN =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS taikhoan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ================= SẢN PHẨM =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS sanpham (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ten TEXT,
    gia REAL,
    soluong INTEGER,
    hinhanh TEXT
)
""")

# ================= KHÁCH HÀNG =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS khachhang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    taikhoan TEXT,
    ten TEXT,
    sdt TEXT,
    diachi TEXT,
    soluongmua INTEGER DEFAULT 0,
    tongtien REAL DEFAULT 0
)
""")

# ================= HÓA ĐƠN =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS hoadon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    khachhang_id INTEGER,
    ngay TEXT,
    tongtien REAL,
    FOREIGN KEY (khachhang_id) REFERENCES khachhang(id)
)
""")

# ================= CHI TIẾT HÓA ĐƠN =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS chitiethoadon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hoadon_id INTEGER,
    sanpham_id INTEGER,
    soluong INTEGER,
    gia REAL,
    FOREIGN KEY (hoadon_id) REFERENCES hoadon(id),
    FOREIGN KEY (sanpham_id) REFERENCES sanpham(id)
)
""")

# ================= THÊM ADMIN MẶC ĐỊNH =================
cursor.execute("SELECT * FROM taikhoan WHERE username = 'admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO taikhoan(username, password) VALUES(?, ?)",
                   ("admin", "123"))

# Lưu lại
conn.commit()
conn.close()

print("✅ Database đã tạo xong!")