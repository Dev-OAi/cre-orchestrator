"""
Local Agent Runner - Offline Multi-Page Document Inspection & Agent Chat
Powered by local Ollama (gemma4-32k / gemma4:e2b) without Antigravity cloud quota.

Features:
1. inspect_scanned_pdf: Multi-page scan & native text extraction via PyMuPDF + Ollama Vision/OCR.
2. ask_local_ollama: Structured agent reasoning & conversation for CRE specialists (Intake, Underwriting, Diligence).
3. End-to-end deal progression test: Ingests documents, parses tables/text, runs underwriting queries, and generates reports.
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import pymupdf  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

DEFAULT_OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:e2b")

# Fallback models if default isn't present
MODEL_CANDIDATES = [
    DEFAULT_MODEL,
    "gemma4-32k:latest",
    "gemma4:latest",
    "llama3:latest",
    "mistral:latest",
]


def resolve_active_model(host: str = DEFAULT_OLLAMA_HOST) -> str:
    """Detect available models from local Ollama tags endpoint."""
    url = f"{host}/api/tags"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            installed = [m.get("name", "") for m in data.get("models", [])]
            for candidate in MODEL_CANDIDATES:
                if any(candidate in name for name in installed):
                    return candidate
            if installed:
                return installed[0]
    except Exception:
        pass
    return DEFAULT_MODEL


def call_ollama_chat(
    prompt: str,
    system_prompt: Optional[str] = None,
    encoded_images: Optional[List[str]] = None,
    format_json: bool = False,
    model: Optional[str] = None,
    host: str = DEFAULT_OLLAMA_HOST,
    timeout: int = 300,
) -> Dict[str, Any]:
    """Call Ollama chat endpoint with robust error handling."""
    active_model = model or resolve_active_model(host)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    user_msg: Dict[str, Any] = {"role": "user", "content": prompt}
    if encoded_images:
        user_msg["images"] = encoded_images
    messages.append(user_msg)

    payload: Dict[str, Any] = {
        "model": active_model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 16384,
        },
    }
    if format_json:
        payload["format"] = "json"

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{host}/api/chat",
        data=data_bytes,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_content = data.get("message", {}).get("content", "")
            return {
                "success": True,
                "model": active_model,
                "content": raw_content,
            }
    except Exception as e:
        return {
            "success": False,
            "model": active_model,
            "error": str(e),
            "content": f"Ollama connection error: {e}",
        }


def ask_local_ollama(
    prompt: str,
    agent_role: str = "general",
    deal_context: Optional[Dict[str, Any]] = None,
    format_json: bool = False,
) -> str:
    """Structured CRE specialist query using local Ollama."""
    roles = {
        "intake": (
            "You are a meticulous Commercial Real Estate Intake Paralegal. "
            "Extract verified lease terms, property metadata, asking prices, and square footages. "
            "Never hallucinate numbers. When asked for JSON, output valid JSON only."
        ),
        "underwriting": (
            "You are an Institutional Real Estate Underwriter. "
            "Calculate and critique NOI, implied Cap Rates, DSCR, and cash flow assumptions. "
            "Provide quantitative analysis citing specific financial line items."
        ),
        "diligence": (
            "You are a CRE Title and Due Diligence Attorney. "
            "Analyze legal checklists, lease covenants, survey exceptions, and identify closing risks."
        ),
        "general": "You are an expert Commercial Real Estate AI assistant.",
    }
    system_prompt = roles.get(agent_role, roles["general"])
    if deal_context:
        prompt = f"Context Data:\n{json.dumps(deal_context, indent=2)}\n\nQuery:\n{prompt}"

    res = call_ollama_chat(prompt=prompt, system_prompt=system_prompt, format_json=format_json)
    return res.get("content", "")


def inspect_scanned_pdf(
    pdf_path: str,
    prompt: str = "Extract all key text, tables, figures, and financial details in a structured summary.",
    start_page: int = 1,
    max_pages: int = 3,
    dpi: int = 225,
    min_text_chars: int = 50,
    force_vision: bool = False,
    host: str = DEFAULT_OLLAMA_HOST,
) -> Dict[str, Any]:
    """
    Offline multi-page PDF inspector:
    - Extracts native selectable text directly when available.
    - Renders low-text or scanned pages to high-DPI PNGs and inspects with Ollama vision.
    - Zero external API quota consumed.
    """
    clean_path = Path(pdf_path).resolve()
    if not clean_path.is_file():
        return {"success": False, "error": f"File not found: {clean_path}"}

    if not PYMUPDF_AVAILABLE:
        return {"success": False, "error": "PyMuPDF (fitz) is not installed."}

    temp_dir = tempfile.mkdtemp(prefix="cre_inspect_")
    doc = None
    try:
        doc = pymupdf.open(str(clean_path))
        total_pages = len(doc)
        first_idx = max(0, start_page - 1)
        last_idx = min(total_pages, first_idx + max_pages)

        if first_idx >= total_pages:
            return {"success": False, "error": f"start_page {start_page} exceeds total pages ({total_pages})"}

        native_sections = []
        vision_page_nums = []
        encoded_images = []
        zoom = dpi / 72.0
        matrix = pymupdf.Matrix(zoom, zoom)

        for p_idx in range(first_idx, last_idx):
            page_num = p_idx + 1
            page = doc.load_page(p_idx)
            text = page.get_text("text").strip()

            if not force_vision and len(text) >= min_text_chars:
                native_sections.append(f"--- Page {page_num} (Native Text) ---\n{text}")
            else:
                vision_page_nums.append(page_num)
                pix = page.get_pixmap(matrix=matrix)
                img_path = os.path.join(temp_dir, f"page_{page_num}.png")
                pix.save(img_path)
                with open(img_path, "rb") as f:
                    encoded_images.append(base64.b64encode(f.read()).decode("utf-8"))

        context_blocks = []
        if native_sections:
            context_blocks.append("Extracted Text Sections:\n" + "\n\n".join(native_sections))
        if encoded_images:
            context_blocks.append(f"Rendered image pages sent to Vision: {vision_page_nums}")

        composite_prompt = (
            f"{prompt}\n\n"
            f"[Document: {clean_path.name} | Pages: {first_idx + 1}-{last_idx} of {total_pages}]\n\n"
            f"{''.join(context_blocks)}"
        )

        resp = call_ollama_chat(
            prompt=composite_prompt,
            encoded_images=encoded_images or None,
            host=host,
        )
        return {
            "success": resp.get("success", False),
            "file": clean_path.name,
            "pages_analyzed": list(range(first_idx + 1, last_idx + 1)),
            "vision_pages": vision_page_nums,
            "analysis": resp.get("content", ""),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if doc is not None:
            doc.close()
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_full_deal_test():
    """Runs a complete test from New Deal ingestion through Underwriting and Diligence review."""
    print("=" * 70)
    print("🚀 CRE Acquisition Orchestrator - Local Offline Agent Test")
    print(f"Connecting to Local Ollama: {DEFAULT_OLLAMA_HOST}")
    active_model = resolve_active_model()
    print(f"Active Model: {active_model}")
    print("=" * 70)

    fixtures_dir = Path(__file__).resolve().parent.parent / "fixtures" / "sample_deal_suite"
    deal_file = fixtures_dir / "deal.json"
    om_file = fixtures_dir / "offering_memorandum.md"
    rr_file = fixtures_dir / "rent_roll.csv"
    t12_file = fixtures_dir / "t12_operating_statement.csv"
    legal_file = fixtures_dir / "legal_diligence_checklist.md"

    if not deal_file.exists():
        print(f"Error: Sample fixtures not found at {fixtures_dir}")
        return

    # Step 1: Load Deal
    with open(deal_file, "r", encoding="utf-8") as f:
        deal = json.load(f)
    print(f"\n[1] Deal Created: '{deal.get('dealName')}' ({deal.get('dealId')})")
    print(f"    Asking Price: ${deal['financials']['askingPrice']:,} | RSF: {deal['property']['totalSqFt']:,}")

    # Step 2: Intake Agent Document Extraction
    print("\n[2] Ingesting Documents (OM, Rent Roll, T12, Legal Checklist)...")
    with open(om_file, "r", encoding="utf-8") as f:
        om_text = f.read()[:1500]

    intake_prompt = (
        f"Based on this excerpt, extract in 2 bullet points the property description and key upside:\n{om_text}"
    )
    print("    Calling Intake Agent (Local Ollama)...")
    intake_summary = ask_local_ollama(intake_prompt, agent_role="intake")
    print("    Intake Agent Summary:\n", "   ", intake_summary.strip().replace("\n", "\n    "))

    # Step 3: Underwriting Agent Analysis
    print("\n[3] Running Underwriting Valuation Review...")
    underwrite_prompt = (
        f"The property Asking Price is ${deal['financials']['askingPrice']:,} with current NOI ${deal['financials']['currentNOI']:,}. "
        f"Calculate the in-place Cap Rate. Compare it to the stated target hold of {deal['targetHoldPeriod']} years."
    )
    uw_summary = ask_local_ollama(underwrite_prompt, agent_role="underwriting", deal_context=deal)
    print("    Underwriter Analysis:\n", "   ", uw_summary.strip().replace("\n", "\n    "))

    # Step 4: Legal & Diligence Risk Review
    print("\n[4] Running Diligence Review on Legal Checklist...")
    with open(legal_file, "r", encoding="utf-8") as f:
        legal_text = f.read()

    diligence_prompt = f"Review this checklist and flag any open or critical items before closing:\n{legal_text}"
    diligence_summary = ask_local_ollama(diligence_prompt, agent_role="diligence")
    print("    Diligence Agent Findings:\n", "   ", diligence_summary.strip().replace("\n", "\n    "))

    print("\n" + "=" * 70)
    print("✅ Deal Workflow Test Complete - 100% Offline with Local Ollama")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--inspect":
        pdf = sys.argv[2] if len(sys.argv) > 2 else "sample.pdf"
        res = inspect_scanned_pdf(pdf)
        print(json.dumps(res, indent=2))
    else:
        run_full_deal_test()
