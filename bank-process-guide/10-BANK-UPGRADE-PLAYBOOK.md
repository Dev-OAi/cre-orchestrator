# 10 — Bank Upgrade Playbook: Transforming for Institutional CRE Lending

## 1. Executive Modernization Blueprint

This playbook outlines the modular engineering roadmap for adapting the **CRE Acquisition Orchestrator** into an **Institutional Commercial Real Estate Lending & Credit Risk Platform** tailored for a commercial bank (e.g., Valley Bank).

While the original open-source framework focuses on an **equity acquisition sponsor**, a commercial bank evaluates transactions through the lens of **credit safety, debt serviceability, regulatory compliance (OCC / FDIC / Federal Reserve), collateral perfection, and loan committee approval**.

```
+-----------------------------------------------------------------------------------------------+
|                        COMMERCIAL BANK UPGRADE ARCHITECTURE                                   |
+-----------------------------------------------------------------------------------------------+
| 1. BORROWER & SPONSOR DILIGENCE   --> KYC/BSA, Net Worth, Global Cash Flow, Credit History     |
| 2. RIGOROUS DEBT SIZING           --> Min DSCR (1.25x-1.35x), Min Debt Yield (8.5%+), Max LTV |
| 3. REGULATORY STRESS TESTING      --> OCC 2006-46 Guidance, +200/300 bps Rate Shocks, Vacancy |
| 4. COLLATERAL & TITLE PERFECTION  --> ALTA 9/17/18/19 Endorsements, Non-Recourse Carveouts     |
| 5. CREDIT COMMITTEE MEMO ENGINE   --> Automated Institutional Loan Approval Recommendation    |
+-----------------------------------------------------------------------------------------------+
```

---

## 2. Section-by-Section Upgrade Specifications

### Stop 0: Document Ingestion — The Banking Intake Upgrade
*Current State:* Parses Rent Roll, T12, and Offering Memo.
*Target Banking Upgrade:*
1. **Borrower Financial Ingestion**:
   - Ingest 3 years of Borrower/Guarantor Federal Tax Returns (IRS 1040, 1120S, 1065) and audited Personal Financial Statements (PFS).
   - Calculate Borrower Adjusted Gross Income (AGI), recurring cash flow, and contingent liabilities.
2. **Third-Party FIRREA Appraisal Parser**:
   - Extract independent Appraised As-Is Market Value, As-Stabilized Value, appraiser cap rate, and market rent conclusions.
3. **Phase I Environmental Site Assessment (ESA) Parser**:
   - Automatically extract Section 1.0 Executive Summary, flagging RECs, historical dry-cleaning operations, or nearby USTs.

### Stop 1: Due Diligence — Credit Risk & Sponsor Diligence
*Current State:* 7 specialists evaluate property condition, market comps, and tenant rollover.
*Target Banking Upgrade:*
1. **Sponsor Credit & Track Record Specialist**:
   - Create `sponsor-credit-analyst.md` to evaluate borrower experience, portfolio scale, historical loan default history, and bankruptcy records.
2. **Global Cash Flow & Contingent Liability Specialist**:
   - Analyze borrower's broader portfolio to ensure other distressed properties will not drain borrower liquidity.
3. **OCC CRE Concentration & Policy Gate**:
   - Implement regulatory check against interagency CRE lending thresholds (e.g., total commercial real estate loans exceeding 300% of total risk-based capital).

### Stop 2: Underwriting — Credit Committee Memo & Stress Testing
*Current State:* Models 10-year equity IRR and 27-scenario sensitivity cube.
*Target Banking Upgrade:*
1. **Shift Focus from IRR to Debt Metrics**:
   - Primary sizing metrics: **Underwritten In-Place DSCR**, **Stabilized DSCR**, **Debt Yield**, and **Loan-to-Cost (LTC)**.
   - Enforce minimum replacement reserve holdback (\$250 - \$350/unit/year) before calculating debt coverage.
2. **OCC Regulatory Interest Rate Shock Testing**:
   - Implement +100 bps, +200 bps, and +300 bps SOFR rate shock tests to measure debt service resilience upon floating-to-fixed conversion or loan maturity.
3. **Bank Credit Memorandum Writer**:
   - Upgrade `ic-memo-writer.md` to generate the bank's standard **Credit Committee Loan Recommendation**:
     - Borrower & Guarantor Summary
     - Collateral & Location Assessment
     - Historical Cash Flow vs Underwritten Pro Forma
     - Proposed Loan Terms, Pricing & Fees
     - Risk Rating Recommendation (Pass Grade 1-4 vs Criticized / Classified)
     - Identified Credit Policy Exceptions & Mitigants.

### Stop 3: Financing — Loan Structuring & Covenant Engineering
*Current State:* Compares external quotes to recommend best debt provider.
*Target Banking Upgrade:*
1. **Internal Bank Loan Pricing Engine**:
   - Replace broker comparison with bank internal pricing logic: Base Index (SOFR or Prime) + Credit Spread (e.g. 225-325 bps) + Floor Rate (e.g. 5.50%).
2. **Covenant & Depository Relationship Module**:
   - Add deposit relationship incentives (e.g., 25 bps rate discount if operating accounts with \$2M+ average balance are maintained at the bank).
   - Require Debt Service Reserve Accounts (DSRA) of 3 to 6 months of P&I for higher-risk loans.

### Stop 4: Legal — First-Lien Perfection & Loan Document Compliance
*Current State:* Reviews PSA, title exceptions, and 200 estoppels.
*Target Banking Upgrade:*
1. **Lender Title Endorsement Verifier**:
   - Explicitly verify required ALTA Endorsements for commercial lenders:
     - ALTA 9.06 (Restrictions, Encroachments, Minerals)
     - ALTA 17.06 (Access and Entry)
     - ALTA 18.06 (Single Tax Parcel)
     - ALTA 19.06 (Contiguity)
     - ALTA 25.06 (Same as Survey).
2. **Non-Recourse Carveout ("Bad Boy") Guaranty Reviewer**:
   - Audit guaranty terms for standard institutional carveouts: fraud, material misrepresentation, voluntary bankruptcy, waste, misapplication of rents/security deposits, environmental liability.

### Stop 5: Closing — Loan Disbursement & Credit Admin Ledger
*Current State:* Coordinates closing checklist and wire instructions.
*Target Banking Upgrade:*
1. **Loan Disbursement Authorization Sheet**:
   - Standard bank closing sheet calculating Gross Loan, less Bank Counsel Fees, Origination Points, Third-Party Report Invoices, and Initial Tax/Insurance Escrows.
2. **Post-Closing Trailing Items Tracking**:
   - Recorded Mortgage / Deed of Trust, final ALTA Title Policy with endorsements, final UCC-1 state filings, certificate of occupancy.

---

## 3. How to Prompt Antigravity for Each Upgrade Step

When you are ready to begin upgrading with Google Antigravity, use this sequential prompt workflow:

### Step 1: Upgrading Stop 0 (Document Intake)
> *"Google Antigravity, we are upgrading Stop 0 (Document Ingestion) for our commercial bank workflow. Please review `bank-process-guide/03-STOP-0-DOCUMENT-INGESTION.md` and `dashboard/server/parser-service.ts`. We want to add parsing support for Borrower Personal Financial Statements (PFS) to extract liquid assets, total net worth, and contingent liabilities into our candidate field extraction schema."*

### Step 2: Upgrading Stop 1 (Due Diligence & Sponsor Analysis)
> *"Google Antigravity, let's upgrade Stop 1 (Due Diligence). Please review `bank-process-guide/04-STOP-1-DUE-DILIGENCE.md`. We want to create a new specialist agent `agents/due-diligence/sponsor-credit-analyst.md` following the 19-section prompt standard to evaluate commercial borrower experience, credit history, and portfolio liquidity."*

### Step 3: Upgrading Stop 2 (Underwriting & Credit Committee Memo)
> *"Google Antigravity, let's upgrade Stop 2 (Underwriting). Please reference `bank-process-guide/05-STOP-2-UNDERWRITING.md`. We want to modify `agents/underwriting/ic-memo-writer.md` and `agents/underwriting/financial-model-builder.md` to output a formal Bank Credit Committee Memorandum, including OCC interest rate stress tests (+200 bps / +300 bps) and risk rating classification (Pass Grade 1 to 4)."*

### Step 4: Upgrading Stop 3 (Bank Loan Pricing & Structuring)
> *"Google Antigravity, let's upgrade Stop 3 (Financing). Reference `bank-process-guide/06-STOP-3-FINANCING.md`. We want to adapt `agents/financing/term-sheet-builder.md` to structure our bank's direct loan terms: SOFR + margin, floor rate, minimum 1.25x DSCR covenant, and depository relationship requirements."*

### Step 5: Upgrading Stop 4 & 5 (Legal Perfection & Closing Administration)
> *"Google Antigravity, let's upgrade Stop 4 and Stop 5. Reference `bank-process-guide/07-STOP-4-LEGAL-AND-COLLATERAL.md` and `bank-process-guide/08-STOP-5-CLOSING-AND-SETTLEMENT.md`. We want to configure `agents/legal/loan-doc-reviewer.md` to verify the bank's ALTA title endorsement package and non-recourse carveout guaranty, and update `agents/closing/funds-flow-manager.md` to generate a standard bank loan disbursement authorization sheet."*
