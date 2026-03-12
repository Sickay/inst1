import numpy as np 

from pathlib import Path 

 

# ===================== НАЛАШТУВАННЯ ПІД ВАРІАНТ ===================== 

VARIANT = 7 

SEED = 42 

 

# Розміри (зміни під свій варіант) 

N, M = 250, 12 

 

# Розподіл: "normal" або "uniform" 

DIST = "uniform"  # або "uniform" 

 

# ===================== ГЕНЕРАЦІЯ ДАНИХ ===================== 

def generate_data(n, m, dist, seed=42): 

    rng = np.random.default_rng(seed) 

    if dist == "normal": 

        X = rng.normal(loc=0.0, scale=1.0, size=(n, m)) 

    elif dist == "uniform": 

        X = rng.uniform(low=0.0, high=1.0, size=(n, m)) 

    else: 

        raise ValueError("Unknown dist. Use 'normal' or 'uniform'.") 

    return X 

 

# ===================== НОРМАЛІЗАЦІЯ / СТАНДАРТИЗАЦІЯ ===================== 

def minmax_normalize(X, eps=1e-12): 

    x_min = X.min(axis=0) 

    x_max = X.max(axis=0) 

    return (X - x_min) / (x_max - x_min + eps) 

 

def zscore_standardize(X, eps=1e-12): 

    mu = X.mean(axis=0) 

    sigma = X.std(axis=0) 

    return (X - mu) / (sigma + eps) 

 

# ===================== ОПЕРАЦІЯ ЗА ВАРІАНТОМ ===================== 

def variant_operation(variant, X): 

    # Повертай словник з результатами (щоб зручно писати звіт) 

    out = {} 

 

    if variant == 1: 

        out["row_energy"] = np.sum(X**2, axis=1) 

 

    elif variant == 2: 

        row_mean = X.mean(axis=1) 

        out["row_mean"] = row_mean 

        out["rows_above_global_mean"] = np.where(row_mean > row_mean.mean())[0] 

 

    elif variant == 3: 

        out["X_centered"] = X - X.mean(axis=0) 

 

    elif variant == 4: 

        out["X_sorted_cols"] = np.sort(X, axis=0) 

 

    elif variant == 5: 

        out["corr"] = np.corrcoef(X, rowvar=False) 

 

    elif variant == 6: 

        mu = X.mean(axis=0) 

        sd = X.std(axis=0) 

        out["mask_gt_mu_plus_2sd"] = X > (mu + 2*sd) 

 

    elif variant == 7: 

        out["row_l2"] = np.linalg.norm(X, axis=1) 

 

    elif variant == 8: 

        out["f"] = X[:, 0] * X[:, 1] - X[:, 2] 

 

    elif variant == 9: 

        out["p25"] = np.percentile(X, 25, axis=0) 

        out["p75"] = np.percentile(X, 75, axis=0) 

 

    elif variant == 10: 

        out["X_bin"] = (X > 0.5).astype(int) 

 

    elif variant == 11: 

        out["XtX"] = X.T @ X 

 

    elif variant == 12: 

        row_max = X.max(axis=1, keepdims=True) 

        out["X_rowmax_norm"] = X / (row_max + 1e-12) 

 

    elif variant == 13: 

        Xr = np.round(X, 1) 

        out["zeros_count"] = int(np.sum(Xr == 0.0)) 

 

    elif variant == 14: 

        # ковзне середнє для колонки 0, вікно 5 

        w = 5 

        c = X[:, 0] 

        kernel = np.ones(w) / w 

        out["moving_avg"] = np.convolve(c, kernel, mode="valid") 

 

    elif variant == 15: 

        out["X_clipped"] = np.clip(X, -2, 2) 

 

    elif variant == 16: 

        mu = X.mean(axis=0) 

        out["dist_to_mu"] = np.linalg.norm(X - mu, axis=1) 

 

    elif variant == 17: 

        # очікуємо M=16 і N=256 щоб reshape в 16x16 

        if X.size != 256*16: 

            out["warning"] = "Неможливо reshape у (16,16) без зміни розміру!" 

        else: 

            out["img16x16"] = X.reshape(16, 16) 

 

    elif variant == 18: 

        flat = X.ravel() 

        idx = np.argpartition(flat, -10)[-10:] 

        idx_sorted = idx[np.argsort(flat[idx])[::-1]] 

        out["top10_values"] = flat[idx_sorted] 

        out["top10_indices_flat"] = idx_sorted 

 

    elif variant == 19: 

        mu = X.mean(axis=0) 

        sd = X.std(axis=0) 

        out["cv"] = sd / (np.abs(mu) + 1e-12) 

 

    elif variant == 20: 

        d = X[:, 0] - X[:, 1] 

        out["d"] = d 

        out["d_mean"] = float(d.mean()) 

        out["d_std"] = float(d.std()) 

        out["d_min"] = float(d.min()) 

        out["d_max"] = float(d.max()) 

 

    else: 

        raise ValueError("Variant must be 1..20") 

 

    return out 

 

# ===================== ЗВІТ ===================== 

def make_report(variant, X, op_res, X_norm, X_std): 

    lines = [] 

    lines.append(f"Лабораторна робота №2 — Звіт (Варіант {variant})") 

    lines.append(f"Матриця X: shape={X.shape}, dtype={X.dtype}, ndim={X.ndim}") 

    lines.append("") 

    lines.append("Агрегати по колонках (X):") 

    lines.append(f"- mean:   {np.round(X.mean(axis=0), 4)}") 

    lines.append(f"- std:    {np.round(X.std(axis=0), 4)}") 

    lines.append(f"- median: {np.round(np.median(X, axis=0), 4)}") 

    lines.append(f"- min:    {np.round(X.min(axis=0), 4)}") 

    lines.append(f"- max:    {np.round(X.max(axis=0), 4)}") 

    lines.append("") 

    lines.append("Перевірка нормалізації / стандартизації:") 

    lines.append(f"- X_norm min~ {np.round(X_norm.min(axis=0), 4)}") 

    lines.append(f"- X_norm max~ {np.round(X_norm.max(axis=0), 4)}") 

    lines.append(f"- X_std mean~ {np.round(X_std.mean(axis=0), 4)}") 

    lines.append(f"- X_std std~  {np.round(X_std.std(axis=0), 4)}") 

    lines.append("") 

    lines.append("Результати операції варіанту (коротко):") 

 

    # короткий вивід залежно від типів результатів 

    for k, v in op_res.items(): 

        if isinstance(v, np.ndarray): 

            lines.append(f"* {k}: array shape={v.shape}, dtype={v.dtype}") 

            # покажемо перші 5 

            preview = v.ravel()[:5] 

            lines.append(f"  first5: {np.round(preview, 4)}") 

        else: 

            lines.append(f"* {k}: {v}") 

 

    return "\n".join(lines) 

 

# ===================== MAIN ===================== 

def main(): 

    X = generate_data(N, M, DIST, seed=SEED) 

 

    # 1) базова інформація 

    print("X shape:", X.shape, "dtype:", X.dtype, "ndim:", X.ndim) 

 

    # 2) агрегати 

    col_mean = X.mean(axis=0) 

    col_std = X.std(axis=0) 

    col_median = np.median(X, axis=0) 

 

    # 3) операція варіанту 

    op_res = variant_operation(VARIANT, X) 

 

    # 4) нормалізація/стандартизація 

    X_norm = minmax_normalize(X) 

    X_std = zscore_standardize(X) 

 

    # 5) збереження 

    np.save(f"X_variant{VARIANT:02d}.npy", X) 

    np.save(f"X_norm_variant{VARIANT:02d}.npy", X_norm) 

    np.save(f"X_std_variant{VARIANT:02d}.npy", X_std) 

 

    report = make_report(VARIANT, X, op_res, X_norm, X_std) 

    Path(f"report_variant{VARIANT:02d}.txt").write_text(report, encoding="utf-8") 

 

    print("Saved ✅:", 

          f"X_variant{VARIANT:02d}.npy, X_norm_variant{VARIANT:02d}.npy, X_std_variant{VARIANT:02d}.npy, report_variant{VARIANT:02d}.txt") 

 

if __name__ == "__main__": 

    main() 