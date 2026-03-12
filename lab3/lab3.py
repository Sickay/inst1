import pandas as pd 

from pathlib import Path 

 

# ===================== НАЛАШТУВАННЯ ПІД ВАРІАНТ ===================== 

VARIANT = 7

FILE_A = "warehouse.csv"
FILE_B = "suppliers.csv"

MERGE_KEY = "supplier_id"
MERGE_HOW = "left"  # "inner", "left", "right", "outer" 

 

# Фільтр (налаштовуй під варіант) 

def apply_filter(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["stock"] <= 10]

 

# Групування (налаштовуй під варіант) 
AGG_COL = "grade"  # числова колонка для агрегацій 
GROUP_COL = "supplier_id"

def group_report(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("supplier_id")
        .agg(
            sku_count=("sku","count"),
            stock_sum=("stock","sum"),
            price_mean=("price","mean")
        )
        .reset_index()
    )

 

# ===================== ЗВІТ ===================== 

def make_text_report(dfA, dfB, dfF, grp, merged) -> str: 

    lines = [] 

    lines.append(f"Лабораторна робота №3 — Звіт (Варіант {VARIANT})") 

    lines.append("") 

    lines.append("== Таблиця A ==") 

    lines.append(f"shape: {dfA.shape}") 

    lines.append(f"columns: {list(dfA.columns)}") 

    lines.append(f"dtypes:\n{dfA.dtypes}") 

    lines.append("") 

    lines.append("== Таблиця B ==") 

    lines.append(f"shape: {dfB.shape}") 

    lines.append(f"columns: {list(dfB.columns)}") 

    lines.append("") 

    lines.append("== Після фільтрації A ==") 

    lines.append(f"shape: {dfF.shape}") 

    lines.append("") 

    lines.append("== GroupBy report (перші 10 рядків) ==") 

    lines.append(grp.head(10).to_string(index=False)) 

    lines.append("") 

    lines.append("== Merge result ==") 

    lines.append(f"merge key: {MERGE_KEY}, how: {MERGE_HOW}") 

    lines.append(f"shape: {merged.shape}") 

    lines.append("") 

    return "\n".join(lines) 

 

# ===================== MAIN ===================== 

def main(): 

    # 1) читання 

    dfA = pd.read_csv(FILE_A) 

    dfB = pd.read_csv(FILE_B) 

 

    print("A:", dfA.shape, "B:", dfB.shape) 

 

    # 2) фільтрація 

    dfF = apply_filter(dfA) 

 

    # 3) groupby+agg 

    grp = group_report(dfF) 

 

    # 4) merge 

    merged = pd.merge(dfF, dfB, on=MERGE_KEY, how=MERGE_HOW) 

 

    # 5) збереження 

    dfF.to_csv(f"filtered_variant{VARIANT:02d}.csv", index=False) 

    grp.to_csv(f"group_report_variant{VARIANT:02d}.csv", index=False) 

    merged.to_csv(f"merged_variant{VARIANT:02d}.csv", index=False) 

 

    report = make_text_report(dfA, dfB, dfF, grp, merged) 

    Path(f"report_variant{VARIANT:02d}.txt").write_text(report, encoding="utf-8") 

 

    print("Saved ✅: filtered, group_report, merged, report") 

 

if __name__ == "__main__": 

    main() 