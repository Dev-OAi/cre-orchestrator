# CRE Acquisition Orchestrator — Bank Process & Architecture Guide

Welcome to the **Bank Process & Architecture Guide** for the **CRE Acquisition Orchestrator**. 

This folder contains a comprehensive, step-by-step technical and domain breakdown of this repository. It is designed specifically for **commercial real estate (CRE) banking, underwriting, credit risk management, and loan committee evaluation**, and serves as the primary reference for **Google Antigravity** as we upgrade each section module by module.

---

## Guide Structure & Index

| File | Title | Description |
|---|---|---|
| [01-EXECUTIVE-SYSTEM-OVERVIEW.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/01-EXECUTIVE-SYSTEM-OVERVIEW.md) | **Executive & Banking Overview** | What the CRE Orchestrator is, how the UI/Conversation Desk functions, dual-runtime architecture, and alignment with commercial bank lending (e.g., Valley Bank). |
| [02-END-TO-END-PROCESS-FLOW.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/02-END-TO-END-PROCESS-FLOW.md) | **End-to-End Acquisition Lifecycle** | Visual sequence diagrams, phase dependency timeline, data contracts, and checkpoint state persistence across all 6 stops. |
| [03-STOP-0-DOCUMENT-INGESTION.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/03-STOP-0-DOCUMENT-INGESTION.md) | **Stop 0: Ingestion & Provenance Parsing** | 4 Document Ingestion Agents (`document-orchestrator`, `rent-roll-parser`, `financials-parser`, `offering-memo-parser`), OCR bridge, and provenance tracking. |
| [04-STOP-1-DUE-DILIGENCE.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/04-STOP-1-DUE-DILIGENCE.md) | **Stop 1: Due Diligence Phase** | `due-diligence-orchestrator` and 7 Specialists: Rent Roll, OpEx, Physical Condition, Market Study, Environmental (Phase I ESA), Legal/Title, Tenant Credit. |
| [05-STOP-2-UNDERWRITING.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/05-STOP-2-UNDERWRITING.md) | **Stop 2: Underwriting & Stress Testing** | `underwriting-orchestrator` and 3 Specialists: Financial Model Builder, Scenario Analyst (27 sensitivity cubes), IC Memo Writer, DSCR/LTV stress tests. |
| [06-STOP-3-FINANCING.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/06-STOP-3-FINANCING.md) | **Stop 3: Financing & Debt Sizing** | `financing-orchestrator` and 3 Specialists: Lender Outreach, Quote Comparator, Term Sheet Builder. Sizing debt by DSCR, Debt Yield, and LTV. |
| [07-STOP-4-LEGAL-AND-COLLATERAL.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/07-STOP-4-LEGAL-AND-COLLATERAL.md) | **Stop 4: Legal, Title & Collateral Perfection** | `legal-orchestrator` and 6 Specialists: PSA Reviewer, Title/Survey, Estoppel Tracker, Loan Doc Reviewer, Insurance Coordinator, Transfer Doc Preparer. |
| [08-STOP-5-CLOSING-AND-SETTLEMENT.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/08-STOP-5-CLOSING-AND-SETTLEMENT.md) | **Stop 5: Closing & Funds Flow** | `closing-orchestrator` and 2 Specialists: Closing Coordinator, Funds Flow Manager. Conditions precedent, wire instructions, proration schedule. |
| [09-AGENT-CONFIGURATION-CATALOG.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/09-AGENT-CONFIGURATION-CATALOG.md) | **Complete 31-Agent Matrix** | Full technical configuration for all 31 roles: prompt files, 19-section structure, schemas, referenced skills, error recovery, and child spawns. |
| [10-BANK-UPGRADE-PLAYBOOK.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/10-BANK-UPGRADE-PLAYBOOK.md) | **Bank Upgrade Roadmap** | Blueprint to adapt this system into a Bank Commercial Credit Platform (OCC CRE concentration rules, Credit Committee memos, loan risk grading). |

---

## How Google Antigravity Uses This Guide

When upgrading or modifying any component of the repository:
1. **Identify the Target Stop**: Locate the relevant stop (e.g., Stop 1 for Due Diligence or Stop 2 for Underwriting).
2. **Review Existing Configuration**: Cross-reference [09-AGENT-CONFIGURATION-CATALOG.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/09-AGENT-CONFIGURATION-CATALOG.md) for current agent prompts and JSON schemas.
3. **Execute Upgrade Blueprint**: Follow the actionable steps in [10-BANK-UPGRADE-PLAYBOOK.md](file:///C:/Users/olegm/Desktop/Valley/CREAcquisitionOrchestrator/cre-acquisition-orchestrator/bank-process-guide/10-BANK-UPGRADE-PLAYBOOK.md) to modify prompts, data schemas, calculations, and UI components.
4. **Preserve Trust Boundaries**: Adhere to the strict local-first, human-in-the-loop review gates so no AI agent mutates loan/underwriting data without explicit operator sign-off.
