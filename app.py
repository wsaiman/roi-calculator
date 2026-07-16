from datetime import datetime

import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos

st.set_page_config(page_title="ROI Calculator", layout="wide")

# ---------- Styling to mirror the original Excel colours ----------
st.markdown(
    """
    <style>
    .header-cell {
        background-color: #0070C0;
        color: white;
        font-weight: 600;
        padding: 6px 10px;
        border-radius: 3px;
        text-align: center;
    }
    .section-title {
        background-color: #D9D9D9;
        font-weight: 700;
        padding: 6px 10px;
        border-radius: 3px;
    }
    .amount-blue { background-color:#44B3E1; padding:4px 8px; border-radius:3px; display:block; text-align:right; }
    .amount-purple { background-color:#9999FF; padding:4px 8px; border-radius:3px; display:block; text-align:right; }
    .amount-green { background-color:#C6EFCE; padding:4px 8px; border-radius:3px; display:block; text-align:right; font-weight:700; }
    .req-cell { padding:4px 8px; text-align:right; display:block; }
    .item-cell { padding:4px 4px; font-weight:500; }
    .formula-cell { padding:4px 4px; color:#555; font-style:italic; }
    .remark-cell { padding:4px 4px; color:#333; font-size:0.9em; }
    .letter-cell { padding:4px 4px; text-align:center; font-weight:700; color:#0070C0; }
    div[data-testid="stNumberInput"] input { background-color:#FFFF00 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def fmt(x, decimals=0):
    return f"{x:,.{decimals}f}"


def build_pdf(report_rows, roi_pct, roi_pass, remarks):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "ROI Calculator Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(0, 112, 192)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(12, 8, "#", border=1, fill=True, align="C")
    pdf.cell(90, 8, "Item", border=1, fill=True)
    pdf.cell(40, 8, "Amount", border=1, fill=True, align="R")
    pdf.ln()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)

    for letter, item, amount in report_rows:
        pdf.cell(12, 7, letter, border=1, align="C")
        pdf.cell(90, 7, item, border=1)
        pdf.cell(40, 7, amount, border=1, align="R")
        pdf.ln()

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    fill = (198, 239, 206) if roi_pass else (255, 199, 206)
    pdf.set_fill_color(*fill)
    pdf.cell(0, 10, f"ROI: {roi_pct:,.0f}%  ({'MEETS' if roi_pass else 'BELOW'} 100% requirement)",
              border=1, fill=True, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Remarks", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    for letter, item, remark in remarks:
        if remark:
            pdf.multi_cell(0, 5, f"{letter}) {item}: {remark}",
                            new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return bytes(pdf.output())


def row(letter, item, formula, amount_html, requirement, remark):
    cols = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])
    cols[0].markdown(f"<div class='letter-cell'>{letter}</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='item-cell'>{item}</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div class='formula-cell'>{formula}</div>", unsafe_allow_html=True)
    cols[3].markdown(amount_html, unsafe_allow_html=True)
    cols[4].markdown(f"<div class='req-cell'>{requirement}</div>", unsafe_allow_html=True)
    cols[5].markdown(f"<div class='remark-cell'>{remark}</div>", unsafe_allow_html=True)


def header():
    cols = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])
    labels = ["#", "Item", "Formula", "Amount", "Requirement", "Remark"]
    for c, l in zip(cols, labels):
        c.markdown(f"<div class='header-cell'>{l}</div>", unsafe_allow_html=True)


st.title("ROI Calculator")

# ==================================================================
# Section 1 — National (baseline)
# ==================================================================
header()

col_a = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])[3]
a = col_a.number_input("a", value=0.60, format="%.2f", step=0.01, label_visibility="collapsed", key="a")
row("a", "Excise Rate", "N/A", "", "", "Excise rate body type and engine. Refer to Table 1.")

col_b = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])[3]
b = col_b.number_input("b", value=65515.00, format="%.2f", step=100.0, label_visibility="collapsed", key="b")
row("b", "Ex-Work", "N/A", "", "", "Total Cost to Produce Vehicles in Plant.")

col_c = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])[3]
c = col_c.number_input("c", value=27269.0, format="%.2f", step=100.0, label_visibility="collapsed", key="c")
row("c", "*ILP Standard", "N/A", "", "", "")

st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

d = b * a
row("d", "Excise Duty (W/out ILP)", "b*a",
    f"<div class='amount-blue'>{fmt(d)}</div>", "", "")

e = (b - c) * a
min_duty = d * 0.15
row("e", "Excise Duty (With ILP Standard)", "(b-c)*a",
    f"<div class='amount-blue'>{fmt(e)}</div>", fmt(min_duty),
    "MIN. 15% Duty payment to gov for non-national")

f = (b + e - c) * 0.10
row("f", "Sales Tax (With ILP Standard)", "(b+e-c)*10%",
    f"<div class='amount-blue'>{fmt(f, 2)}</div>", "", "")

g = e + f
row("g", "Total Taxes", "e+f",
    f"<div class='amount-blue'>{fmt(g, 2)}</div>", "", "")

st.markdown("<div class='section-title'>Non-National</div>", unsafe_allow_html=True)
header()

col_h = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])[3]
h = col_h.number_input("h", value=1.92, format="%.2f", step=0.01, label_visibility="collapsed", key="h")
row("h", "ILP Ratio", "", "", "", "Best ratio based on ROI formula by MARii.")

i = c * h
row("i", "ILP Amount (EEV)", "c*h",
    f"<div class='amount-purple'>{fmt(i)}</div>", "",
    "New ILP amount increased by (h) ratio from ILP standard")

col_j = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])[3]
j = col_j.number_input("j", value=110000000.0, format="%.2f", step=100000.0, label_visibility="collapsed", key="j")
row("j", "Investment", "N/A", "", "", "Any investment related to automotive")

col_k = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])[3]
k = col_k.number_input("k", value=0.0, format="%.2f", step=1000.0, label_visibility="collapsed", key="k",
                        help="Masukkan 0 jika tiada export ('-')")
row("k", "Export (Net Export Value)", "N/A", "", "", "Any export, CBU or component.")

col_l = st.columns([0.4, 2, 1.3, 1.6, 1.1, 3])[3]
l = col_l.number_input("l", value=3500.0, format="%.0f", step=10.0, label_visibility="collapsed", key="l")
row("l", "Volume Request (units)", "N/A", "", "", "Any additional unit will require additional investment.")

st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

n = (b - i) * a
o = (b + n - i) * 0.10
p = n + o
q = g - p
r = p * l
s = q * l
roi = (i + j + k + r - s) / s if s else 0.0

roi_color = "amount-green" if roi >= 1.0 else "amount-blue"
row("m", "ROI &gt; 100%", "[i+j+k+r-s]/s",
    f"<div class='{roi_color}'>{roi*100:,.0f}%</div>", "100%",
    "Must be &gt;= 100% to be get additional ILP (EEV Incentive)")

row("n", "Excise Duty Per unit", "(b-i)*a",
    f"<div class='amount-purple'>{fmt(n)}</div>", fmt(min_duty),
    "MIN. 15% Duty payment to gov for non-national")

row("o", "Sales Tax Per Unit", "(b+n-i)*10%",
    f"<div class='amount-purple'>{fmt(o)}</div>", "", "")

row("p", "Tax Payment per unit", "n+o",
    f"<div class='amount-purple'>{fmt(p)}</div>", "", "Actual tax paid with EEV incentive")

row("q", "Tax Forgone per unit", "g-p",
    f"<div class='amount-purple'>{fmt(q)}</div>", "", "Higher tax forgone reduce ROI%")

row("r", "Total Taxes Payment", "p*l",
    f"<div class='amount-purple'>{fmt(r)}</div>", "", "Tax Payment with EEV incentive")

row("s", "Total Taxes Foregone", "q*l",
    f"<div class='amount-purple'>{fmt(s)}</div>", "", "Tax Foregone by the government")

st.caption(
    "Nota: kotak kuning sahaja yang boleh diedit (a, b, c, h, j, k, l). "
    "Semua baris lain dikira secara automatik mengikut formula asal dalam ROI Calculator.xlsx."
)

st.divider()

report_rows = [
    ("a", "Excise Rate", f"{a * 100:,.0f}%"),
    ("b", "Ex-Work", fmt(b, 2)),
    ("c", "*ILP Standard", fmt(c, 2)),
    ("d", "Excise Duty (W/out ILP)", fmt(d)),
    ("e", "Excise Duty (With ILP Standard)", fmt(e)),
    ("f", "Sales Tax (With ILP Standard)", fmt(f, 2)),
    ("g", "Total Taxes", fmt(g, 2)),
    ("h", "ILP Ratio", f"{h:,.2f}"),
    ("i", "ILP Amount (EEV)", fmt(i)),
    ("j", "Investment", fmt(j, 2)),
    ("k", "Export (Net Export Value)", fmt(k, 2)),
    ("l", "Volume Request (units)", fmt(l)),
    ("n", "Excise Duty Per unit", fmt(n)),
    ("o", "Sales Tax Per Unit", fmt(o)),
    ("p", "Tax Payment per unit", fmt(p)),
    ("q", "Tax Forgone per unit", fmt(q)),
    ("r", "Total Taxes Payment", fmt(r)),
    ("s", "Total Taxes Foregone", fmt(s)),
]

remarks = [
    ("a", "Excise Rate", "Excise rate body type and engine. Refer to Table 1."),
    ("b", "Ex-Work", "Total Cost to Produce Vehicles in Plant."),
    ("e", "Excise Duty (With ILP Standard)", "MIN. 15% Duty payment to gov for non-national"),
    ("h", "ILP Ratio", "Best ratio based on ROI formula by MARii."),
    ("i", "ILP Amount (EEV)", "New ILP amount increased by (h) ratio from ILP standard"),
    ("j", "Investment", "Any investment related to automotive"),
    ("k", "Export (Net Export Value)", "Any export, CBU or component."),
    ("l", "Volume Request (units)", "Any additional unit will require additional investment."),
    ("m", "ROI > 100%", "Must be >= 100% to be get additional ILP (EEV Incentive)"),
    ("n", "Excise Duty Per unit", "MIN. 15% Duty payment to gov for non-national"),
    ("p", "Tax Payment per unit", "Actual tax paid with EEV incentive"),
    ("q", "Tax Forgone per unit", "Higher tax forgone reduce ROI%"),
    ("r", "Total Taxes Payment", "Tax Payment with EEV incentive"),
    ("s", "Total Taxes Foregone", "Tax Foregone by the government"),
]

pdf_bytes = build_pdf(report_rows, roi * 100, roi >= 1.0, remarks)

st.download_button(
    label="📄 Download Report (PDF)",
    data=pdf_bytes,
    file_name=f"ROI_Calculator_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
    mime="application/pdf",
    type="primary",
)
