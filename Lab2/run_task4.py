import pandas as pd

from experiments import (
    task4_tolerance_table,
    task4_f0_fb_table,
    task4_budget_table,
)
from plots import (
    plot_task4_nf_vs_eps,
    plot_task4_length_vs_nf,
    plot_task4_errors_vs_nf,
    plot_task4_budget,
    ensure_output_dir,
)

# Функция для красивого форматирования чисел
def format_numbers(df):
    df_formatted = df.copy()
    
    # Столбцы, где точно есть дробные числа (делаем ровно 4 знака в экспоненте)
    float_cols = ["eps_x", "length", "x_mid", "error_x", "error_f"]
    for col in float_cols:
        if col in df_formatted.columns:
            df_formatted[col] = df_formatted[col].apply(
                lambda x: f"{x:.4e}" if pd.notna(x) else x
            )
            
    # Если нужно, чтобы Nf и iters тоже были с 4 знаками после запятой 
    # (например 402.0000), раскомментируй код ниже. 
    # Но обычно их оставляют целыми. Оставлю как есть, чтобы не было каши.
    
    return df_formatted

if __name__ == "__main__":
    ensure_output_dir()

    # 1. Таблица точностей
    df_tol = task4_tolerance_table()
    df_tol_fmt = format_numbers(df_tol)
    # Сохраняем с разделителем ';' и кодировкой utf-8-sig, чтобы Excel не ругался
    df_tol_fmt.to_csv("output/task4_tolerance.csv", index=False, sep=';', encoding='utf-8-sig')
    print("Таблица сохранена: task4_tolerance.csv")

    # 2. Таблица границ (f0 и fb)
    df_edge = task4_f0_fb_table(eps_x=1e-4)
    df_edge_fmt = format_numbers(df_edge)
    df_edge_fmt.to_csv("output/task4_edge.csv", index=False, sep=';', encoding='utf-8-sig')
    print("Таблица сохранена: task4_edge.csv")

    # 3. Таблица бюджетов
    df_budget = task4_budget_table()
    df_budget_fmt = format_numbers(df_budget)
    df_budget_fmt.to_csv("output/task4_budget.csv", index=False, sep=';', encoding='utf-8-sig')
    print("Таблица сохранена: task4_budget.csv")

    # 4. Построение графиков
    funcs_for_plots = ["f3", "f5", "f6"]

    plot_task4_nf_vs_eps(df_tol, funcs_for_plots, "task4_nf_vs_eps.png",
                         title="Nf vs eps_x")
    plot_task4_length_vs_nf(df_tol, funcs_for_plots, "task4_length_vs_nf.png",
                            title="length vs Nf")
    plot_task4_errors_vs_nf(df_tol, funcs_for_plots, "task4_errors_vs_nf.png",
                            title="error_x and error_f vs Nf")
    plot_task4_budget(df_budget, "task4_budget.png",
                      title="Budget: f3 vs f6")
    
    print("Все графики успешно построены.")