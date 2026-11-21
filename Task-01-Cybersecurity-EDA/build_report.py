"""Build the Task 01 PDF report: styled HTML -> headless Chrome -> PDF.

If a visualization PNG is missing, a clearly labeled placeholder box is inserted
so the draft is never mistaken for a finished submission.
"""
import base64
import html
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VIS = os.path.join(ROOT, "visualizations")
REPORTS = os.path.join(ROOT, "reports")
SHOTS = os.path.join(ROOT, "screenshots")
os.makedirs(REPORTS, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

FIGURES = [
    ("18_01_histogram_risk_signals", "Histogram — distribution of phishing-leaning signals per website",
     "Phishing sites sit further right, with a median of 10 failed checks against 7 for legitimate ones. "
     "The two distributions still overlap a lot, so the total count on its own is only a weak-to-moderate separator."),
    ("18_02_bar_top_correlations", "Bar chart — absolute correlation of each feature with the class label",
     "SSL state (0.71) and external anchor URLs (0.69) are far ahead of everything else. After those two the "
     "values drop to 0.35 and below."),
    ("18_03_pie_class_balance", "Pie chart — class balance (Full dataset)",
     "The full dataset of 11,055 records is composed of 4,898 phishing sites (44.31%) and 6,157 legitimate ones (55.69%)."),
    ("18_04_scatter_ssl_vs_anchor", "Scatter plot — SSL state vs external anchor URL",
     "The corner with an invalid certificate and off-site anchors is almost entirely phishing. The opposite corner, "
     "valid certificate and same-site anchors, is almost entirely legitimate."),
    ("18_05_line_threshold_rates", "Line chart — share of each class at or above a risk-signal threshold",
     "The gap peaks at a threshold of 8, where 82.7% of phishing sites qualify against 42.0% of legitimate ones. "
     "Past 12 the lines converge, which is the usual recall and false-positive trade-off."),
    ("18_06_box_risk_signals", "Box plot — risk signals by class",
     "The medians differ, 10 against 7, but the interquartile ranges overlap (8–12 and 5–10). Phishing also has "
     "the longer upper tail, reaching 25."),
    ("18_07_heatmap_correlations", "Correlation heatmap — twelve strongest features and the class label",
     "Most of the cells between two features are pale. The strong predictors are not simply restating each other, "
     "which is what makes them worth keeping."),
    ("18_08_countplot_ssl_state", "Count plot — websites per SSL state, split by class",
     "An invalid SSL state appears on 62.3% of phishing sites and on only 8.2% of legitimate ones."),
    ("18_09_pairplot_features", "Pair plot — strongest features and the derived risk score",
     "SSL state and external anchor URL split the two classes more cleanly than the combined risk score does."),
    ("18_10_violin_risk_signals", "Violin plot — density of risk signals by class",
     "The phishing density peaks at 9 failed checks, the legitimate density at 6."),
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
    ("Repeated feature vectors account for 47.1% of the data.",
     "Of 11,055 rows, 5,206 repeat a feature vector already present. Because there are no unique website identifiers, "
     "the primary analysis uses the full 11,055-row dataset to avoid assuming these are redundant websites. "
     "Deduplication is used only for sensitivity analysis."),
    ("Class distribution is moderately imbalanced.",
     "The full dataset contains 4,898 phishing sites (44.31%) and 6,157 legitimate ones (55.69%). "
     "Sensitivity analysis on the deduplicated subset (5,849 rows) shifts this to 51.62% / 48.38%."),
    ("There is nothing missing to fill in.",
     "All 342,705 cells hold a value. Any imputation here would have meant inventing data, so the right move was to "
     "run the audit, report zero, and leave the file alone."),
    ("A valid certificate is the strongest single sign of a real site (r = 0.71).",
     "62.3% of phishing sites in the full dataset have an invalid or missing certificate, compared with 8.2% "
     "of legitimate sites. On the other side, 91.4% of legitimate sites present a valid one."),
    ("Links that point off-site are a very strong phishing sign (r = 0.69).",
     "66.3% of phishing sites send anchor links outside their own domain, against 0.6% of legitimate sites. "
     "This feature provides a very clean separation between the two classes."),
    ("A hyphen in the domain is common, which is exactly the problem.",
     "Every phishing site in the sample is coded −1 for Has_Prefix_Suffix, but so are 76.2% of legitimate sites. "
     "With r = 0.35 the feature describes most of the data and separates very little of it."),
    ("Traffic rank carries real signal.",
     "70.2% of legitimate sites have positive web traffic, against 30.8% of phishing sites (r = 0.35). Popularity "
     "is hard to fake quickly, which fits the rest of the pattern."),
    ("Some columns tell you nothing.",
     "RightClick_Disabled is coded 1 for 95.4% of phishing and 95.9% of legitimate sites. PopUp_Window (r = +0.00), "
     "Uses_Iframe (r = −0.00) and Favicon_From_Domain (r = −0.00) are no better. Overall, 18 of the 30 features "
     "sit below |r| = 0.10, and 11 of those below 0.05."),
    ("High variation does not imply predictive power.",
     "Domain_Age has a standard deviation of 1.00 in the full file, split 5,189 / 5,866 between its two observed "
     "codes. However, its correlation with the class is only r ≈ 0.12."),
    ("Counting every failed check is a weaker test than it looks.",
     "Phishing sites average 10.41 risk signals and legitimate sites 7.71, a gap of 2.7. More tellingly, "
     "many sites from both classes overlap in the mid-range of signal counts."),
    ("Recently registered domains lean phishing.",
     "Domain_Registration_Length correlates negatively (r = −0.23). Phishing domains average −0.10 on this feature, "
     "legitimate domains −0.53."),
    ("The target has two values, not three.",
     "Result contains only −1 and 1. Some descriptions of this dataset mention a 0 class for suspicious sites, but "
     "this file has none."),
]


def img_block(name, caption, note):
    path = os.path.join(VIS, f"{name}.png")
    if os.path.exists(path):
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        body = f'<img src="data:image/png;base64,{b64}" alt="{html.escape(caption)}">'
        status = ""
    else:
        body = ('<div class="ph"><strong>CHART PENDING</strong><br>'
                f'Generate <code>visualizations/{name}.png</code> by running the notebook.</div>')
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
        shot_block("Data cleaning — duplicate records", "02_cleaning_duplicates.png", "Screenshot of the duplicate analysis cell and output"),
        shot_block("Missing values and dtypes", "03_missing_dtypes.png", "Screenshot of the missing-value and dtype cells"),
        shot_block("Descriptive statistics", "04_statistics.png", "Screenshot of the statistics table"),
        shot_block("Correlation analysis", "05_correlation.png", "Screenshot of the correlation ranking"),
    ])
    out_shots = "\n".join([
        shot_block("Notebook output — class balance, full vs deduplicated", "06_output_balance.png", "Screenshot of the class balance output"),
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
    <tr><td>Internship Domain</td><td>AI/ML — Cybersecurity</td></tr>
    <tr><td>Program</td><td>Devixo Solutions AI/ML Internship</td></tr>
    <tr><td>Submission Date</td><td>22 November 2026</td></tr>
    <tr><td>Environment</td><td>Jupyter Notebook (Python 3)</td></tr>
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
</ol>
</section>

<section>
{draft_banner}
<h2>1. Introduction</h2>
<p>Most phishing attacks do not break into a network. They convince someone to type a password into a page that
looks like the real thing, and the page itself is usually where the evidence sits. A fake login page often uses
a raw IP address instead of a domain name, carries a certificate that does not check out, or links away to hosts
that have nothing to do with the brand it imitates. Each of those is something a program can measure.</p>
<p>This report is my analysis of a public dataset of 11,055 websites, each described by 30 of those measurable
properties. I loaded the file, checked what was actually in it, cleaned it, and then worked through descriptive
statistics, correlations and ten charts before writing down what the numbers showed. Everything runs in Python
with Pandas, NumPy, Matplotlib and Seaborn, in a Jupyter notebook.</p>

<h2>2. Problem Statement</h2>
<p>A security team receives far more suspicious URLs in a day than it can open by hand. Before anything
automatic is built on top of that, two things are worth knowing. First, what is actually in the data, and can it
be trusted. Second, which of the measured properties really differ between a phishing site and a legitimate one.
Skip those questions and the model inherits whatever assumptions were made about the file.</p>

<h2>3. Objective</h2>
<ol>
  <li>Load the dataset with Pandas and inspect its structure, types and completeness.</li>
  <li>Classify every column by type and explain why the classification matters.</li>
  <li>Detect and handle missing values, duplicates, incorrect data types, unclear names and invalid values, with justification.</li>
  <li>Produce descriptive statistics: mean, median, mode, minimum, maximum, range, standard deviation and variance.</li>
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
<p>Each row is one website. The 30 features are not raw measurements; they are rule-based judgments about the
URL, the domain and the page. Every one is coded on three levels: −1 leans phishing, 0 means suspicious or
inconclusive, and 1 leans legitimate. The target column, <code>Result</code>, is −1 for phishing and 1 for
legitimate, so the prediction task is binary even though the inputs are not.</p>

<h2>7. Dataset Size</h2>
<div class="kpi">
  <div><div class="v">11,055</div><div class="l">Records</div></div>
  <div><div class="v">31</div><div class="l">Columns</div></div>
  <div><div class="v">30</div><div class="l">Features</div></div>
  <div><div class="v">782 KB</div><div class="l">File size</div></div>
  <div><div class="v">0</div><div class="l">Missing cells</div></div>
</div>
<p>That comes to 342,705 cells in total. 5,206 of the rows (47.1%) repeat a feature vector that already appears in
the file; the primary analysis keeps all 11,055 records, and a deduplicated copy of 5,849 rows is used only as a
sensitivity check (section 11.2).</p>

<h2>8. Features / Columns Description</h2>
<table>
<tr><th style="width:26%">Column (renamed)</th><th style="width:24%">Original name</th><th>Meaning</th></tr>
{feature_rows}
<tr><td><code>Result</code> → <code>Class</code></td><td>Result</td><td>Target: −1 = phishing, 1 = legitimate</td></tr>
</table>

<h2>9. Methodology</h2>
<ol>
  <li><strong>Dataset selection.</strong> A Kaggle-hosted cybersecurity dataset with at least 500 rows and several numeric features, so that every required chart type has something to show.</li>
  <li><strong>Data loading.</strong> Pandas <code>read_csv</code>, with a fallback that downloads and parses the official UCI ARFF archive if the CSV is missing.</li>
  <li><strong>Data understanding.</strong> Head, tail, a random sample, <code>info()</code>, shape, dtypes and distinct-value counts.</li>
  <li><strong>Data cleaning.</strong> Missing-value audit, duplicate-record analysis (full file kept as primary, deduplicated copy as sensitivity), dtype narrowing to <code>int8</code>, column renaming and a value-domain check.</li>
  <li><strong>EDA and statistics.</strong> Descriptive statistics, interpretation of mean, median, mode and standard deviation, then a correlation ranking.</li>
  <li><strong>Visualization.</strong> The ten required chart types, each labeled and interpreted.</li>
  <li><strong>Insight extraction.</strong> Twelve findings, each tied to a number the notebook actually computed.</li>
</ol>
<p>Every cleaning step is justified in the notebook itself. I did not impute anything, invent values or quietly drop rows.</p>

<h2>10. Data Loading</h2>
<p>The notebook reads <code>data/phishing_dataset.csv</code>, which is a straight conversion of the official UCI
<code>Training Dataset.arff</code>. Only the header changed: the ARFF attribute lines became a single CSV header
row and the data block was copied as it was. After converting, I read the file back and checked the shape (11,055
rows, 31 columns), the empty cells (none) and the value range (everything inside {{−1, 0, 1}}).</p>

<h2>11. Data Cleaning</h2>
<h3>11.1 Missing values</h3>
<p>I checked every column separately and found no missing cells at all: 0 out of 342,705. Nothing was imputed.
Filling gaps that are not there would mean making up observations, and every statistic after that point would
rest on invented values.</p>
<h3>11.2 Duplicate records</h3>
<p>This turned out to be the biggest question in the file. 5,206 rows (47.1%) repeat a feature vector that already
appears somewhere else, spread over 2,637 repeated groups and leaving 5,849 distinct vectors. The dataset carries
no website identifier, so a repeated row might be the same site recorded twice or a different site with identical
measurements — there is no way to tell from the file alone. The repeats are also not spread evenly: 3,327 of them
are legitimate rows and only 1,879 phishing, so dropping them would move the class split from 44.31% / 55.69% to
51.62% / 48.38%. Because of both facts, the primary analysis keeps all 11,055 records and the deduplicated copy
(5,849 rows) is reported only as a labelled sensitivity check wherever it appears.</p>
<h3>11.3 Data types</h3>
<p>Every column was already an integer. There were no numbers stored as text and no dates stored as strings,
since the dataset has no date column at all. I narrowed the dtype from <code>int64</code> to <code>int8</code>.
The values fit, and the array now takes an eighth of the memory it did before.</p>
<h3>11.4 Column renaming</h3>
<p>Three of the original names were misspelled: <code>Shortining_Service</code>,
<code>Domain_registeration_length</code> and <code>popUpWidnow</code>. Others were abbreviations that mean
nothing without the source paper, <code>SFH</code> for example. I renamed all 31 columns to names that describe
what they hold. Section 8 lists the old name beside each new one.</p>
<h3>11.5 Invalid values</h3>
<p>I checked the range of every column. Each feature stays inside {{−1, 0, 1}} and the target inside {{−1, 1}},
so there was nothing out of range to correct. One structural point is worth recording: the target is binary.
Some descriptions of this dataset mention a “suspicious” class coded 0, but it does not appear in this file.</p>

<h2>12. Exploratory Data Analysis</h2>
<p>The full dataset has 4,898 phishing sites (44.31%) against 6,157 legitimate ones (55.69%) — mild enough that no
resampling was needed. Two properties of the data shaped the rest of the work. The features are
ternary codes, not continuous measurements. And a lot of them barely move: RightClick_Disabled is 1 for 95.7% of
sites, Uses_Iframe for 90.8%, Has_Prefix_Suffix for −1 86.7% and Uses_Redirect for 0 88.4%.</p>
<p>A three-level code gives a histogram or a violin plot almost nothing to show, so for the distribution charts I
built one extra column. <strong>Risk_Signals</strong> counts how many features in a row are coded −1. It is a
derived variable and is labeled that way everywhere it appears, because it is not part of the original
dataset.</p>

<h2>13. Statistical Analysis</h2>
<p>For every feature the notebook reports mean, median, mode, minimum, maximum, range, standard deviation and
variance, using the usual formula for the mean:</p>
<p style="text-align:center"><code>mean = Σx / n</code></p>
<p>SSL_State is a good example. Its mean is 0.25 across the whole dataset, −0.48 among phishing sites and 0.83
among legitimate ones. The sign carries the meaning here. Because the codes are ordinal, the mean is a net
direction of evidence rather than a quantity with units.</p>
<p>Median and mode guard against the mean being dragged around by a lopsided distribution. Risk_Signals has a mean
of 8.90 and a median of 8, so it leans slightly to the right and the median is the better description of a typical
row. The mode is useful for the opposite reason: where one value dominates, the feature has almost no room left to
separate anything.</p>
<p>Standard deviation shows spread. Domain_Age has the largest possible value, 1.00, split 5,189 / 5,866 across
its two observed codes, while Uses_Redirect has the smallest at about 0.32. Spread on its own says nothing about
usefulness. Domain_Age is the most variable column in the file and correlates with the class at only r ≈ 0.12.</p>
<p>The correlation ranking against the class label (Pearson r) came out as follows.</p>
<table>
<tr><th>Feature</th><th>r</th><th>Interpretation</th></tr>
<tr><td>SSL_State</td><td>+0.71</td><td>Strongest single signal; valid certificates indicate legitimacy</td></tr>
<tr><td>External_Anchor_URL</td><td>+0.69</td><td>Off-site anchor links strongly indicate phishing</td></tr>
<tr><td>Has_Prefix_Suffix</td><td>+0.35</td><td>Hyphen in domain; common in phishing but also in legitimate sites</td></tr>
<tr><td>Web_Traffic</td><td>+0.35</td><td>Popular sites are usually legitimate</td></tr>
<tr><td>Has_Sub_Domain</td><td>+0.30</td><td>Deep sub-domain nesting leans phishing</td></tr>
<tr><td>External_Request_URL</td><td>+0.25</td><td>External resource requests</td></tr>
<tr><td>External_Links_In_Tags</td><td>+0.25</td><td>Off-site links in meta/script tags</td></tr>
<tr><td>Domain_Registration_Length</td><td>−0.23</td><td>Short registration periods lean phishing</td></tr>
<tr><td>Server_Form_Handler</td><td>+0.22</td><td>Blank or foreign form handlers lean phishing</td></tr>
<tr><td>Google_Indexed / In_Statistical_Report / Has_IP_Address</td><td>+0.08 … +0.13</td><td>Weak</td></tr>
<tr><td>Remaining 18 features</td><td>|r| &lt; 0.10</td><td>Little or no linear signal</td></tr>
</table>

<h2 class="break">14. Data Visualizations</h2>
<p>The ten required chart types follow, each with a title, labeled axes and a note on what the chart shows.</p>
{figs}

<h2 class="break">15. Code Screenshots</h2>
{code_shots}

<h2>16. Output Screenshots</h2>
{out_shots}

<h2>17. Graph Screenshots</h2>
{graph_shots}

<h2>18. Major Findings</h2>
<ul>
  <li><strong>Almost half the records repeat a feature vector, and that is a caution rather than a fix.</strong> 47.1% of the rows repeat one already present, mostly legitimate ones. With no website identifiers we cannot call them duplicate sites, so the primary analysis keeps all 11,055 records and the deduplicated view appears only as a sensitivity check.</li>
  <li><strong>Two features do most of the work.</strong> SSL state (r = 0.71) and external anchor URLs (r = 0.69) separate the classes better than anything else in the file.</li>
  <li><strong>Picking features beats adding them up.</strong> Counting every failed check gives 10.41 against 7.71 with a large overlap, while the two strongest columns on their own separate them much better.</li>
  <li><strong>A lot of the columns are noise.</strong> 18 of the 30 features sit below |r| = 0.10, and 11 of those below 0.05.</li>
  <li><strong>Variance is not the same as usefulness.</strong> The most variable column in the file is one of the least informative.</li>
</ul>

<h2>19. At Least 10 Insights</h2>
<ol>{insights_html}</ol>

<h2>20. Challenges and Solutions</h2>
<table>
<tr><th style="width:38%">Challenge</th><th>Solution</th></tr>
<tr><td>Almost half the records repeat a feature vector, and it is unclear whether they are the same website twice.</td>
    <td>Counted and characterised the repeats, kept the full 11,055 rows for the primary analysis, and reported the deduplicated split (51.62% / 48.38%) beside the original (44.31% / 55.69%) so the effect of the choice is visible rather than assumed.</td></tr>
<tr><td>Every feature is a three-level code, so histograms, scatter plots and violin plots have very little visual resolution.</td>
    <td>Built a documented derived variable (Risk_Signals) and added jitter to the scatter plots, so the charts show something readable without inventing data.</td></tr>
<tr><td>The original dataset has no missing values, yet the task requires missing-value handling.</td>
    <td>Ran the full audit, reported 0 missing cells, and explained why imputation was not applied instead of creating gaps to fill.</td></tr>
<tr><td>Three column names contained spelling errors and several abbreviations were ambiguous.</td>
    <td>Renamed all 31 columns and recorded the old name beside each new one.</td></tr>
<tr><td>A simple count of failed checks looked like it separated the classes well.</td>
    <td>Measured the distributions properly and corrected the claim. The overlap turned out to be substantial, which changed the conclusion and made the case for feature selection stronger.</td></tr>
</table>

<h2>21. Conclusion</h2>
<p>This analysis looked at the UCI Phishing Websites dataset: 11,055 websites described by 30 integer-coded
security features. The first real finding was about the data rather than the websites. 47.1% of the records repeat
a feature vector that already appears in the file, and because the dataset carries no website identifier there was
no way to prove they are the same site twice. The primary analysis therefore keeps all 11,055 records and reports
44.31% phishing / 55.69% legitimate; the deduplicated copy (5,849 rows) shifts that to 51.62% / 48.38% and is
shown only as a sensitivity check. There were no missing values and no out-of-range codes, so the honest cleaning
steps were to narrow the integer types, fix three misspelled column names, and say plainly that no imputation was
needed. Adding one for appearance would have been worse than leaving it out.</p>
<p>On the statistics, phishing detection from URL and page structure looks very feasible. SSL state (r = 0.71) and
external anchor URLs (r = 0.69) are strong and largely independent of each other, and the domain-structure features
follow at r ≈ 0.22–0.35. The other side of that result matters just as much: 18 of the 30 features sit below
|r| = 0.10, and a large standard deviation on its own, as with Domain_Age at the maximum possible value but
r ≈ 0.12, does not make a column predictive. Counting every failed check separated the classes only moderately
(means 10.41 versus 7.71, with heavy overlap), which
is the clearest argument in this report for choosing features carefully instead of adding them up. In practice
these checks are cheap to compute. A browser, a mail gateway or a SOC triage queue could run them on any URL, and
the seven features with |r| ≥ 0.24 are a sensible starting set for a baseline classifier in the next stage.</p>
<p><strong>What I took from the work:</strong> most of the time in a data project goes into checking and cleaning
before any analysis happens, summary statistics have to be read in the context of how the values are coded, and a
correlation is not evidence of predictive value.</p>

<h2>22. GitHub Repository Link</h2>
<p>Repository: <code>https://github.com/shahlal07/devixo-task-1</code></p>
<p>The repository holds the notebook, the dataset, the visualization images, this report and a README that
explains the workflow and how to run it.</p>
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
