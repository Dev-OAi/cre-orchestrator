# 02 — End-to-End Acquisition & Diligence Process Flow

## 1. Complete System Flowchart

The lifecycle moves sequentially across six distinct operational stops. A key real-world architectural feature is that **Legal review initiates early (when Due Diligence reaches 80% completion)** to reflect practical deal pacing, while loan document review waits for the financing phase output.

```mermaid
flowchart TD
    subgraph STOP0["Stop 0: Document Ingestion & Provenance"]
        DOCS["Raw Deal Files<br/>(Rent Roll, T12, OM, Leases, Phase I)"]
        PARSERS["4 Ingestion Parsers<br/>(XLSX/CSV Engine + OCR Bridge)"]
        CANDIDATES["Candidate Fields & Provenance<br/>(Cell/Page, Confidence, Source Hash)"]
        GATE{"Human Operator<br/>Approval Gate"}
        
        DOCS --> PARSERS
        PARSERS --> CANDIDATES
        CANDIDATES --> GATE
    end

    subgraph STOP1["Stop 1: Due Diligence Phase (7 Specialists)"]
        DDO["Due Diligence Orchestrator"]
        RRA["Rent Roll Analyst"]
        OPA["OpEx Analyst"]
        PI["Physical Inspection"]
        MS["Market Study"]
        ER["Environmental Review"]
        LTR["Legal Title Review"]
        TC["Tenant Credit"]
        
        GATE -->|"Approved Data Snapshot"| DDO
        DDO --> RRA
        DDO --> OPA
        DDO --> PI
        DDO --> MS
        DDO --> ER
        DDO --> LTR
        DDO --> TC
    end

    subgraph STOP2["Stop 2: Underwriting Phase (3 Specialists)"]
        UWO["Underwriting Orchestrator"]
        FMB["Financial Model Builder<br/>(10-Yr Pro Forma, NOI, DSCR)"]
        SA["Scenario Analyst<br/>(27 Sensitivity Cases)"]
        ICM["IC Memo Writer<br/>(Investment / Credit Memo)"]
        
        RRA & OPA & PI & MS & TC -->|"DD 100% Complete"| UWO
        UWO --> FMB
        FMB --> SA
        SA --> ICM
    end

    subgraph STOP3["Stop 3: Financing Phase (3 Specialists)"]
        FINO["Financing Orchestrator"]
        LO["Lender Outreach<br/>(Agency, CMBS, LifeCo, Bank)"]
        QC["Quote Comparator<br/>(Rate, LTV, DSCR, Covenants)"]
        TSB["Term Sheet Builder<br/>(Recommended Loan Structure)"]
        
        ICM -->|"UW 100% Complete"| FINO
        FINO --> LO
        LO --> QC
        QC --> TSB
    end

    subgraph STOP4["Stop 4: Legal & Collateral Phase (6 Specialists)"]
        LEGO["Legal Orchestrator"]
        PSA["PSA Reviewer"]
        TSR["Title & Survey Reviewer"]
        ET["Estoppel Tracker"]
        IC["Insurance Coordinator"]
        TDP["Transfer Doc Preparer"]
        LDR["Loan Doc Reviewer"]
        
        DDO -.->|"Trigger: DD 80% Complete"| LEGO
        LEGO --> PSA
        LEGO --> TSR
        LEGO --> ET
        LEGO --> IC
        LEGO --> TDP
        TSB -->|"Approved Term Sheet"| LDR
        LEGO --> LDR
    end

    subgraph STOP5["Stop 5: Closing & Settlement Phase (2 Specialists)"]
        CLO["Closing Orchestrator"]
        CC["Closing Coordinator<br/>(Readiness Checklist & CP)"]
        FFM["Funds Flow Manager<br/>(Sources & Uses, Wire Schedule)"]
        PACKAGE["Final IC / Credit Committee Package<br/>(Audit Manifest, Reports, Memos)"]
        
        UWO & TSB & LEGO --> CLO
        CLO --> CC
        CC --> FFM
        FFM --> PACKAGE
    end

    style STOP0 fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#fff
    style STOP1 fill:#0f172a,stroke:#06b6d4,stroke-width:2px,color:#fff
    style STOP2 fill:#0f172a,stroke:#8b5cf6,stroke-width:2px,color:#fff
    style STOP3 fill:#0f172a,stroke:#ec4899,stroke-width:2px,color:#fff
    style STOP4 fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#fff
    style STOP5 fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#fff
    style GATE fill:#b91c1c,stroke:#f87171,stroke-width:2px,color:#fff
    style PACKAGE fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#fff
```

---

## 2. Phase Execution Sequence & Triggers

| Stop # | Phase Name | Trigger Condition | Execution Mode | Downstream Deliverables |
|---|---|---|---|---|
| **Stop 0** | **Document Ingestion** | Raw files dropped in workspace | Sequential parsing, parallel OCR | Extracted candidate JSON with cryptographic hash and cell/page provenance. |
| **Gate** | **Human Review Gate** | Candidate fields generated | Manual Underwriter Sign-off | Immutable `input-snapshot.json` locking in approved property metrics. |
| **Stop 1** | **Due Diligence** | Input snapshot verified | 5 parallel agents + 2 sequential | Property risk score, physical deferred CapEx, market rent comps, tenant concentration. |
| **Stop 2** | **Underwriting** | Due Diligence 100% complete | Strict sequential: Model → Scenarios → Memo | 10-year pro forma cash flow waterfall, 27-scenario sensitivity cube, Draft IC Memo. |
| **Stop 3** | **Financing** | Underwriting 100% complete | Parallel lender outreach → Sequential quote compare | Comparative lender matrix (Agency vs Bank vs CMBS), Debt sizing by DSCR/LTV/Debt Yield. |
| **Stop 4** | **Legal & Collateral** | **Early trigger: DD 80% complete** (Loan reviewer waits for Financing) | 4 parallel legal agents + 1 sequential loan doc agent | Title exception schedule, ALTA survey analysis, lease estoppel tracker, insurance compliance report. |
| **Stop 5** | **Closing & Settlement** | All prior 4 phases complete | Sequential: Coordinator → Funds Flow | Final closing checklist, conditions precedent, funds flow wire schedule, IC package export. |

---

## 3. Data Contracts & State Persistence

To ensure auditability required by institutional financial institutions, no data is passed informally between agents. Every handoff is persisted on disk and validated against JSON Schemas:

1. **`data/deals/{dealId}/deal.json`**: Core deal parameters (property name, address, unit count, asking price).
2. **`data/deals/{dealId}/documents/`**: Original immutable source files with SHA-256 integrity hashes.
3. **`data/runs/{dealId}/input-snapshot.json`**: The frozen, approved dataset used by the run manager.
4. **`data/status/{dealId}/checkpoints/`**: Incremental phase states (`due-diligence.json`, `underwriting.json`, etc.). If a pipeline fails or is cancelled, it resumes exactly from the last verified checkpoint.
5. **`data/phase-outputs/{dealId}/`**: Formally validated structured outputs for each phase conforming to schemas in `schemas/phases/`.
6. **`data/reports/{dealId}/`**: Human-readable Markdown reports generated by specialists for the investment package.
7. **`data/deals/{dealId}/packages/`**: The compiled, versioned **Investment Committee Starter Package** (`.md` and `.json`), ready for distribution to loan committees.
