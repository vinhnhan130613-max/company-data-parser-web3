import re
import datetime
import unidecode

def format_title_case(text: str) -> str:
    """Viết hoa chữ cái đầu mỗi từ, chuẩn hóa TNHH và CP."""
    formatted = " ".join([w.capitalize() for w in text.split()])
    formatted = formatted.replace("Tnhh", "TNHH")
    formatted = formatted.replace("Cổ Phần", "CP")
    return formatted

def normalize_international_name(name: str) -> str:
    """Chuẩn hóa tên quốc tế theo quy tắc, không phân biệt hoa thường."""
    formatted = format_title_case(name)

    if "company limited" in name.lower():
        formatted = formatted.replace("Company Limited", "Co Ltd")
    if "joint stock company" in name.lower():
        formatted = formatted.replace("Joint Stock Company", "JSC")
        formatted = formatted.replace("JOINT STOCK COMPANY", "JSC")
    if "cổ phần" in name.lower():
        formatted = formatted.replace("Cổ Phần", "CP")

    return formatted.strip()

def normalize_address_segment(segment: str) -> str:
    """Chuẩn hóa các cụm đặc biệt trong Trường 3."""
    seg = segment.strip()
    seg = seg.replace("Khu Dân Cư", "KDC")
    seg = seg.replace("Khu Công Nghiệp", "KCN")
    seg = seg.replace("Cụm Công Nghiệp", "CCN")
    seg = seg.replace("Khu Đô Thị", "KĐT")
    return seg

def parse_raw_data(text: str) -> dict:
    result = {}

    # Trường 1
    match_name = re.search(r"(CÔNG TY[^\n]+|VĂN PHÒNG[^\n]+)", text)
    if match_name:
        raw_name = match_name.group(0).strip()
        result["Trường 1"] = format_title_case(raw_name)

    # Trường 2: lấy từ 'Tên quốc tế'
    match_international = re.search(r"Tên quốc tế\s+([^\n]+)", text)
    if match_international:
        intl_name = match_international.group(1).strip()
        result["Trường 2"] = normalize_international_name(intl_name)

    # Trường 3–6: địa chỉ thuế
    match_addr_tax = re.search(r"Địa chỉ Thuế\s+([^\n]+)", text)
    if match_addr_tax:
        addr_tax = match_addr_tax.group(1).strip()
        parts = re.split(r"(Phường\s+[^\n,]+|Xã\s+[^\n,]+)", addr_tax)
        before_area = parts[0].strip().rstrip(",")

        # Áp dụng quy tắc viết tắt cho Trường 3
        before_area = normalize_address_segment(before_area)
        result["Trường 3"] = before_area

        # Trường 4: dịch sang tiếng Anh từ Trường 3
        translated_segments = []
        for seg in before_area.split(","):
            seg = seg.strip()
            if seg.startswith("Đường"):
                translated_segments.append(unidecode.unidecode(seg.replace("Đường", "").strip()) + " St")
            elif seg.startswith("Khu phố"):
                translated_segments.append(unidecode.unidecode(seg.replace("Khu phố", "").strip()) + " Quarter")
            elif seg.startswith("Thôn"):
                translated_segments.append(unidecode.unidecode(seg.replace("Thôn", "").strip()) + " Village")
            elif seg.startswith("Ấp"):
                translated_segments.append(unidecode.unidecode(seg.replace("Ấp", "").strip()) + " Hamlet")
            else:
                translated_segments.append(unidecode.unidecode(seg))
        result["Trường 4"] = ", ".join(translated_segments)

        if len(parts) > 1:
            area = parts[1].strip().rstrip(",")
            result["Trường 5"] = area
            if area.startswith("Phường"):
                name = area.replace("Phường", "").strip()
                result["Trường 6"] = unidecode.unidecode(name) + " Ward"
            elif area.startswith("Xã"):
                name = area.replace("Xã", "").strip()
                result["Trường 6"] = unidecode.unidecode(name) + " Commune"
            else:
                result["Trường 6"] = unidecode.unidecode(area)

    # Trường 7: giữ nguyên dữ liệu gốc
    match_phone = re.search(r"Điện thoại\s+([^\n]+)", text)
    if match_phone:
        result["Trường 7"] = match_phone.group(1).strip()
    else:
        result["Trường 7"] = "N/A"

    # Trường 8–9: người đại diện
    match_rep = re.search(r"Người đại diện\s+([^\n]+)", text)
    if match_rep:
        rep_name = format_title_case(match_rep.group(1).strip())
        result["Trường 8"] = rep_name
        today = datetime.date.today()
        result["Trường 9"] = f"【{today.day}/{today.month}/{today.year}; Phone: {result.get('Trường 7','N/A')}; Checked firm: {rep_name} & address OK】"

    return result
