import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO taikhoan(username,password) VALUES(?,?)",
               ("admin", "123"))

conn.commit()
conn.close()

print("Đã tạo tài khoản")