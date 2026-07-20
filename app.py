import streamlit as st

st.set_page_config(page_title="ROI Calculator", page_icon="⚡", layout="centered")

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .block-container { max-width: 640px; padding-top: 2rem; padding-bottom: 3rem; }

    .section-title {
        background-color: #D9D9D9;
        font-weight: 700;
        padding: 8px 14px;
        border-radius: 6px;
        margin: 22px 0 12px 0;
    }

    .calc-card {
        border: 1px solid #e6e6e6;
        border-radius: 10px;
        padding: 12px 14px 10px 14px;
        margin-bottom: 10px;
        background: #fff;
    }
    .calc-card.blue-card { border-left: 6px solid #44B3E1; }
    .calc-card.purple-card { border-left: 6px solid #9999FF; }
    .calc-card.green-card { border-left: 6px solid #2FA84F; background: #EEFBF1; }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stNumberInput"]),
    div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stTextInput"]) {
        border-left: 6px solid #FFD600 !important;
        background: #FFFDE0;
    }

    .card-head {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 4px;
    }
    .card-title { font-weight: 600; font-size: 1rem; }
    .letter-badge {
        display: inline-block;
        background: #0070C0;
        color: white;
        font-weight: 700;
        font-size: 0.75rem;
        border-radius: 50%;
        width: 20px; height: 20px;
        line-height: 20px;
        text-align: center;
        margin-right: 6px;
    }
    .formula-tag { color: #888; font-style: italic; font-size: 0.85rem; }

    .amount-value {
        font-size: 1.25rem;
        font-weight: 700;
        margin: 4px 0 2px 0;
    }
    .meta-line { color: #666; font-size: 0.82rem; margin-top: 2px; }
    .req-line { color: #a15c00; font-size: 0.82rem; margin-top: 2px; }

    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input {
        background-color: #FFFF00 !important;
        font-weight: 600;
    }

    .app-title { font-size: 2.1rem; font-weight: 800; margin-bottom: 10px; }
    .fill-hint {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #FFFDE0;
        border: 1px solid #FFD600;
        border-left: 6px solid #FFD600;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 22px;
        font-size: 0.92rem;
        color: #4a4000;
    }
    .fill-hint-icon { font-size: 1.4rem; line-height: 1; }
    </style>
    """,
    unsafe_allow_html=True,
)


def fmt(x, decimals=0):
    return f"{x:,.{decimals}f}"


def nz(x):
    return x if x is not None else 0.0


def section_title(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def input_field(letter, item, key, remark="", formula="N/A", placeholder=None, **kwargs):
    with st.container(border=True):
        st.markdown(
            f'<div class="card-head">'
            f'<span class="card-title"><span class="letter-badge">{letter}</span>{item}</span>'
            f'<span class="formula-tag">{formula}</span></div>',
            unsafe_allow_html=True,
        )
        val = st.number_input(
            item, value=None, placeholder=placeholder,
            label_visibility="collapsed", key=key, **kwargs,
        )
        if remark:
            st.markdown(f'<div class="meta-line">{remark}</div>', unsafe_allow_html=True)
    return val


def money_input(letter, item, key, remark="", formula="N/A", placeholder=None, decimals=0):
    if key in st.session_state:
        cleaned = st.session_state[key].replace(",", "").strip()
        if cleaned:
            try:
                st.session_state[key] = f"{float(cleaned):,.{decimals}f}"
            except ValueError:
                pass
    with st.container(border=True):
        st.markdown(
            f'<div class="card-head">'
            f'<span class="card-title"><span class="letter-badge">{letter}</span>{item}</span>'
            f'<span class="formula-tag">{formula}</span></div>',
            unsafe_allow_html=True,
        )
        text_val = st.text_input(
            item, placeholder=placeholder,
            label_visibility="collapsed", key=key,
        )
        if remark:
            st.markdown(f'<div class="meta-line">{remark}</div>', unsafe_allow_html=True)
    if text_val:
        cleaned = text_val.replace(",", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def computed_field(letter, item, formula, amount_str, color, requirement="", remark=""):
    req_html = f'<div class="req-line">Requirement: {requirement}</div>' if requirement else ""
    remark_html = f'<div class="meta-line">{remark}</div>' if remark else ""
    st.markdown(
        f'<div class="calc-card {color}-card">'
        f'<div class="card-head">'
        f'<span class="card-title"><span class="letter-badge">{letter}</span>{item}</span>'
        f'<span class="formula-tag">{formula}</span></div>'
        f'<div class="amount-value">{amount_str}</div>'
        f'{req_html}{remark_html}</div>',
        unsafe_allow_html=True,
    )


st.markdown(
    '<div class="app-title">ROI Calculator ⚡</div>'
    '<div class="fill-hint"><span class="fill-hint-icon">✏️</span>'
    '<span><strong>Fill up the yellow input box only</strong> — semua baris lain kira sendiri.</span></div>',
    unsafe_allow_html=True,
)

# ==================================================================
# Section 1 — National (baseline)
# ==================================================================
a_in = input_field("a", "Excise Rate", "a",
                    "Excise rate body type and engine. Refer to Table 1. "
                    "Please input percentage figure (cth: 60 untuk 60%).",
                    placeholder="cth: 60", format="%.2f", step=1.0)
b_in = money_input("b", "Ex-Work", "b", "Total Cost to Produce Vehicles in Plant.",
                    placeholder="cth: 65,515.00", decimals=2)
c_in = money_input("c", "*ILP Standard", "c", "",
                    placeholder="cth: 27,269.00", decimals=2)

a, b, c = nz(a_in) / 100.0, nz(b_in), nz(c_in)

d = b * a
computed_field("d", "Excise Duty (W/out ILP)", "b*a", fmt(d), "blue")

e = (b - c) * a
min_duty = d * 0.15
computed_field("e", "Excise Duty (With ILP Standard)", "(b-c)*a", fmt(e), "blue",
                requirement=fmt(min_duty), remark="MIN. 15% Duty payment to gov for non-national")

f = (b + e - c) * 0.10
computed_field("f", "Sales Tax (With ILP Standard)", "(b+e-c)*10%", fmt(f, 2), "blue")

g = e + f
computed_field("g", "Total Taxes", "e+f", fmt(g, 2), "blue")

# ==================================================================
# Section 2 — Non-National (EEV)
# ==================================================================
section_title("Non-National")

h_in = input_field("h", "ILP Ratio", "h", "Best ratio based on ROI formula by MARii.",
                    placeholder="cth: 1.92", format="%.2f", step=0.01)

h = nz(h_in)
i = c * h
computed_field("i", "ILP Amount (EEV)", "c*h", fmt(i), "purple",
                remark="New ILP amount increased by (h) ratio from ILP standard")

j_in = money_input("j", "Investment", "j", "Any investment related to automotive",
                    placeholder="cth: 110,000,000.00", decimals=2)
k_in = money_input("k", "Export (Net Export Value)", "k", "Any export, CBU or component.",
                    placeholder="0 jika tiada", decimals=2)
l_in = money_input("l", "Volume Request (units)", "l", "Any additional unit will require additional investment.",
                    placeholder="cth: 3,500", decimals=0)

j, k, l = nz(j_in), nz(k_in), nz(l_in)

n_raw = (b - i) * a
n = min_duty if n_raw < min_duty else n_raw
o = (b + n) * 0.10 * 0.15
p = n + o
q = g - p
r = p * l
s = q * l
roi = (j + k + r - s) / s if s else 0.0
direct_exemption = (1 - n / d) if d else 0.0

roi_color = "green" if roi >= 1.0 else "blue"
computed_field("m", "ROI &gt; 100%", "[j+k+r-s]/s", f"{roi * 100:,.0f}%", roi_color,
                requirement="100%", remark="Must be &gt;= 100% to be get additional ILP (EEV Incentive)")

computed_field("n", "Excise Duty Per unit", "MAX[(b-i)*a, min 15%]", fmt(n), "purple",
                requirement=fmt(min_duty), remark="MIN. 15% Duty payment to gov for non-national")

computed_field("★", "Direct Exemption", "1-(n/d)", f"{direct_exemption * 100:,.0f}%", "purple",
                remark="% of excise duty exempted vs. paying full duty without ILP")

computed_field("o", "Sales Tax Per Unit", "(b+n)*10%*15%", fmt(o), "purple")

computed_field("p", "Tax Payment per unit", "n+o", fmt(p), "purple",
                remark="Actual tax paid with EEV incentive")

computed_field("q", "Tax Forgone per unit", "g-p", fmt(q), "purple",
                remark="Higher tax forgone reduce ROI%")

computed_field("r", "Total Taxes Payment", "p*l", fmt(r), "purple",
                remark="Tax Payment with EEV incentive")

computed_field("s", "Total Taxes Foregone", "q*l", fmt(s), "purple",
                remark="Tax Foregone by the government")

st.caption(
    "Nota: kotak kuning sahaja yang boleh diedit (a, b, c, h, j, k, l), kosong secara default. "
    "Semua baris lain dikira secara automatik mengikut formula asal dalam EEV Calculator.xlsx."
)
