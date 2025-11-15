# 🏦 Financial Risk Mitigation & Customer Retention: A Power BI Churn Analysis

## Project Overview

This project delivers a comprehensive, **3-page interactive dashboard** built in Power BI, designed to help a financial institution understand, quantify, and proactively reduce customer attrition (churn). Using a granular customer data snapshot, the dashboard moves stakeholders from a simple metric (**Churn Rate**) to **actionable intervention strategies** by identifying high-risk segments and individuals.

| Metric | Business Question Answered |
| :--- | :--- |
| **\[Churn Rate]** | *What percentage of our customers are leaving?* |
| **\[Total Lost Balance]** | *What is the immediate financial cost of churn?* |
| **`Churn Risk Score`** | *Which specific customers are most likely to leave next?* |

-----

## 💾 Data Source & Preparation

The analysis is based on a snapshot of customer demographic and financial data from a multinational bank.

  * **Source File:** `Churn_Modelling.csv` (10,000 customer records)
  * **Technology:** Power BI Desktop (with underlying transformations performed in Power Query/M and DAX).

### Data Transformation Steps:

1.  **Irrelevant Column Removal:** `RowNumber`, `CustomerId`, and `Surname` were removed to focus the model on analytical variables.
2.  **Recoding:** Binary columns (`Exited`, `IsActiveMember`, `HasCrCard`) were converted from **0/1** integers to descriptive text (**"Retained"/"Churned"**, **"Active"/"Inactive"**) for clarity in visualizations.
3.  **Feature Engineering (Grouping):** New columns were created to improve segmentation in visuals:
      * **`Age Group`** (e.g., 18-30, 31-45, 46-60, 60+)
      * **`Tenure Group`** (e.g., 0-1 Year, 2-4 Years, 5-7 Years, 8+ Years)

-----

## ⚙️ Key DAX Modeling & Risk Scoring

The project relies on two core modeling elements for its actionable insights.

### 1\. Core Financial Measures

All rates and financial metrics are calculated using these central measures, stored in the **`_Measures`** table.

  * **\[Churn Rate]:** `DIVIDE([Churned Customers], [Total Customers])`
  * **\[Total Lost Balance]:** `CALCULATE(SUM('Table'[Balance]), 'Table'[Exited] = "Churned")`

### 2\. Churn Risk Score (Calculated Column)

A **weighted risk score** was engineered using a DAX calculated column to identify customers at the highest risk of attrition based on key known drivers. This score is used to prioritize intervention efforts on **Page 3**.

$$\text{Risk Score} = (0.4 \times \text{Low Tenure}) + (0.3 \times \text{Low Product Count}) + (0.2 \times \text{Inactive Member}) + (0.1 \times \text{High Balance})$$

**DAX Implementation:**

```dax
Churn Risk Score = 
VAR TenureRisk = IF('Table'[Tenure] < 3, 0.4, 0)
VAR ProductRisk = IF('Table'[NumOfProducts] = 1, 0.3, 0)
VAR InactiveRisk = IF('Table'[IsActiveMember] = 0, 0.2, 0) // Note: Checks for the integer 0
VAR HighBalanceRisk = IF('Table'[Balance] > 120000, 0.1, 0)
RETURN TenureRisk + ProductRisk + InactiveRisk + HighBalanceRisk
```

-----

## 🖥️ Report Structure and Insights (3 Pages)

### Page 1: Executive Summary & Financial Impact

  * **Goal:** Quantify the problem and flag top-level risks.
  * **Key Visual:** **Map Visual** shows Churn Rate by **Geography**.
  * **Key Insight:** Identifies which country (e.g., Germany) requires immediate, localized strategy changes due to having a disproportionately high churn rate despite lower customer volume.

### Page 2: Root Cause Analysis & Segmentation

  * **Goal:** Diagnose *who* is leaving and *why*, by behavioral and demographic segments.
  * **Key Visuals:** Clustered Bar Charts using the **`Age Group`** and **`Tenure Group`** columns.
  * **Actionable Insight:** The analysis reveals that the **'46-60' Age Group** and customers with **only 1 product** are the most critical segments for proactive retention campaigns. The **Key Influencers** visual confirms these factors are the strongest predictors of churn.

### Page 3: Intervention & Strategic Action Plan

  * **Goal:** Provide a direct, actionable list for managers and model retention budgets.
  * **Key Visual:** **Table Visual** sorted descending by **`Churn Risk Score`**.
  * **Strategic Action:** This table serves as the **high-priority call list**. Management should focus retention offers on the customers at the top of this list to maximize the reduction in **\[Total Lost Balance]**. The **What-If Analysis** parameter allows the team to forecast the ROI of any retention investment budget.
