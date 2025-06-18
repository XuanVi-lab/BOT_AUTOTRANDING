from db_config import get_connection

industry_map = {
    "OILGAS": "Dầu khí",
    "BASICRES": "Tài nguyên Cơ bản",
    "INDUS": "Hàng & Dịch vụ Công nghiệp",
    "FOOD": "Thực phẩm và Đồ uống",
    "HEALTH": "Y tế",
    "MEDIA": "Truyền thông",
    "TELECOM": "Viễn thông",
    "BANK": "Ngân hàng",
    "REAL": "Bất động sản",
    "TECH": "Công nghệ Thông tin",
    "CHEM": "Hóa chất",
    "MATCON": "Xây dựng và Vật liệu",
    "AUTO": "Ô tô và phụ tùng",
    "PERSONAL": "Hàng cá nhân & Gia dụng",
    "RETAIL": "Bán lẻ",
    "TRAVEL": "Du lịch và Giải trí",
    "UTILITIES": "Điện, nước & xăng dầu khí đốt",
    "INSURE": "Bảo hiểm",
    "FINANCE": "Dịch vụ tài chính"
}

def insert_industries():
    conn = get_connection()
    cursor = conn.cursor()

    for code, name in industry_map.items():
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM industry WHERE industry_code = ?)
            INSERT INTO industry (industry_code, industry_name)
            VALUES (?, ?)
        """, code, code, name)

    conn.commit()
    print("✅ Đã ghi bảng ngành đầy đủ.")


# 👇 Đừng quên gọi hàm khi chạy trực tiếp:
if __name__ == "__main__":
    insert_industries()
