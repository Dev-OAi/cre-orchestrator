# 01 — Executive & Banking Overview

## 1. What is the CRE Acquisition Orchestrator?

The **CRE Acquisition Orchestrator** is an open-source, multi-agent artificial intelligence framework engineered for **Commercial Real Estate (CRE) acquisitions and underwriting**. 

While general AI frameworks focus on generic coding or casual chat, this system models how institutional multifamily and commercial real estate transactions actually move across **Due Diligence, Financial Modeling & Underwriting, Debt Financing, Legal & Title Review, and Final Closing**.

### By the Numbers:
- **31 Named AI Roles**: 6 Orchestrators, 21 Specialized Domain Agents, and 4 Document Ingestion Parsers.
- **5 Core Acquisition Phases**: Due Diligence, Underwriting, Financing, Legal, Closing (plus Document Ingestion as Step 0).
- **8 CRE Domain Knowledge Bases (Skills)**: Real estate formulas, risk scoring matrices, multifamily operating benchmarks, lender underwriting guidelines, legal checklists, logging protocols, and self-review validation.
- **28 Strict JSON Schemas**: Every data handoff between agents, phases, and tools is strictly validated using AJV schemas.
- **Two Distinct Runtimes**:
  1. **Deterministic Local Simulation**: 100% offline, zero-credential engine that computes pro formas and triggers mock agent events for testing, CI/CD, and fast demonstrations.
  2. **Live Agent Runner**: Authenticated LLM runner that executes deep agent prompts, searches live comps/demographics/rates, and performs unstructured document reasoning.

---

## 2. Decoding the Demo UI (What You See on Screen)

When running `run_workspace.bat`, the system initiates:
1. `npm --prefix dashboard run dev:server` on a local background Node/TypeScript service (`watcher.ts` on port 3001/WebSocket).
2. `npm --prefix dashboard run dev:client` via Vite on `http://localhost:5173`.

```
========================================================================================================
[ CRE Acquisition Orchestrator — Top Bar: Connected | Advanced | Deals | + New Deal ]
========================================================================================================
[ 1 · CHOOSE A DEAL ]         | [ 2 · CHOOSE A SPECIALIST: Financials Parser (Ingestion) ] [Open Workspace]
- Parkview Apartments (200u)  | ----------------------------------------------------------------------
- Oakwood (SAMPLE)            | [Deal ready] [No source documents yet]   [ADD DOCUMENTS] [SET UP CHATGPT]
- Riverside (SAMPLE)          | 
                              | START HERE:
RECENT CONVERSATIONS:         | "What do you want to know about Parkview Apartments?"
- Financials Parser           | "You're speaking with Financials Parser. Add source documents first..."
- Transfer Doc Preparer       | ----------------------------------------------------------------------
- Tenant Credit               | [ 3 · ASK FINANCIALS PARSER ]
- Legal Title Review          | [ Ask about Parkview Apartments...                                  ]
========================================================================================================
```

### The Three Steps of the Front Door ("Conversation Desk")
1. **Step 1: Choose a Deal (Left Sidebar)**:
   - Selects the active deal context (e.g., `Parkview Apartments`, a 200-unit multifamily asset in Austin, TX).
   - Shows existing deal files, upload history, and past retained conversations with agents.
2. **Step 2: Choose a Specialist (Center Workspace)**:
   - An interactive dropdown allowing you to select any of the 31 AI roles (e.g., `Financials Parser`, `Rent Roll Analyst`, `Market Study Analyst`, `Loan Doc Reviewer`).
   - Clicking **"Open full workspace"** transitions from simple conversational Q&A into the complete institutional **Lifecycle Deal Workspace** (with Gantt progress, phase briefs, red flag consoles, and the Investment Committee package).
3. **Step 3: Ask the Specialist (Bottom Input Box)**:
   - Allows natural language querying of the property's underlying documents.
   - **Crucial Trust Rule**: The agent will **never hallucinate**. If source documents (Rent Roll, T12 operating statement, Offering Memo) have not been uploaded or approved, the agent explicitly flags `unanswered=true` and prompts the user to add source files first.
   - When documents are uploaded, every response extracts and displays exact citations (file name, sheet, cell, row, or page number).

---

## 3. Commercial Bank Perspective (Valley Bank Context)

In a commercial real estate lending department at a bank (such as Valley Bank), a deal is analyzed from a **debt and credit risk** perspective rather than purely an equity sponsor perspective:

| Sponsor / Private Equity Focus | Commercial Bank Lending Focus | CRE Orchestrator Alignment |
|---|---|---|
| **Max Levered IRR & Equity Multiple** | **Debt Service Coverage Ratio (DSCR) & Cash Flow Durability** | Orchestrator calculates both, but can be tailored to stress minimum debt coverage (e.g., 1.25x - 1.35x DSCR). |
| **Upside Renovation Potential & Value Creation** | **Downside Collateral Valuation & Loan-to-Value (LTV)** | Physical inspection and OpEx benchmarking verify if CapEx budgets and reserve deposits are adequate to protect collateral. |
| **Aggressive Exit Cap Rate Assumptions** | **Refinancing Risk & Exit Debt Yield** | Scenario Analyst stress-tests 27 sensitivity cases, including cap rate expansion (+50 to +150 bps) and higher exit mortgage rates. |
| **Quick Letter of Intent (LOI) Execution** | **Regulatory Compliance (OCC CRE Concentrations, Basel III)** | Audit-ready trail: every extracted field has a cryptographic hash (`sourceHash`) and page/cell provenance for bank examiners. |
| **General Title & Legal Review** | **First-Lien Mortgage Collateral Perfection & Estoppel Clearance** | Legal orchestrator tracks tenant estoppels (aiming for >85-90%), loan document covenants, non-recourse carveout guarantees, and ALTA title policy endorsements. |

---

## 4. Why This Architecture Matters for Bank Modernization

1. **Deterministic Truth Boundary**: In a regulated financial institution, an LLM must never silently guess financial numbers. In this system, raw documents are parsed by deterministic parsers (or review-gated OCR). An underwriter or credit officer must click **"Approve"** on candidate fields before they populate the pro forma model.
2. **Modular Role Specialization**: Instead of asking a single prompt to do an entire 60-page loan credit memo, the work is divided among 31 specialists. A tenant concentration expert evaluates rollover risk while a civil/environmental specialist reviews Phase I ASTM E1527-21 reports.
3. **Durable Auditable Artifacts**: The end result is not just chat text; it is an **Investment Committee (IC) / Credit Committee Starter Package**, complete with a 27-scenario sensitivity cube, risk scorecards, wire schedules, and an evidence provenance graph.
