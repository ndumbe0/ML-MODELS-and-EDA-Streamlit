# Power BI Dashboard — Telco Churn (Train + Test)

Built from `telco_churn_traintest.csv` in this folder: the project's 5,042
training customers plus the 2,000-row labeled test set (7,042 customers, no
ID overlap).

**Important:** the test set is deliberately enriched with churned customers
(51.1% churn vs 26.5% in train). Never pool the two for business KPIs —
always filter or split by `dataset`.

## 1. Load the data

1. **Get data → Text/CSV** → `telco_churn_traintest.csv` → **Transform Data**.
2. Types: `tenure`, `churned`, `senior_citizen` → Whole Number;
   `monthly_charges`, `total_charges` → Decimal; rest Text.
3. Rename the query to `Telco`. Close & Apply.
4. (Optional) Load `telco_churn_traintest_summary.csv` as `TelcoSummary`.

## 2. DAX measures

```dax
Churn Rate = AVERAGE(Telco[churned])

Customers = COUNTROWS(Telco)

Revenue at Risk USD =
SUMX(FILTER(Telco, Telco[churned] = 1), Telco[monthly_charges])

Churn Rate — Train Only = CALCULATE([Churn Rate], Telco[dataset] = "train")

Churn Rate — Test Only = CALCULATE([Churn Rate], Telco[dataset] = "test")

Train-Test Gap = [Churn Rate — Test Only] - [Churn Rate — Train Only]
```

## 3. Pages and visuals

### Page 1 — Business view (train only; lock with a filter `dataset = train`)
| Visual | Fields |
|---|---|
| **Card** | `Churn Rate` (%) |
| **Donut** | Legend: `churn` • Values: `Customers` |
| **Bar** | Axis: `contract` • Values: `Churn Rate` |
| **Line** | Axis: `tenure_group` (ordered 0-12…61-72) • Values: `Churn Rate` |
| **Bar** | Axis: `payment_method` • Values: `Churn Rate` |

### Page 2 — Data-quality / model view
| Visual | Fields |
|---|---|
| **Clustered bar** | Axis: `contract` • Legend: `dataset` • Values: `Churn Rate` — shows the enrichment |
| **KPI** | Indicator: `Train-Test Gap` |
| **Matrix** | Rows: `dataset`, `internet_service` • Values: `Churn Rate`, `Customers` |
| **Card** | `Revenue at Risk USD` (train filter) |

### Page 3 — Retention levers
Same as Page 1 but add slicers: `gender`, `senior_citizen`, `partner`,
`dependents`, `contract` (sync across pages).

## 4. Optional: SQL Server

Run `telco_traintest.sql` → database `TelcoChurn_TrainTest`, table
`telco_churn_traintest` + views `v_churn_by_dataset`, `v_churn_by_contract`,
`v_churn_by_payment`, `v_churn_by_tenure_group`, `v_churn_contract_x_dataset`,
`v_revenue_at_risk`.

## 5. Tableau

Open `telco_traintest_dashboard.twb` (expects `telco_churn_traintest.csv`
alongside). 5 sheets: Churn Rate by Dataset / Contract / Tenure Group /
Payment Method, and Monthly Revenue by Churn.
