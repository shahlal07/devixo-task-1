# Dataset Documentation: Phishing Websites

This dataset contains 11,055 websites described by 30 security features.

## Repeated Feature Vectors

Analysis reveals that 5,206 rows (47.1%) represent a feature vector already present elsewhere in the file. 

**Scientific Interpretation:**
The dataset does not provide unique website identifiers. Consequently, we cannot determine if these repeated rows represent the same physical website recorded multiple times or different websites that happen to share identical measurable security features.

- **Primary Methodology:** We retain all 11,055 records for primary analysis to avoid making assumptions about data redundancy.
- **Sensitivity Analysis:** A deduplicated subset of 5,849 records is generated during the cleaning process and used exclusively for sensitivity analysis to observe how class proportions shift (from 44.31%/55.69% to 51.62%/48.38%).
