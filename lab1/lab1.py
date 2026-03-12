import csv 

from collections import Counter 

from statistics import median 

from pathlib import Path 

 

# ===================== НАЛАШТУВАННЯ ПІД ВАРІАНТ ===================== 

VARIANT = 7 

INPUT_FILE = f"variant{VARIANT:02d}.csv"      # або .txt 

DELIMITER = ","                                # для TXT може бути ";" або "\t" 

 

# Вкажи одну числову колонку і одну категоріальну: 

NUM_COL = "stock"      # наприклад: "salary", "temp", "price" 

CAT_COL = "category"       # наприклад: "category", "genre", "position" 

 

# Умова фільтрації (зміни під свій варіант) 

def filter_condition(row: dict) -> bool: 

    # приклад для ВАРІАНТУ 1: grade >= 80 

    g = to_float(row.get("stock")) 

    return g is not None and g <= 10 

 

# ===================== ДОПОМІЖНІ ФУНКЦІЇ ===================== 

def to_float(x): 

    if x is None: 

        return None 

    x = str(x).strip().replace(",", ".") 

    if x == "": 

        return None 

    try: 

        return float(x) 

    except ValueError: 

        return None 

 

def read_table(path: str, delimiter: str = ","): 

    p = Path(path) 

    if not p.exists(): 

        raise FileNotFoundError(f"Файл не знайдено: {p.resolve()}") 

 

    with open(p, "r", encoding="utf-8") as f: 

        # DictReader підходить і для CSV, і для TXT з заголовком 

        reader = csv.DictReader(f, delimiter=delimiter) 

        rows = list(reader) 

 

    # Очищення пробілів у ключах/значеннях 

    # rows example :  

    # date, type, amount, currency, account 
    # {{ date:01/01/255 , type:’bank’, amount:1, currency : ’UAH’, account : 1}, 

    # { date:01/01/255 , type:’bank’, amount:1, currency : ’UAH’, account : 2} } 

    clean_rows = [] 

    for r in rows: 

        rr = {} 

        for k, v in r.items(): 

            kk = (k or "").strip() 

            vv = (v or "").strip() 

            rr[kk] = vv 

        clean_rows.append(rr) 

    return clean_rows 

 

def missing_report(rows): 

    if not rows: 

        return {} 

    cols = list(rows[0].keys()) 

    miss = {c: 0 for c in cols}  

    for r in rows: 

        for c in cols: 

            if r.get(c, "").strip() == "": 

                miss[c] += 1 

    return miss 

 

def numeric_stats(rows, col): 

    vals = [to_float(r.get(col)) for r in rows] 

    vals = [v for v in vals if v is not None] 

    if not vals: 

        return {"count": 0, "min": None, "max": None, "mean": None, "median": None} 

    return { 

        "count": len(vals), 

        "min": min(vals), 

        "max": max(vals), 

        "mean": sum(vals) / len(vals), 

        "median": median(vals), 

    } 

 

def top_k(rows, col, k=5): 

    c = Counter() 

    for r in rows: 

        val = r.get(col, "").strip() 

        if val != "": 

            c[val] += 1 

    return c.most_common(k) 

 

def write_csv(path, rows, delimiter=","): 

    if not rows: 

        # створимо порожній файл з повідомленням 

        Path(path).write_text("", encoding="utf-8") 

        return 

    cols = list(rows[0].keys()) 

    with open(path, "w", encoding="utf-8", newline="") as f: 

        w = csv.DictWriter(f, fieldnames=cols, delimiter=delimiter) 

        w.writeheader() 

        w.writerows(rows) 

 

def write_report(path, text): 

    Path(path).write_text(text, encoding="utf-8") 

 

# ===================== ОСНОВНА ПРОГРАМА ===================== 

def main(): 

    rows = read_table(INPUT_FILE, delimiter=DELIMITER) 

 

    cols = list(rows[0].keys()) if rows else [] 

    miss = missing_report(rows) 

 

    filtered = [r for r in rows if filter_condition(r)] 

 

    stats = numeric_stats(filtered, NUM_COL) 

    top = top_k(filtered, CAT_COL, k=5) 

 

    out_csv = f"result_variant{VARIANT:02d}.csv" 

    out_txt = f"report_variant{VARIANT:02d}.txt" 

 

    write_csv(out_csv, filtered, delimiter=DELIMITER) 

 

    report_lines = [] 

    report_lines.append(f"Лабораторна робота №1 — Звіт (Варіант {VARIANT})") 

    report_lines.append(f"Вхідний файл: {INPUT_FILE}") 

    report_lines.append(f"Кількість записів (всього): {len(rows)}") 

    report_lines.append(f"Кількість записів (після фільтра): {len(filtered)}") 

    report_lines.append("") 

    report_lines.append("Колонки:") 

    report_lines.append(", ".join(cols)) 

    report_lines.append("") 

    report_lines.append("Пропуски по колонках:") 

    for c, m in miss.items(): 

        report_lines.append(f"- {c}: {m}") 

    report_lines.append("") 

    report_lines.append(f"Статистика числової колонки '{NUM_COL}' (після фільтра):") 

    report_lines.append(f"- count:  {stats['count']}") 

    report_lines.append(f"- min:    {stats['min']}") 

    report_lines.append(f"- max:    {stats['max']}") 

    report_lines.append(f"- mean:   {stats['mean']}") 

    report_lines.append(f"- median: {stats['median']}") 

    report_lines.append("") 

    report_lines.append(f"Топ-5 значень категоріальної колонки '{CAT_COL}' (після фільтра):") 

    for i, (val, cnt) in enumerate(top, 1): 

        report_lines.append(f"{i}) {val} — {cnt}") 

 

    write_report(out_txt, "\n".join(report_lines)) 

 

    print("Готово ✅") 

    print("Збережено:", out_csv, "та", out_txt) 

 

if __name__ == "__main__": 

    main() 