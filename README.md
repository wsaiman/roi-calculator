# 🚗 ROI Calculator

An interactive **Streamlit** rebuild of the ROI Calculator spreadsheet used to evaluate
Excise Duty, Sales Tax and ROI eligibility for the EEV (Energy Efficient Vehicle) / ILP
incentive scheme.

Only the highlighted **input fields** are editable — every other figure is computed live,
exactly following the original formulas, item names and remarks from the source workbook.

## ✨ Features

- **National** and **Non-National (EEV)** calculation blocks, laid out like the original spreadsheet
- Live recalculation of Excise Duty, Sales Tax, Total Taxes, and **ROI %** eligibility (≥ 100% requirement)
- Colour-coded cells matching the original Excel (yellow = input, blue/purple = computed, green = pass)

## 🖥️ Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (already done if you're reading this on GitHub 🙂)
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**
3. Point it to this repo, branch `main`, main file `app.py`
4. Deploy — share the generated link with stakeholders

## 📁 Files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit application |
| `requirements.txt` | Python dependencies |
| `ROI Calculator.xlsx` | Original source spreadsheet (reference) |

## Inputs (yellow cells)

| Letter | Item |
|---|---|
| a | Excise Rate |
| b | Ex-Work |
| c | *ILP Standard |
| h | ILP Ratio |
| j | Investment |
| k | Export (Net Export Value) |
| l | Volume Request (units) |
