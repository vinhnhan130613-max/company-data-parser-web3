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
    """Chuẩn hóa tên quốc tế theo quy tắc."""
    formatted = format_title_case(name)

    if "company limited" in name.lower():
        formatted = formatted.replace("Company Limited", "Co Ltd")
        formatted = formatted.replace("COMPANY LIMITED", "Co Ltd")

    if "joint stock company" in name.lower():
        formatted = formatted.replace("Joint Stock Company", "JSC")
        formatted = formatted.replace("JOINT STOCK COMPANY", "JSC")

    if "cổ phần" in name.lower():
        formatted = formatted.replace("Cổ Phần", "CP")

    # Fix lỗi Co, Ltd → Co Ltd
    formatted = formatted.replace("Co, Ltd", "Co Ltd")

    return formatted.strip()

def normalize_address_segment(segment: str) -> str:
    """Chuẩn hóa các cụm đặc biệt trong Trường 3."""
    seg = segment.strip()
    seg = seg.replace("Khu Dân Cư", "KDC")
    seg = seg.replace("Khu Công Nghiệp", "KCN")
    seg = seg.replace("Cụm Công Nghiệp", "CCN")
    seg = seg.replace("Khu Đô Thị", "KĐT")
    return seg

def translate_address_segment(segment: str) -> str:
    """Dịch từng đoạn địa chỉ sang tiếng Anh, bỏ dấu, thêm hậu tố nếu có."""
    seg = segment.strip()

    # Quy tắc cho Tổ/TDP/Tổ Dân Phố
    if "Tổ Dân Phố" in seg or "TDP" in seg or seg.startswith("Tổ"):
        parts = seg.split()
        for word in parts:
            if word.isdigit():
                return "Group " + word
        name = unidecode.unidecode(" ".join(parts[1:])).strip()
        return name + " Group"

    if "Đường" in seg:
        return unidecode.unidecode(seg.replace("Đường", "").strip()) + " St"
    elif "Khu phố" in seg:
        return unidecode.unidecode(seg.replace("Khu phố", "").strip()) + " Quarter"
    elif "Thôn" in seg:
        return unidecode.unidecode(seg.replace("Thôn", "").strip()) + " Village"
    elif "Ấp" in seg:
        return unidecode.unidecode(seg.replace("Ấp", "").strip()) + " Hamlet"
    else:
        return unidecode.unidecode(seg)

def build_field4(field3: str) -> str:
    """Xây dựng Trường 4 từ Trường 3 bằng cách dịch từng đoạn."""
    translated_segments = []
    for seg in field3.split(","):
        translated_segments.append(translate_address_segment(seg))
    return ", ".join(translated_segments)

def title_case_address(text: str) -> str:
    """Viết hoa chữ cái đầu mỗi từ trong địa chỉ."""
    return " ".join([w.capitalize() for w in text.split()])

def parse_raw_data(text: str) -> dict:
    result = {}

    # Trường 1
    match_name = re.search(r"(CÔNG TY[^\n]+|VĂN PHÒNG[^\n]+)", text)
    if match_name:
        raw_name = match_name.group(0).strip()
        result["Trường 1"] = format_title_case(raw_name)

    # Trường 2
    match_international = re.search(r"Tên quốc tế\s+([^\n]+)", text)
    if match_international:
        intl_name = match_international.group(1).strip()
        result["Trường 2"] = normalize_international_name(intl_name)

    # Trường 3–6
    match_addr_tax = re.search(r"Địa chỉ Thuế\s+([^\n]+)", text)
    if match_addr_tax:
        addr_tax = match_addr_tax.group(1).strip()
        parts = re.split(r"(Phường\s+[^\n,]+|Xã\s+[^\n,]+)", addr_tax)
        before_area = parts[0].strip().rstrip(",")

        before_area = normalize_address_segment(before_area)
        result["Trường 3"] = title_case_address(before_area)

        field4 = build_field4(before_area)
        result["Trường 4"] = title_case_address(field4)

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

    # Trường 7
    match_phone = re.search(r"Điện thoại\s+([^\n]+)", text)
    if match_phone:
        result["Trường 7"] = match_phone.group(1).strip()
    else:
        result["Trường 7"] = "N/A"

    # Trường 8–9
    match_rep = re.search(r"Người đại diện\s+([^\n]+)", text)
    if match_rep:
        rep_name = format_title_case(match_rep.group(1).strip())
        result["Trường 8"] = rep_name
        today = datetime.date.today()
        result["Trường 9"] = f"【{today.day}/{today.month}/{today.year}; Phone: {result.get('Trường 7','N/A')}; Checked firm: {rep_name} & address OK】"

    return result
