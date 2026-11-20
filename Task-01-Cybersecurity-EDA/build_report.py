"""Build the Task 01 PDF report: styled HTML -> headless Chrome -> PDF.

If a visualization PNG is missing, a clearly labelled placeholder box is inserted
so the draft is never mistaken for a finished submission.
"""
import base64
import html
import os
import subprocess
import sys

ROOT = r"E:\Devixo\Task-01-Cybersecurity-EDA"
VIS = os.path.join(ROOT, "visualizations")
REPORTS = os.path.join(ROOT, "reports")
SHOTS = os.path.join(ROOT, "screenshots")
os.makedirs(REPORTS, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

FIGURES = [
    ("18_01_histogram_risk_signals", "Histogram — distribution of phishing-leaning signals per website",
     "Phishing sites shift right (median 10 failed checks) while legitimate sites cluster lower (median 7). "
     "The distributions overlap substantially, so the aggregate count is only a weak-to-moderate separator."),
    ("18_02_bar_top_correlations", "Bar chart — absolute correlation of each feature with the class label",
     "SSL state (0.69) and external anchor URLs (0.68) dominate; the signal drops sharply to 0.38 and below."),
    ("18_03_pie_class_balance", "Pie chart — class balance after duplicate removal",
     "The cleaned dataset is close to balanced: 51.62% phishing (3,019) versus 48.38% legitimate (2,830)."),
    ("18_04_scatter_ssl_vs_anchor", "Scatter plot — SSL state vs external anchor URL",
     "The invalid-SSL / off-site-anchor corner is dominated by phishing; the valid-SSL / on-site corner by legitimate sites."),
    ("18_05_line_threshold_rates", "Line chart — share of each class at or above a risk-signal threshold",
     "The gap is widest at a threshold of 8 (82.0% vs 47.8%) and narrows after 12, illustrating the recall / false-positive trade-off."),
    ("18_06_box_risk_signals", "Box plot — risk signals by class",
     "Medians differ (10 vs 7) but the interquartile ranges overlap (8–12 vs 6–11); phishing has the longer upper tail (max 25)."),
    ("18_07_heatmap_correlations", "Correlation heatmap — twelve strongest features and the class label",
     "Most inter-feature cells are pale, meaning the strongest predictors contribute largely independent information."),
    ("18_08_countplot_ssl_state", "Count plot — websites per SSL state, split by class",
     "61.7% of phishing sites have an invalid SSL state against 9.3% of legitimate sites."),
    ("18_09_pairplot_features", "Pair plot — strongest features and the derived risk score",
     "SSL state and external anchor URL separate the classes more clearly than the aggregate risk score."),
    ("18_10_violin_risk_signals", "Violin plot — density of risk signals by class",
     "The phishing density peaks around 8–9 failed checks, the legitimate density around 6–7."),
]

FEATURE_ROWS = [
    ("Has_IP_Address", "having_IP_Address", "URL uses a raw IP address instead of a domain name"),
    ("URL_Length", "URL_Length", "Length category of the URL"),
    ("Uses_Shortening_Service", "Shortining_Service", "URL shortened by a service such as bit.ly"),
    ("Has_At_Symbol", "having_At_Symbol", "Presence of an @ symbol in the URL"),
    ("Double_Slash_Redirect", "double_slash_redirecting", "Double slash appearing inside the URL path"),
    ("Has_Prefix_Suffix", "Prefix_Suffix", "Hyphen present in the domain name"),
    ("Has_Sub_Domain", "having_Sub_Domain", "Number of sub-domains in the URL"),
    ("SSL_State", "SSLfinal_State", "Validity of the HTTPS / SSL certificate"),
    ("Domain_Registration_Length", "Domain_registeration_length", "Registration duration of the domain"),
    ("Favicon_From_Domain", "Favicon", "Favicon loaded from the same domain or an external one"),
    ("Nonstandard_Port", "port", "Use of a non-standard network port"),
    ("HTTPS_Token_In_Domain", "HTTPS_token", "The token “https” embedded inside the domain part"),
    ("External_Request_URL", "Request_URL", "Objects inside the page requested from other domains"),
    ("External_Anchor_URL", "URL_of_Anchor", "Anchor links pointing outside the site"),
    ("External_Links_In_Tags", "Links_in_tags", "Links in meta / script / link tags pointing elsewhere"),
    ("Server_Form_Handler", "SFH", "Where the form submits to (blank, external or same domain)"),
    ("Submits_To_Email", "Submitting_to_email", "Form submits through a mailto: handler"),
    ("Abnormal_URL", "Abnormal_URL", "URL does not match the identity of the host"),
    ("Uses_Redirect", "Redirect", "Number of redirections triggered by the URL"),
    ("Mouseover_Changes_Status", "on_mouseover", "Status bar altered on mouse-over"),
    ("RightClick_Disabled", "RightClick", "Right-click context menu disabled"),
    ("PopUp_Window", "popUpWidnow", "Popup window containing a text field"),
    ("Uses_Iframe", "Iframe", "An iframe is used to display content"),
    ("Domain_Age", "age_of_domain", "Age of the domain at the time of collection"),
    ("Has_DNS_Record", "DNSRecord", "A DNS record exists for the host"),
    ("Web_Traffic", "web_traffic", "Traffic rank of the site"),
    ("Page_Rank", "Page_Rank", "PageRank value of the page"),
    ("Google_Indexed", "Google_Index", "Whether the site is indexed by Google"),
    ("Links_Pointing_To_Page", "Links_pointing_to_page", "Number of inbound links"),
    ("In_Statistical_Report", "Statistical_report", "Host appears in published phishing statistical reports"),
]

INSIGHTS = [
    ("Nearly half the dataset is duplicated, and the duplicates are biased.",
     "5,206 of 11,055 rows (47.1%) are exact duplicates. Removing them changes the class balance from "
     "44.31% / 55.69% to 51.62% / 48.38%, because 3,327 legitimate rows were duplicated versus 1,879 phishing rows."),
    ("The cleaned dataset is close to balanced.",
     "3,019 phishing (51.62%) versus 2,830 legitimate (48.38%) — a ratio of 1.07 : 1, so no resampling is needed."),
    ("There are no missing values at all.",
     "0 missing cells out of 342,705. Imputation would therefore have fabricated data; the correct decision was to perform none."),
    ("SSL state is the strongest single indicator of legitimacy (r = 0.69).",
     "61.7% of phishing sites have an invalid or absent certificate, against 9.3% of legitimate sites. "
     "90.4% of legitimate sites present a valid certificate."),
    ("External anchor URLs are the strongest indicator of phishing (r = 0.68).",
     "65.7% of phishing sites have anchor links pointing off-site, versus 0.7% of legitimate sites — "
     "effectively a near-perfect separator on its own."),
    ("A hyphen in the domain is necessary but not sufficient.",
     "100% of phishing sites are coded −1 for Has_Prefix_Suffix, but so are 75.2% of legitimate sites. "
     "Its correlation is only 0.38, so it cannot be used alone."),
    ("Popularity is a real, measurable protective factor.",
     "65.7% of legitimate sites show positive web traffic against 32.5% of phishing sites (r = 0.28)."),
    ("Several features carry no usable signal.",
     "RightClick_Disabled (94.9% vs 95.3% coded 1), PopUp_Window (r = −0.02), Uses_Iframe (r = −0.01) and "
     "Favicon_From_Domain (r = −0.03) behave almost identically in both classes. In total 18 of 30 features "
     "correlate below |r| = 0.10, and 12 of those below 0.05."),
    ("High variance does not imply predictive power.",
     "Domain_Age has the largest standard deviation in the dataset (1.00, split 2,862 / 2,987) yet correlates "
     "with the class at only r ≈ 0.06."),
    ("A simple count of failed checks is only a weak-to-moderate separator.",
     "Mean risk signals are 10.50 for phishing versus 8.10 for legitimate sites — a gap of only 2.4 — and "
     "64.1% of phishing sites fall in the same 7–11 band as 42.1% of legitimate sites."),
    ("Short domain registration periods lean phishing.",
     "Domain_Registration_Length correlates negatively (r = −0.22): phishing domains average −0.10 versus −0.52 "
     "for legitimate domains."),
    ("The target is binary — the “suspicious” class is absent.",
     "The target contains only −1 and 1; no 0 class exists, even though some descriptions of this dataset mention one."),
]


def img_block(name, caption, note):
    path = os.path.join(VIS, f"{name}.png")
    if os.path.exists(path):
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        body = f'<img src="data:image/png;base64,{b64}" alt="{html.escape(caption)}">'
        status = ""
    else:
        body = ('<div class="ph"><strong>CHART PENDING</strong><br>'
                f'Generate <code>visualizations/{name}.png</code> by running the notebook in Colab.</div>')
        status = ' class="pending"'
    return f"""
    <figure{status}>
      {body}
      <figcaption><strong>{html.escape(caption)}</strong><br><span class="note">{html.escape(note)}</span></figcaption>
    </figure>"""


def shot_block(title, filename, hint):
    path = os.path.join(SHOTS, filename)
    if os.path.exists(path):
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        body = f'<img src="data:image/png;base64,{b64}" alt="{html.escape(title)}">'
        cls = ""
    else:
        body = f'<div class="ph"><strong>SCREENSHOT PENDING</strong><br>{html.escape(hint)}<br><code>screenshots/{filename}</code></div>'
        cls = ' class="pending"'
    return f'<figure{cls}>{body}<figcaption>{html.escape(title)}</figcaption></figure>'


def build_html(draft: bool):
    feature_rows = "\n".join(
        f"<tr><td><code>{html.escape(new)}</code></td><td><code>{html.escape(orig)}</code></td><td>{html.escape(desc)}</td></tr>"
        for new, orig, desc in FEATURE_ROWS)

    insights_html = "\n".join(
        f"<li><strong>{html.escape(t)}</strong><br>{html.escape(b)}</li>" for t, b in INSIGHTS)

    figs = "\n".join(img_block(n, c, note) for n, c, note in FIGURES)

    code_shots = "\n".join([
        shot_block("Data loading and inspection", "01_loading.png", "Screenshot of the loading / head / info cells"),
        shot_block("Data cleaning — duplicates", "02_cleaning_duplicates.png", "Screenshot of the duplicate removal cell and output"),
        shot_block("Missing values and dtypes", "03_missing_dtypes.png", "Screenshot of the missing-value and dtype cells"),
        shot_block("Descriptive statistics", "04_statistics.png", "Screenshot of the statistics table"),
        shot_block("Correlation analysis", "05_correlation.png", "Screenshot of the correlation ranking"),
    ])
    out_shots = "\n".join([
        shot_block("Notebook output — class balance before and after cleaning", "06_output_balance.png", "Screenshot of the class balance output"),
        shot_block("Notebook output — evidence behind the insights", "07_output_insights.png", "Screenshot of the insights evidence cell"),
        shot_block("Execution log — every code cell completed without error", "08_execution_log.png", "Screenshot of the full run log"),
    ])
    graph_shots = "\n".join([
        shot_block("Chart gallery — all ten required visualization types", "09_charts_notebook.png", "Screenshot of the generated charts"),
        shot_block("Visualization files written by the notebook", "10_charts_files.png", "Screenshot of visualizations/ contents"),
    ])

    draft_banner = ('<div class="draft">DRAFT — placeholder boxes mark content that must be produced by running '
                    'the notebook. Do not submit this file.</div>') if draft else ""

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Task 01 — Python Programming, Data Analysis &amp; Visualization</title>
<style>
  @page {{ size: A4; margin: 18mm 16mm 18mm 16mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: "Segoe UI", "Calibri", Arial, sans-serif; font-size: 10.5pt; line-height: 1.55;
         color: #1a1a1a; margin: 0; }}
  h1, h2, h3 {{ font-family: "Segoe UI Semibold", "Segoe UI", Arial, sans-serif; color: #0f2740; }}
  h1 {{ font-size: 21pt; margin: 0 0 6pt; }}
  h2 {{ font-size: 14pt; margin: 22pt 0 8pt; padding-bottom: 4pt; border-bottom: 2px solid #2471a3; }}
  h3 {{ font-size: 11.5pt; margin: 14pt 0 5pt; color: #16496b; }}
  p {{ margin: 0 0 8pt; text-align: justify; }}
  code {{ font-family: Consolas, "Courier New", monospace; font-size: 9pt; background: #eef2f6;
          padding: 1px 4px; border-radius: 3px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 8pt 0 12pt; font-size: 9pt; }}
  th, td {{ border: 1px solid #c9d4de; padding: 4pt 6pt; text-align: left; vertical-align: top; }}
  th {{ background: #e8eef4; font-weight: 600; color: #0f2740; }}
  tr:nth-child(even) td {{ background: #f7fafc; }}
  ul, ol {{ margin: 0 0 10pt 16pt; padding: 0; }}
  li {{ margin-bottom: 5pt; }}
  .cover {{ page-break-after: always; text-align: center; padding-top: 45mm; }}
  .cover .brand {{ font-size: 13pt; letter-spacing: 2.5px; text-transform: uppercase; color: #2471a3; font-weight: 600; }}
  .cover .prog {{ font-size: 11pt; color: #52606d; margin-top: 4pt; }}
  .cover hr {{ width: 45%; margin: 26pt auto; border: 0; border-top: 3px solid #2471a3; }}
  .cover h1 {{ font-size: 25pt; line-height: 1.25; margin-bottom: 8pt; }}
  .cover .sub {{ font-size: 12pt; color: #33475b; margin-bottom: 40pt; }}
  .meta {{ display: inline-block; text-align: left; font-size: 10.5pt; }}
  .meta table {{ border: 0; }}
  .meta td {{ border: 0; padding: 3pt 10pt 3pt 0; background: transparent !important; }}
  .meta td:first-child {{ color: #52606d; }}
  .draft {{ background: #fff3cd; border: 1px solid #e0b100; padding: 8pt 10pt; margin-bottom: 14pt;
            font-size: 9.5pt; color: #6b5200; }}
  figure {{ margin: 10pt 0 16pt; page-break-inside: avoid; text-align: center; }}
  figure img {{ max-width: 100%; border: 1px solid #d5dee6; border-radius: 3px; }}
  figcaption {{ font-size: 9pt; color: #33475b; margin-top: 5pt; text-align: left; }}
  .note {{ color: #52606d; }}
  .ph {{ border: 2px dashed #9fb3c8; border-radius: 4px; padding: 26pt 12pt; color: #52606d;
         background: #f7fafc; font-size: 9pt; }}
  .kpi {{ display: flex; gap: 8pt; margin: 10pt 0 14pt; }}
  .kpi div {{ flex: 1; border: 1px solid #c9d4de; border-top: 3px solid #2471a3; padding: 7pt; text-align: center; }}
  .kpi .v {{ font-size: 15pt; font-weight: 700; color: #0f2740; }}
  .kpi .l {{ font-size: 8pt; color: #52606d; text-transform: uppercase; letter-spacing: 0.4px; }}
  .toc a {{ color: #16496b; text-decoration: none; }}
  .toc ol {{ margin-left: 18pt; }}
  .break {{ page-break-before: always; }}
  footer {{ display: none; }}
</style></head>
<body>

<section class="cover">
  <div class="brand">Devixo Solutions</div>
  <div class="prog">AI/ML Internship Program</div>
  <hr>
  <h1>Task 01<br>Python Programming, Data Analysis &amp; Visualization</h1>
  <div class="sub">Exploratory Data Analysis of 30 Security Features<br>from 11,055 Phishing and Legitimate Websites</div>
  <div class="meta"><table>
    <tr><td>Student Name</td><td><strong>Shahlal Jaffir</strong></td></tr>
    <tr><td>Roll Number / ID</td><td>—</td></tr>
    <tr><td>Internship Domain</td><td>AI/ML — Cybersecurity</td></tr>
    <tr><td>Program</td><td>Devixo Solutions AI/ML Internship</td></tr>
    <tr><td>Submission Date</td><td>22 November 2026</td></tr>
    <tr><td>Environment</td><td>Google Colab (Python 3)</td></tr>
  </table></div>
</section>

<section>
<h2>Contents</h2>
<ol class="toc">
  <li>Introduction</li>
  <li>Problem Statement</li>
  <li>Objective</li>
  <li>Dataset Name</li>
  <li>Dataset Source</li>
  <li>Dataset Description</li>
  <li>Dataset Size</li>
  <li>Features / Columns Description</li>
  <li>Methodology</li>
  <li>Data Loading</li>
  <li>Data Cleaning</li>
  <li>Exploratory Data Analysis</li>
  <li>Statistical Analysis</li>
  <li>Data Visualizations</li>
  <li>Code Screenshots</li>
  <li>Output Screenshots</li>
  <li>Graph Screenshots</li>
  <li>Major Findings</li>
  <li>At Least 10 Insights</li>
  <li>Challenges and Solutions</li>
  <li>Conclusion</li>
  <li>GitHub Repository Link</li>
  <li>References</li>
</ol>
</section>

<section>
{draft_banner}
<h2>1. Introduction</h2>
<p>Phishing remains one of the most common entry points for cyber attacks. Instead of attacking a network
directly, a phishing site impersonates a trusted brand and persuades a user to surrender credentials. Because
the attack surface is the web page itself, many phishing sites can be recognised from measurable properties of
their URL, domain and page structure — whether the URL uses a raw IP address instead of a domain name, whether
the SSL certificate is valid, or whether anchor links point outside the site.</p>
<p>This report documents a complete data analysis of a public dataset of 11,055 websites, each described by 30
such security features. The work covers loading, understanding, cleaning, exploratory analysis, descriptive
statistics, correlation analysis, ten visualizations and evidence-based conclusions. The analysis is performed
entirely in Python using Pandas, NumPy, Matplotlib and Seaborn inside Google Colab.</p>

<h2>2. Problem Statement</h2>
<p>Security teams receive far more suspicious URLs than they can inspect manually. Before any automated
detection model can be built, two questions must be answered from data: what does the data actually contain and
how trustworthy is it, and which measurable website properties differ meaningfully between phishing and
legitimate sites? Without this analysis, a model would be built on unverified assumptions.</p>

<h2>3. Objective</h2>
<ol>
  <li>Load the dataset with Pandas and inspect its structure, types and completeness.</li>
  <li>Classify every column by type and explain why the classification matters.</li>
  <li>Detect and handle missing values, duplicates, incorrect data types, unclear names and invalid values, with justification.</li>
  <li>Produce descriptive statistics — mean, median, mode, minimum, maximum, range, standard deviation, variance.</li>
  <li>Quantify relationships between features with a correlation matrix.</li>
  <li>Produce the ten required visualizations, each with labels and an interpretation.</li>
  <li>Extract at least ten insights supported by the actual numbers.</li>
  <li>Document the work reproducibly and publish it on GitHub.</li>
</ol>

<h2>4. Dataset Name</h2>
<p><strong>Phishing Websites</strong> (also distributed on Kaggle as
<em>“Phishing Website Dataset”</em> / <em>“Phishing Dataset UCI ML CSV”</em>).</p>

<h2>5. Dataset Source</h2>
<table>
<tr><th>Property</th><th>Value</th></tr>
<tr><td>Authors</td><td>Rami M. Mohammad, Lee McCluskey (University of Huddersfield)</td></tr>
<tr><td>Year</td><td>2012 (donated to UCI in 2015)</td></tr>
<tr><td>Original repository</td><td>UCI Machine Learning Repository, dataset ID 327</td></tr>
<tr><td>DOI</td><td>10.24432/C51W2X</td></tr>
<tr><td>Kaggle mirror</td><td>kaggle.com/datasets/akashkr/phishing-website-dataset</td></tr>
<tr><td>License</td><td>Creative Commons Attribution 4.0 International (CC BY 4.0)</td></tr>
<tr><td>Data origin</td><td>PhishTank archive, MillerSmiles archive, Google search operators</td></tr>
</table>

<h2>6. Dataset Description</h2>
<p>Each record describes one website. The 30 predictive features encode rule-based assessments of URL, domain
and page-level properties. The dataset uses a three-level ordinal encoding: −1 indicates a phishing-leaning
assessment, 0 a suspicious or inconclusive result, and 1 a legitimate-leaning assessment. The target column
<code>Result</code> is −1 for phishing and 1 for legitimate. The dataset is therefore a binary classification
problem, even though the individual features are ternary.</p>

<h2>7. Dataset Size</h2>
<div class="kpi">
  <div><div class="v">11,055</div><div class="l">Records</div></div>
  <div><div class="v">31</div><div class="l">Columns</div></div>
  <div><div class="v">30</div><div class="l">Features</div></div>
  <div><div class="v">782 KB</div><div class="l">File size</div></div>
  <div><div class="v">0</div><div class="l">Missing cells</div></div>
</div>
<p>Total cells: 342,705. After removing 5,206 duplicate rows the analysis dataset contains 5,849 records.</p>

<h2>8. Features / Columns Description</h2>
<table>
<tr><th style="width:26%">Column (renamed)</th><th style="width:24%">Original name</th><th>Meaning</th></tr>
{feature_rows}
<tr><td><code>Result</code> → <code>Class</code></td><td>Result</td><td>Target: −1 = phishing, 1 = legitimate</td></tr>
</table>

<h2>9. Methodology</h2>
<ol>
  <li><strong>Dataset selection</strong> — a Kaggle-hosted cybersecurity dataset with at least 500 rows and multiple numeric features, so that every required chart type is meaningful.</li>
  <li><strong>Data loading</strong> — Pandas <code>read_csv</code>, with an automatic fallback that downloads and parses the official UCI ARFF archive if the CSV is absent.</li>
  <li><strong>Data understanding</strong> — head, tail, random sample, <code>info()</code>, shape, dtypes, distinct-value counts.</li>
  <li><strong>Data cleaning</strong> — missing-value audit, duplicate removal, dtype narrowing to <code>int8</code>, column renaming, value-domain validation.</li>
  <li><strong>EDA and statistics</strong> — descriptive statistics, mean/median/mode/std interpretation, correlation ranking.</li>
  <li><strong>Visualization</strong> — the ten required chart types, each labelled and interpreted.</li>
  <li><strong>Insight extraction</strong> — twelve findings, each tied to a computed number.</li>
</ol>
<p>Every cleaning decision is justified in the notebook. Nothing was imputed, invented or silently dropped.</p>

<h2>10. Data Loading</h2>
<p>The notebook loads <code>data/phishing_dataset.csv</code>, a direct conversion of the official UCI
<code>Training Dataset.arff</code>. No value was modified: the conversion only rewrote the ARFF header as a CSV
header row and copied the data section verbatim. Verification after conversion confirmed 11,055 rows, 31
columns, zero empty cells and all values within {{−1, 0, 1}}.</p>

<h2>11. Data Cleaning</h2>
<h3>11.1 Missing values</h3>
<p>A per-column audit found <strong>0 missing cells out of 342,705</strong>. No imputation was applied, because
filling gaps that do not exist would fabricate observations and distort every statistic that follows.</p>
<h3>11.2 Duplicate records</h3>
<p><strong>5,206 exact duplicate rows (47.1%)</strong> were detected across 2,637 duplicate groups and removed,
leaving 5,849 records. The duplicates were not evenly distributed: 3,327 legitimate rows were duplicated versus
1,879 phishing rows, so removing them shifted the class balance from 44.31% / 55.69% to 51.62% / 48.38%.
Verification after removal confirmed zero remaining duplicates.</p>
<h3>11.3 Data types</h3>
<p>All 31 columns were already integers — no numbers stored as text and no dates stored as strings (the dataset
contains no date column). The dtype was narrowed from <code>int64</code> to <code>int8</code>, which stores the
values exactly while using one eighth of the memory.</p>
<h3>11.4 Column renaming</h3>
<p>Three original names contained spelling errors — <code>Shortining_Service</code>,
<code>Domain_registeration_length</code> and <code>popUpWidnow</code> — and several abbreviations were unclear
(<code>SFH</code>). All 31 columns were renamed to clear, consistent, self-describing names; the full mapping is
in Section 8.</p>
<h3>11.5 Invalid values</h3>
<p>A value-domain check confirmed every feature lies strictly within {{−1, 0, 1}} and the target within {{−1, 1}}.
No out-of-range, negative or impossible values were found, so nothing required correction. One structural
observation is recorded: the target is binary — the “suspicious” (0) class mentioned in some descriptions of
this dataset is absent.</p>

<h2>12. Exploratory Data Analysis</h2>
<p>After cleaning, the dataset holds 3,019 phishing sites (51.62%) and 2,830 legitimate sites (48.38%). The
class distribution is therefore close to balanced. Three observations shaped the rest of the analysis: the
features are ternary rather than continuous; several features are dominated by a single value (RightClick_Disabled
is 1 for 95.1% of sites, Uses_Iframe 89.3%, Has_Prefix_Suffix 88.0%, Uses_Redirect 86.8%); and the strongest
signals are concentrated in a small subset of features.</p>
<p>Because every feature is a three-level code, a derived variable — <strong>Risk_Signals</strong>, the number of
features in a row coded −1 — was created for distribution plots. It is explicitly labelled as derived wherever it
appears.</p>

<h2>13. Statistical Analysis</h2>
<p>For each feature the notebook computes mean, median, mode, minimum, maximum, range, standard deviation and
variance. The mean follows the standard formula:</p>
<p style="text-align:center"><code>mean = Σx / n</code></p>
<p>For example, SSL_State sums to a mean of 0.25 overall, −0.47 for phishing and 0.81 for legitimate sites: the
sign difference is the signal, and because the codes are ordinal the mean is read as net direction of evidence
rather than as a physical quantity.</p>
<p>Median and mode add robustness. For Risk_Signals the mean (9.34) sits slightly above the median (9),
indicating a mild right skew, so the median is the more honest “typical” value. The mode exposes near-constant
features, which have little room to discriminate.</p>
<p>Standard deviation measures spread. Domain_Age has the maximum possible value (1.00, split 2,862 / 2,987
between its two observed codes), while Uses_Redirect has the smallest (≈0.34). Crucially, high spread is not the
same as predictive power — Domain_Age correlates with the class at only r ≈ 0.06.</p>
<p>Correlation analysis produced the ranking below (Pearson r against the class label):</p>
<table>
<tr><th>Feature</th><th>r</th><th>Interpretation</th></tr>
<tr><td>SSL_State</td><td>+0.69</td><td>Strongest single signal; valid certificates indicate legitimacy</td></tr>
<tr><td>External_Anchor_URL</td><td>+0.68</td><td>Off-site anchor links strongly indicate phishing</td></tr>
<tr><td>Has_Prefix_Suffix</td><td>+0.38</td><td>Hyphen in domain; common in phishing but also in legitimate sites</td></tr>
<tr><td>Has_Sub_Domain</td><td>+0.30</td><td>Deep sub-domain nesting leans phishing</td></tr>
<tr><td>Web_Traffic</td><td>+0.28</td><td>Popular sites are usually legitimate</td></tr>
<tr><td>Server_Form_Handler</td><td>+0.28</td><td>Blank or foreign form handlers lean phishing</td></tr>
<tr><td>External_Links_In_Tags</td><td>+0.24</td><td>Off-site links in meta/script tags</td></tr>
<tr><td>External_Request_URL</td><td>+0.24</td><td>External resource requests</td></tr>
<tr><td>Domain_Registration_Length</td><td>−0.22</td><td>Short registration periods lean phishing</td></tr>
<tr><td>Google_Indexed / In_Statistical_Report / Has_IP_Address</td><td>+0.11 … +0.12</td><td>Weak</td></tr>
<tr><td>Remaining 18 features</td><td>|r| &lt; 0.10</td><td>Little or no linear signal</td></tr>
</table>

<h2 class="break">14. Data Visualizations</h2>
<p>The ten required chart types follow. Each has a title, labelled axes, an appropriate figure size, and an
interpretation of what it shows and why it matters.</p>
{figs}

<h2 class="break">15. Code Screenshots</h2>
{code_shots}

<h2>16. Output Screenshots</h2>
{out_shots}

<h2>17. Graph Screenshots</h2>
{graph_shots}

<h2>18. Major Findings</h2>
<ul>
  <li><strong>Data quality dominated the work.</strong> Almost half the file was duplicated, and the duplicates were biased toward the legitimate class — a fact that would have silently distorted every downstream statistic.</li>
  <li><strong>Two features carry most of the signal.</strong> SSL state (r = 0.69) and external anchor URLs (r = 0.68) separate the classes far better than anything else.</li>
  <li><strong>Feature selection beats aggregation.</strong> A count of all failed checks separates the classes only weakly (10.50 vs 8.10, heavy overlap), while the two strongest individual features separate them strongly.</li>
  <li><strong>Many features are noise.</strong> 18 of 30 features correlate below |r| = 0.10, and 12 below 0.05.</li>
  <li><strong>Variance is not predictive power.</strong> The most variable feature in the dataset is among the least informative.</li>
</ul>

<h2>19. At Least 10 Insights</h2>
<ol>{insights_html}</ol>

<h2>20. Challenges and Solutions</h2>
<table>
<tr><th style="width:38%">Challenge</th><th>Solution</th></tr>
<tr><td>Almost half the records were exact duplicates, which would inflate frequencies and bias class proportions.</td>
    <td>Counted duplicates, removed them, verified zero remained, and compared class balance before and after to quantify the bias.</td></tr>
<tr><td>Every feature is a three-level code, so histograms, scatter plots and violin plots have very little visual resolution.</td>
    <td>Created a documented derived variable (Risk_Signals) and used jitter on scatter plots so the charts describe something meaningful without inventing data.</td></tr>
<tr><td>The original dataset has no missing values, yet the task requires missing-value handling.</td>
    <td>Performed the full audit, reported 0 missing cells, and justified explicitly why imputation was not applied rather than inventing gaps.</td></tr>
<tr><td>Three column names contained spelling errors and several abbreviations were ambiguous.</td>
    <td>Renamed all 31 columns and documented the old → new mapping.</td></tr>
<tr><td>A naive “count of failed checks” initially appeared to separate the classes well.</td>
    <td>Measured the distributions properly and corrected the claim: the overlap is substantial, which changed the conclusion and strengthened the argument for feature selection.</td></tr>
</table>

<h2>21. Conclusion</h2>
<p>This analysis examined the UCI Phishing Websites dataset — 11,055 websites described by 30 integer-coded
security features. The first substantive finding was a data-quality one: 47.1% of the records were exact
duplicates, and removing them materially changed the class balance, from 44.31% / 55.69% to 51.62% / 48.38%.
The dataset contained no missing values and no out-of-range codes, so the honest cleaning decisions were to
remove duplicates, narrow the integer types, correct three misspelled column names, and document explicitly that
no imputation was required rather than applying one for appearance.</p>
<p>Statistically, phishing detection from URL and page structure is highly feasible: SSL state (r = 0.69) and
external anchor URLs (r = 0.68) are strong, largely independent predictors, followed by domain-structure
features at r ≈ 0.24–0.38. At the same time, 18 of the 30 features correlate below |r| = 0.10, and high variance
alone — as in Domain_Age, with the maximum possible standard deviation but r ≈ 0.06 — does not make a feature
predictive. A naive count of failed checks separated the classes only weakly, which underlines that selecting
the right features matters far more than aggregating many of them. The practical value is direct: these are
cheap, automatable checks that a browser, mail gateway or SOC triage pipeline can compute for any URL, and the
seven features with |r| ≥ 0.24 form a natural candidate set for a baseline classifier in the next stage.</p>
<p><strong>What was learned:</strong> most of the effort in a data project goes into verifying and cleaning the
data before analysis, statistical summaries must be interpreted in the context of the encoding, and correlation
alone is not evidence of predictive value.</p>

<h2>22. GitHub Repository Link</h2>
<p>Repository: <code>[GITHUB_REPOSITORY_URL]</code></p>
<p>The repository contains the Jupyter notebook, the dataset, the generated visualization images, this report and
a README describing the project, its workflow and how to run it.</p>

<h2>23. References</h2>
<ol>
  <li>Mohammad, R. M., &amp; McCluskey, L. (2012). <em>Phishing Websites</em> [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C51W2X (CC BY 4.0)</li>
  <li>Mohammad, R. M., Thabtah, F., &amp; McCluskey, L. (2012). <em>An assessment of features related to phishing websites using an automated technique.</em> ICITST 2012.</li>
  <li>UCI Machine Learning Repository — https://archive.ics.uci.edu/dataset/327/phishing+websites</li>
  <li>Kaggle mirror — https://www.kaggle.com/datasets/akashkr/phishing-website-dataset</li>
  <li>Pandas documentation — https://pandas.pydata.org/docs/</li>
  <li>NumPy documentation — https://numpy.org/doc/</li>
  <li>Matplotlib documentation — https://matplotlib.org/stable/</li>
  <li>Seaborn documentation — https://seaborn.pydata.org/</li>
  <li>OWASP Top 10 (2021), A07: Identification and Authentication Failures — https://owasp.org/Top10/</li>
</ol>
</section>
</body></html>"""


def main():
    draft = "--final" not in sys.argv
    html_path = os.path.join(REPORTS, "_report_build.html")
    pdf_name = "DRAFT_Shahlal_Jaffir_Task1.pdf" if draft else "Shahlal_Jaffir_Task1.pdf"
    pdf_path = os.path.join(REPORTS, pdf_name)

    open(html_path, "w", encoding="utf-8").write(build_html(draft))

    if not os.path.exists(CHROME):
        print("Chrome not found at", CHROME)
        return 1

    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
        "--virtual-time-budget=6000", html_path.replace("\\", "/").join(["file:///", ""]),
    ], check=False, capture_output=True)

    if os.path.exists(pdf_path):
        print(f"PDF: {pdf_path}  ({os.path.getsize(pdf_path) / 1024:.0f} KB)")
        print(f"HTML: {html_path}")
    else:
        print("PDF generation failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
