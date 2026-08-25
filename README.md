# 🎼 Riemann Zeta Zeros Research Dashboard
### Дослідницька панель нулів Дзети Рімана

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_red.svg)](https://zeta-research.streamlit.app)
[![Data DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22045431.svg)](https://doi.org/10.5281/zenodo.22045431)
[![FAIR Score](https://img.shields.io/badge/FAIR_Maturity-84%25-green)](https://www.f-uji.net/)

---

## 🌎 English Description

An interactive, FAIR-compliant computational framework for the analysis, visualization, and audit of the non-trivial zeros of the Riemann zeta function. This project integrates 2.1 million zeros from historical and modern sources into a single, high-performance ecosystem.

### 🚀 Key Features:
*   **Unified Data:** Combines Odlyzko's historical tables (1989-2001) with modern LMFDB verified records.
*   **Four Research Modules:**
    1.  **Prime Music:** Real-time synthesis of the Chebyshev step function $\psi(x)$ using up to 10,000 harmonics.
    2.  **Spectral Analysis:** Spacing statistics (GUE hypothesis) and Fast Fourier Transform (FFT) density analysis.
    3.  **Delta Audit:** Precision verification between datasets (discrepancies detected at pico-unit scale $10^{-12}$).
    4.  **Zero Database:** Flexible exploration and export of the unified 26MB Apache Parquet dataset.
*   **Scientific Insight:** Detects a structural precision shift at $n=2000$ due to the integration of Rosser’s tables into Odlyzko's array.
*   **FAIR Principles:** Achieved a **84% High Maturity** score on the F-UJI assessment.

### 🛠 Installation & Local Usage:
1. Clone the repository: `git clone https://github.com/your-username/zeta-research-dashboard.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

---

## 🇺🇦 Опис проекту (Ukrainian)

Інтерактивна обчислювальна платформа для аналізу, візуалізації та аудиту нетривіальних нулів дзета-функції Рімана, розроблена згідно з принципами FAIR. Проект об'єднує 2.1 млн нулів з історичних та сучасних джерел у єдину високопродуктивну екосистему.

### 🚀 Ключові можливості:
*   **Уніфіковані дані:** Об'єднання таблиць Одлижко (1989-2001) та верифікованих записів LMFDB.
*   **Чотири дослідницькі модулі:**
    1.  **Музика чисел:** Синтез сходинок Чебишова $\psi(x)$ в реальному часі.
    2.  **Спектральний аналіз:** Статистика проміжків та швидке перетворення Фур'є (FFT).
    3.  **Аналіз відмінностей:** Аудит точності між джерелами (виявлення розбіжностей на піко-рівні $10^{-12}$).
    4.  **База нулів:** Дослідження та експорт даних у форматі Apache Parquet.
*   **Наукова цінність:** Виявлено структурний перехід точності біля $n=2000$, що свідчить про зміну методології в історичних даних.
*   **Принципи FAIR:** Отримано оцінку **84% (High Maturity)** за аудитом F-UJI.

---

## 📊 Data Provenance & FAIRness
*   **Original Data:** Andrew Odlyzko (University of Minnesota) & [LMFDB](https://www.lmfdb.org/).
*   **Processing:** Data cleaned, offsets recalculated, and converted to Apache Parquet via Python/Pandas.
*   **FAIR Audit:** Evaluated using F-UJI (FsF-v0.8 metrics). Score: **84%**.

---

## 🎓 Citation / Цитування
If you use this dataset or software in your research, please cite it as:
*Якщо ви використовуєте ці дані або софт у дослідженні, будь ласка, цитуйте їх так:*

> **Kudinov, M. V., Mezhuyev, V. I. (2026). Unified Dataset of Riemann Zeta Function Zeros. Zenodo. https://doi.org/10.5281/zenodo.22045431**

---

## 📜 License / Ліцензія
*   **Software:** Licensed under the **MIT License**.
*   **Data:** Licensed under **CC-BY-SA 4.0** (Creative Commons Attribution-ShareAlike).

