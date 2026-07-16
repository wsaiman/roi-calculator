import streamlit as st

st.set_page_config(page_title="ROI Calculator", layout="centered")

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
    .calc-card.input-card {
        background: #FFFDE0;
        border-left: 6px solid #FFD600;
    }
    .calc-card.blue-card { border-left: 6px solid #44B3E1; }
    .calc-card.purple-card { border-left: 6px solid #9999FF; }
    .calc-card.green-card { border-left: 6px solid #2FA84F; background: #EEFBF1; }

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

    div[data-testid="stNumberInput"] input {
        background-color: #FFFF00 !important;
        font-weight: 600;
    }
    div[data-testid="stNumberInput"] { margin-top: -6px; margin-bottom: 2px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def fmt(x, decimals=0):
    return f"{x:,.{decimals}f}"


def section_title(title):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)


def input_field(letter, item, key, value, remark="", formula="N/A", **kwargs):
    st.markdown(
        f"""
        <div class="calc-card input-card">
            <div class="card-head">
                <span class="card-title"><span class="letter-badge">{letter}</span>{item}</span>
                <span class="formula-tag">{formula}</span>
            </div>
        """,
        unsafe_allow_html=True,
    )
    val = st.number_input(item, value=value, label_visibility="collapsed", key=key, **kwargs)
    if remark:
        st.markdown(f"<div class='meta-line'>{remark}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return val


def computed_field(letter, item, formula, amount_str, color, requirement="", remark=""):
    req_html = f"<div class='req-line'>Requirement: {requirement}</div>" if requirement else ""
    remark_html = f"<div class='meta-line'>{remark}</div>" if remark else ""
    st.markdown(
        f"""
        <div class="calc-card {color}-card">
            <div class="card-head">
                <span class="card-title"><span class="letter-badge">{letter}</span>{item}</span>
                <span class="formula-tag">{formula}</span>
            </div>
            <div class="amount-value">{amount_str}</div>
            {req_html}
            {remark_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.title("ROI Calculator")

# ==================================================================
# Section 1 — National (baseline)
# ==================================================================
a = input_field("a", "Excise Rate", "a", 0.60, "Excise rate body type and engine. Refer to Table 1.",
                 format="%.2f", step=0.01)
b = input_field("b", "Ex-Work", "b", 65515.00, "Total Cost to Produce Vehicles in Plant.",
                 format="%.2f", step=100.0)
c = input_field("c", "*ILP Standard", "c", 27269.0, "", format="%.2f", step=100.0)

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

h = input_field("h", "ILP Ratio", "h", 1.92, "Best ratio based on ROI formula by MARii.",
                format="%.2f", step=0.01)

i = c * h
computed_field("i", "ILP Amount (EEV)", "c*h", fmt(i), "purple",
                remark="New ILP amount increased by (h) ratio from ILP standard")

j = input_field("j", "Investment", "j", 110000000.0, "Any investment related to automotive",
                format="%.2f", step=100000.0)
k = input_field("k", "Export (Net Export Value)", "k", 0.0, "Any export, CBU or component. Masukkan 0 jika tiada ('-')",
                format="%.2f", step=1000.0)
l = input_field("l", "Volume Request (units)", "l", 3500.0, "Any additional unit will require additional investment.",
                format="%.0f", step=10.0)

n = (b - i) * a
o = (b + n - i) * 0.10
p = n + o
q = g - p
r = p * l
s = q * l
roi = (i + j + k + r - s) / s if s else 0.0

roi_color = "green" if roi >= 1.0 else "blue"
computed_field("m", "ROI &gt; 100%", "[i+j+k+r-s]/s", f"{roi * 100:,.0f}%", roi_color,
                requirement="100%", remark="Must be &gt;= 100% to be get additional ILP (EEV Incentive)")

computed_field("n", "Excise Duty Per unit", "(b-i)*a", fmt(n), "purple",
                requirement=fmt(min_duty), remark="MIN. 15% Duty payment to gov for non-national")

computed_field("o", "Sales Tax Per Unit", "(b+n-i)*10%", fmt(o), "purple")

computed_field("p", "Tax Payment per unit", "n+o", fmt(p), "purple",
                remark="Actual tax paid with EEV incentive")

computed_field("q", "Tax Forgone per unit", "g-p", fmt(q), "purple",
                remark="Higher tax forgone reduce ROI%")

computed_field("r", "Total Taxes Payment", "p*l", fmt(r), "purple",
                remark="Tax Payment with EEV incentive")

computed_field("s", "Total Taxes Foregone", "q*l", fmt(s), "purple",
                remark="Tax Foregone by the government")

st.caption(
    "Nota: kotak kuning sahaja yang boleh diedit (a, b, c, h, j, k, l). "
    "Semua baris lain dikira secara automatik mengikut formula asal dalam ROI Calculator.xlsx."
)
