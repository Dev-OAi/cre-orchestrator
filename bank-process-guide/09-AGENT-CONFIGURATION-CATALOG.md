# 09 — Complete 31-Agent Configuration Catalog

## 1. Overview of the Agent Architecture

The CRE Acquisition Orchestrator is powered by **31 named AI roles**:
- **6 Orchestrators**: High-level workflow directors that enforce phase dependencies, aggregate findings, and enforce stop conditions.
- **21 Acquisition Specialists**: Deep domain agents that execute specialized analytical tasks following the **19-section prompt specification**.
- **4 Document Ingestion Parsers**: Specialized roles that parse, extract, and structure raw source files into verifiable JSON candidates.

---

## 2. Master Agent Directory (All 31 Roles)

| # | Agent Name | Phase / Group | Prompt Path | Primary Specialty |
|---|---|---|---|---|
| 1 | **master-orchestrator** | Master | `orchestrators/master-orchestrator.md` | Full lifecycle coordinator, phase transitions, overall deal verdict. |
| 2 | **due-diligence-orchestrator** | Phase 1 | `orchestrators/due-diligence-orchestrator.md` | Manages 7 diligence specialists, dependency schedules. |
| 3 | **underwriting-orchestrator** | Phase 2 | `orchestrators/underwriting-orchestrator.md` | Coordinates modeling, scenario stress-testing, and IC memo drafting. |
| 4 | **financing-orchestrator** | Phase 3 | `orchestrators/financing-orchestrator.md` | Directs lender outreach, quote evaluation, and term sheet structuring. |
| 5 | **legal-orchestrator** | Phase 4 | `orchestrators/legal-orchestrator.md` | Manages contract, title, survey, estoppel, and loan doc diligence. |
| 6 | **closing-orchestrator** | Phase 5 | `orchestrators/closing-orchestrator.md` | Manages closing checklist, funds flow schedule, and package assembly. |
| 7 | **rent-roll-analyst** | Phase 1 (DD) | `agents/due-diligence/rent-roll-analyst.md` | Rent roll audit, unit mix, loss-to-lease, vacancy, lease anomalies. |
| 8 | **opex-analyst** | Phase 1 (DD) | `agents/due-diligence/opex-analyst.md` | T12 operating expense normalization, tax reassessment modeling. |
| 9 | **physical-inspection** | Phase 1 (DD) | `agents/due-diligence/physical-inspection.md` | PCA review, remaining useful life, deferred maintenance, CapEx budget. |
| 10 | **market-study** | Phase 1 (DD) | `agents/due-diligence/market-study.md` | Submarket rent comps, demographic trends, new supply pipeline. |
| 11 | **environmental-review** | Phase 1 (DD) | `agents/due-diligence/environmental-review.md` | Phase I ESA audit, RECs, contamination risk, remediation sizing. |
| 12 | **legal-title-review** | Phase 1 (DD) | `agents/due-diligence/legal-title-review.md` | Title commitment Schedule B-I/B-II, easements, encumbrances. |
| 13 | **tenant-credit** | Phase 1 (DD) | `agents/due-diligence/tenant-credit.md` | Tenant creditworthiness, employer concentration, lease expiration cliff. |
| 14 | **financial-model-builder** | Phase 2 (UW) | `agents/underwriting/financial-model-builder.md` | 10-year pro forma waterfall, NOI, DSCR, LTV, IRR, Debt Yield. |
| 15 | **scenario-analyst** | Phase 2 (UW) | `agents/underwriting/scenario-analyst.md` | 27-scenario sensitivity cube (rent growth $\times$ vacancy $\times$ cap rate). |
| 16 | **ic-memo-writer** | Phase 2 (UW) | `agents/underwriting/ic-memo-writer.md` | Investment Committee Memo, executive decision card, risk synthesis. |
| 17 | **lender-outreach** | Phase 3 (Fin) | `agents/financing/lender-outreach.md` | Sourcing debt quotes across Agency, Bank, LifeCo, CMBS, Debt Funds. |
| 18 | **quote-comparator** | Phase 3 (Fin) | `agents/financing/quote-comparator.md` | Side-by-side loan quote comparison, debt sizing constraints. |
| 19 | **term-sheet-builder** | Phase 3 (Fin) | `agents/financing/term-sheet-builder.md` | Loan term sheet drafting, covenants, guarantor requirements, escrows. |
| 20 | **psa-reviewer** | Phase 4 (Legal) | `agents/legal/psa-reviewer.md` | Purchase & Sale Agreement audit, critical dates, seller reps & warranties. |
| 21 | **title-survey-reviewer** | Phase 4 (Legal) | `agents/legal/title-survey-reviewer.md` | ALTA/NSPS survey review, boundary encroachments, title endorsements. |
| 22 | **estoppel-tracker** | Phase 4 (Legal) | `agents/legal/estoppel-tracker.md` | Tenant estoppel collection, discrepancy flags, closing threshold. |
| 23 | **loan-doc-reviewer** | Phase 4 (Legal) | `agents/legal/loan-doc-reviewer.md` | Note, Mortgage, Guaranty audit against approved term sheet. |
| 24 | **insurance-coordinator** | Phase 4 (Legal) | `agents/legal/insurance-coordinator.md` | Property/casualty, liability, flood, business interruption compliance. |
| 25 | **transfer-doc-preparer** | Phase 4 (Legal) | `agents/legal/transfer-doc-preparer.md` | Deed, Bill of Sale, FIRPTA, settlement statement, transfer taxes. |
| 26 | **closing-coordinator** | Phase 5 (Closing) | `agents/closing/closing-coordinator.md` | Master closing checklist, conditions precedent, readiness scoring. |
| 27 | **funds-flow-manager** | Phase 5 (Closing) | `agents/closing/funds-flow-manager.md` | Sources & uses, buyer/seller prorations, net lender wire schedule. |
| 28 | **document-orchestrator** | Ingestion | `agents/ingestion/document-orchestrator.md` | Raw file classification, routing, extraction manifest coordination. |
| 29 | **rent-roll-parser** | Ingestion | `agents/ingestion/rent-roll-parser.md` | Extracts unit mix, tenant names, lease dates, rents from XLSX/PDF. |
| 30 | **financials-parser** | Ingestion | `agents/ingestion/financials-parser.md` | Extracts trailing 12-month financial lines, income, and expenses. |
| 31 | **offering-memo-parser** | Ingestion | `agents/ingestion/offering-memo-parser.md` | Extracts property highlights, pricing guidance, and submarket data. |

---

## 3. The Canonical 19-Section Prompt Anatomy

Every specialist agent in the system adheres to a standardized **19-section markdown prompt contract**:

```
 1. Identity Table             --> Name, Role, Phase, Version, Type
 2. Mission                    --> Concise one-paragraph operational directive
 3. Tools Available            --> Read, Write, Bash, Glob, Grep, WebSearch
 4. Input Data                 --> Explicit upstream file dependencies and JSON paths
 5. Strategy                   --> Step-by-step analytical algorithm (Step 1, Step 2, ...)
 6. Output Format              --> Strict JSON schema definition of the agent output
 7. Checkpoint Protocol        --> Checkpoint IDs, triggers, and state persistence rules
 8. Logging Protocol           --> Log event structures, severity levels, attribution IDs
 9. Resume Protocol            --> How the agent recovers state after interruption
10. Runtime Parameters         --> Parameters injected by the orchestrator (dealId, scenario)
11. Tool Usage Patterns        --> Concrete syntax examples for tool calls
12. Error Recovery             --> Error matrix with retry counts and fallback logic
13. Data Gap Handling          --> 5-step protocol when required fields are missing
14. Output Location            --> File destination path, format, and permissions
15. Dealbreaker Detection      --> Unconditional fatal flags that abort pursuit
16. Confidence Scoring         --> Rubric for HIGH (>=0.85), MEDIUM, LOW (<0.65) confidence
17. Downstream Data Contract   --> Exact fields guaranteed to downstream consumers
18. Self-Review Checklist      --> 6-point pre-flight sanity check before writing output
19. Self-Validation Checks     --> Boundary and range check tables (e.g. occupancy between 0-100%)
```

---

## 4. Dynamic Child Agent Spawns

Three specialists possess the architectural authority to dynamically spawn child sub-agents:

1. **`scenario-analyst` (Phase 2)**:
   - Spawns up to **27 child scenario agents**, each executing one specific sensitivity permutation (e.g., Scenario #14: Base rent growth + High vacancy + Expanded cap rate).
2. **`lender-outreach` (Phase 3)**:
   - Spawns up to **12 child lender outreach agents**, each modeling negotiations with a specific capital source (e.g., Fannie Mae DUS lender vs regional commercial bank).
3. **`estoppel-tracker` (Phase 4)**:
   - Spawns up to **200 per-unit estoppel reconciliation child agents**, each matching an individual tenant's returned certificate against the master rent roll row.
