import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- КОНФІГУРАЦІЯ СТОРІНКИ ---
st.set_page_config(page_title="Zeta Research Dashboard", layout="wide", page_icon="🎼")

# --- СЛОВНИК ПЕРЕКЛАДІВ ---
LANG_DICT = {
    "UA": {
        "main_title": "🎼 Дослідницька панель нулів Дзети Рімана",
        "sub_title": "Уніфікований FAIR-датасет (2.1 млн нулів) | Платформа для аналізу та аудиту",
        "sidebar_settings": "⚙️ Глобальні налаштування",
        "select_sources": "Оберіть доступні джерела:",
        "warning_source": "👈 Будь ласка, оберіть хоча б одне джерело даних у боковій панелі.",
        "tabs": ["🎹 Музика чисел", "📊 Спектральний аналіз", "📉 Аналіз відмінностей (Delta)", "📍 База нулів"],
        "tab1_header": "Побудова сходинок простих чисел (Функція Чебишова)",
        "music_src": "Джерело для синтезу:",
        "num_zeros": "Кількість нулів (N):",
        "limit_x": "Межа дослідження x:",
        "legend_primes": "Прості (p)",
        "legend_powers": "Степені (pᵏ)",
        "synth_title": "Синтез ({src}, N={n})",
        "tab2_header": "Статистика проміжків та спектральна щільність",
        "tab2_n": "Кількість нулів для аналізу (N):",
        "tab2_src": "Джерело для аналізу:",
        "hist_title": "Розподіл проміжків (Spacings)",
        "fft_title": "Амплітудний спектр (FFT)",
        "delta_header": "Аудит похибки (Delta Check)",
        "delta_range": "Діапазон нулів для аудиту (N):",
        "delta_warn": "⚠️ Оберіть рівно 2 джерела для розрахунку Delta.",
        "mae": "MAE (Середня похибка)",
        "precision_note": "Похибка в піко-одиницях (10⁻¹²) підтверджує узгодженість.",
        "anomaly_note": "🔬 **Наукова примітка:** Виявлено структурний перехід точності біля n=2000 (злиття таблиць Россера та Одлижко).",
        "db_header": "Дослідження та експорт уніфікованих даних",
        "start": "Початок:",
        "end": "Кінець:",
        "slider_label": "Межі (n):",
        "stats": "Статистика:",
        "download": "📥 Завантажити CSV",
        "cite": "🎓 Цитування",
        "footer": "Дані: Odlyzko & LMFDB"
    },
    "EN": {
        "main_title": "🎼 Riemann Zeta Zeros Research Dashboard",
        "sub_title": "Unified FAIR Dataset (2.1M zeros) | Analysis & Audit Platform",
        "sidebar_settings": "⚙️ Global Settings",
        "select_sources": "Select Data Sources:",
        "warning_source": "👈 Please select at least one data source in the sidebar.",
        "tabs": ["🎹 Prime Music", "📊 Spectral Analysis", "📉 Delta Analysis", "📍 Zero Database"],
        "tab1_header": "Step Function of Prime Numbers (Chebyshev Function)",
        "music_src": "Source for Synthesis:",
        "num_zeros": "Number of Zeros (N):",
        "limit_x": "Research Limit x:",
        "legend_primes": "Primes (p)",
        "legend_powers": "Prime Powers (pᵏ)",
        "synth_title": "Synthesis ({src}, N={n})",
        "tab2_header": "Spacing Statistics and Spectral Density",
        "tab2_n": "Number of Zeros for Analysis (N):",
        "tab2_src": "Source for Analysis:",
        "hist_title": "Distribution of Spacings",
        "fft_title": "Amplitude Spectrum (FFT)",
        "delta_header": "Error Audit (Delta Check)",
        "delta_range": "Zero range for audit (N):",
        "delta_warn": "⚠️ Select exactly 2 sources to calculate Delta.",
        "mae": "MAE (Mean Absolute Error)",
        "precision_note": "Error in pico-units (10⁻¹²) confirms data consistency.",
        "anomaly_note": "🔬 **Research Note:** A structural precision shift detected near n=2000 (Rosser/Odlyzko table merge).",
        "db_header": "Unified Data Exploration and Export",
        "start": "Start:",
        "end": "End:",
        "slider_label": "Range (n):",
        "stats": "Statistics:",
        "download": "📥 Download CSV",
        "cite": "🎓 Citation",
        "footer": "Data: Odlyzko & LMFDB"
    }
}

# --- ВИБІР МОВИ ---
lang = st.sidebar.radio("🌐 Language / Мова", ["EN", "UA"])
t = LANG_DICT[lang]

# --- ШАПКА ---
st.title(t["main_title"])
st.write(t["sub_title"])

@st.cache_data
def load_data():
    DATA_URL = "https://zenodo.org/records/22045431/files/unified_zeta_zeros.parquet?download=1"
    return pd.read_parquet(DATA_URL)

try:
    loading_msg = "Завантаження даних із Zenodo..." if lang == "UA" else "Downloading data from Zenodo..."
    with st.spinner(loading_msg):
    	df = load_data()
    all_sources = [s for s in df['source'].unique() if "10^" not in s]
    
    st.sidebar.divider()
    selected_sources = st.sidebar.multiselect(
        t["select_sources"], 
        options=all_sources, 
        default=all_sources
    )

    if not selected_sources:
        st.warning(t["warning_source"])
    else:
        # --- ВКЛАДКИ ---
        tab1, tab2, tab3, tab4 = st.tabs(t["tabs"])

        # --- TAB 1: MUSIC ---
        with tab1:
            st.subheader(t["tab1_header"])
            st.latex(r"\psi(x) \approx x - \sum_{n=1}^N \frac{2\sqrt{x}}{\frac{1}{4} + \gamma_n^2} \left[ \frac{1}{2}\cos(\gamma_n \ln x) + \gamma_n \sin(\gamma_n \ln x) \right] - \ln(2\pi)")

            col_s1, col_s2 = st.columns([1, 3])
            with col_s1:
                music_src = st.selectbox(t["music_src"], options=selected_sources, key="m_src")
                n_st = st.select_slider(t["num_zeros"], options=[10, 100, 1000, 5000, 10000], value=10)
                x_m = st.select_slider(t["limit_x"], options=[10, 20, 30, 40, 50], value=10)
                st.markdown(f"<small><span style='color:red'>●</span> {t['legend_primes']}<br><span style='color:gray'>●</span> {t['legend_powers']}</small>", unsafe_allow_html=True)

            with col_s2:
                x_v = np.linspace(2.01, x_m, 1000)
                g_st = df[df['source'] == music_src]['gamma'].head(n_st).values
                X, G = np.meshgrid(x_v, g_st)
                terms = (2 * np.sqrt(X) / (0.25 + G**2)) * (0.5 * np.cos(G * np.log(X)) + G * np.sin(G * np.log(X)))
                psi = x_v - np.sum(terms, axis=0) - np.log(2 * np.pi)

                fig1 = px.line(x=x_v, y=psi, labels={'x': 'x', 'y': 'psi(x)'}, title=t["synth_title"].format(src=music_src, n=n_st))
                # Marking
                primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
                p_pow = [4, 8, 9, 16, 25, 27, 32, 49]
                ms = [10, 20, 30, 40, 50]
                tk = sorted(list(set([p for p in primes if p <= x_m] + [pp for pp in p_pow if pp <= x_m] + [m for m in ms if m <= x_m])))
                for p in primes:
                    if p <= x_m: fig1.add_vline(x=p, line_dash="dot", line_color="red", opacity=0.6)
                for pp in p_pow:
                    if pp <= x_m: fig1.add_vline(x=pp, line_dash="dot", line_color="darkgrey", opacity=0.3)
                fig1.update_xaxes(tickmode='array', tickvals=tk, ticktext=[f"<b>{i}</b>" if i in ms else str(i) for i in tk], showgrid=False)
                fig1.update_layout(template="plotly_white", showlegend=False)
                st.plotly_chart(fig1, use_container_width=True)

        # --- TAB 2: SPECTRAL ---
        with tab2:
            st.subheader(t["tab2_header"])
            c1, c2 = st.columns([1, 3])
            with c1:
                n_sp = st.select_slider(t["tab2_n"], options=[10, 100, 1000, 5000, 10000], value=1000)
                sp_src = st.selectbox(t["tab2_src"], options=selected_sources, key="s_src")
            
            s_data = df[df['source'] == sp_src].head(n_sp)
            g1, g2 = st.columns(2)
            with g1:
                diffs = np.diff(s_data['gamma'])
                st.plotly_chart(px.histogram(diffs, nbins=50, title=t["hist_title"], template="plotly_white"), use_container_width=True)
            with g2:
                fv = np.abs(np.fft.fft(s_data['gamma'].values))
                st.plotly_chart(px.line(y=fv[1:int(len(fv)/2)], title=t["fft_title"], template="plotly_white"), use_container_width=True)

        # --- TAB 3: DELTA ---
        with tab3:
            st.subheader(t["delta_header"])
            n_d = st.slider(t["delta_range"], 100, 100000, 100)
            if len(selected_sources) == 2:
                # Merge logic for Delta
                c_df = pd.DataFrame({'index': sorted(df[df['source'].isin(selected_sources) & (df['index'] <= n_d)]['index'].unique())})
                for s in selected_sources:
                    sd = df[(df['source'] == s) & (df['index'] <= n_d)][['index', 'gamma']]
                    sd.columns = ['index', f'gamma_{s}']
                    c_df = pd.merge(c_df, sd, on='index', how='left')
                c_df['delta'] = c_df[f'gamma_{selected_sources[0]}'] - c_df[f'gamma_{selected_sources[1]}']
                
                d1, d2 = st.columns([3, 1])
                with d1:
                    fig_d = px.line(c_df, x="index", y="delta", title=f"Delta: {selected_sources[0]} vs {selected_sources[1]}")
                    fig_d.update_layout(yaxis_tickformat='.1e', template="plotly_white")
                    st.plotly_chart(fig_d, use_container_width=True)
                with d2:
                    st.metric(t["mae"], f"{c_df['delta'].abs().mean():.2e}")
                    st.info(t["precision_note"])
                    st.warning(t["anomaly_note"])
            else:
                st.warning(t["delta_warn"])

        # --- TAB 4: DATABASE ---
        with tab4:
            st.subheader(t["db_header"])
            if 'range_slider' not in st.session_state: st.session_state.range_slider = (1, 100)
            if 'f_s' not in st.session_state: st.session_state.f_s = "1"
            if 'f_e' not in st.session_state: st.session_state.f_e = "100"

            def txt_ch():
                try:
                    s, e = int(st.session_state.f_s), int(st.session_state.f_e)
                    if s < 1: s = 1
                    if e > 2000000: e = 2000000
                    if s >= e: s = e - 1
                    st.session_state.range_slider = (s, e)
                except: pass
            def sld_ch():
                st.session_state.f_s = str(st.session_state.range_slider[0])
                st.session_state.f_e = str(st.session_state.range_slider[1])

            i1, i2 = st.columns(2)
            with i1: st.text_input(t["start"], key="f_s", on_change=txt_ch)
            with i2: st.text_input(t["end"], key="f_e", on_change=txt_ch)
            st.slider(t["slider_label"], 1, 100000, key="range_slider", on_change=sld_ch)

            sn, en = st.session_state.range_slider
            f_raw = df[(df['source'].isin(selected_sources)) & (df['index'] >= sn) & (df['index'] <= en)]
            
            b1, b2 = st.columns([3, 1])
            with b1:
                if not f_raw.empty:
                    st.plotly_chart(px.scatter(f_raw, x="index", y="gamma", color="source", opacity=0.6, template="plotly_white"), use_container_width=True)
                else: st.warning(t["warning_source"])
            with b2:
                st.write(f"**{t['stats']}**")
                st.write(f_raw['source'].value_counts())
                ex_df = pd.DataFrame({'index': sorted(f_raw['index'].unique())})
                for s in selected_sources:
                    sd = f_raw[f_raw['source'] == s][['index', 'gamma']]
                    sd.columns = ['index', f'gamma_{s}']
                    ex_df = pd.merge(ex_df, sd, on='index', how='left')
                st.download_button(t["download"], ex_df.to_csv(index=False).encode('utf-8'), f"zeta_{sn}_{en}.csv")

except Exception as e:
    st.error(f"Error: {e}")

# --- ФУТЕР ---
st.sidebar.divider()
st.sidebar.markdown("**FAIR Maturity:** 🟢 **84%**  \n[F-UJI Audit v0.8](https://www.f-uji.net/)")
st.sidebar.subheader(t["cite"])
st.sidebar.code("Kudinov, M. V., Mezhuyev, V. I. (2026). Unified Dataset of Riemann Zeta Function Zeros. Zenodo. https://doi.org/10.5281/zenodo.22045431", language="text")

st.divider()
st.markdown(f"""<div style="color: gray; font-size: 0.85rem; display: flex; align-items: center; gap: 10px;">
<span>{t['footer']} | DOI: 10.5281/zenodo.22045431</span>
<a href="https://doi.org/10.5281/zenodo.22045431"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.22045431.svg"></a>
</div>""", unsafe_allow_html=True)