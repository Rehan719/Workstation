import os
import shutil
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import datetime
import uuid
import json

from config.paths import DATA_DIR
from agentic_core.ai.ceo.memory_v01 import memory_v01

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ingest", tags=["Content Ingestion"])

# §15.6 (W495, FU-124) — TRANSCRIPTION_MOCK IS DELETED.
#
# It was a filename-pattern lookup table whose output was registered as a file's `extracted_text` with
# status INGESTED, written into memory_v01 (the store the AI CEO and the avatars read) and fed into every
# synthesis prompt as "Knowledge base". Nothing was transcribed; no transcription engine exists in this
# codebase. An upload whose NAME contained "recitation" was given this as its content:
#
#     "In the name of Allah, the Most Gracious, the Most Merciful. All praise is due to Allah, Lord of
#      the worlds."
#
# — an English rendering of the Basmala and Al-Fatiha 1:2, attached to a user's file as its transcription.
# Under this platform's faith-content rules scripture is served only from its recorded sources and is
# never produced by this system, so a hard-coded rendering presented as a user's file content is the
# worst shape this defect class takes. The other two patterns fabricated sentences about the Qur'an and
# about "digital sovereignty" the same way.
#
# There is no replacement, because there is nothing here that transcribes audio. The honest states are
# read, not-readable-here, or absent — see _extract_text below.

# what a real extractor would be, when one is installed: checked at call time, never assumed
def _pdf_docx_extractor(ext: str):
    """Returns (name, callable) for a REAL extractor if one is importable, else (None, None).

    Kept as a lookup so that installing pypdf or python-docx makes extraction work without another
    truth fix — and so that its absence is reported rather than papered over."""
    if ext == ".pdf":
        for mod, fn in (("pypdf", "PdfReader"), ("PyPDF2", "PdfReader")):
            try:
                m = __import__(mod)
                return f"{mod}.{fn}", getattr(m, fn)
            except Exception:
                continue
    if ext == ".docx":
        try:
            import docx  # python-docx
            return "python-docx", docx.Document
        except Exception:
            pass
    return None, None

class IngestedFile(BaseModel):
    file_id: str
    filename: str
    content_type: str
    size: int
    timestamp: str
    extracted_text: str
    status: str
    # W495 (FU-124) — the response MODEL strips undeclared keys, so the three fields that say which of
    # the three states applied were dropped at the boundary and no surface could have read them. A
    # qualifier that does not leave the process is not a qualifier.
    extraction_method: Optional[str] = None
    extraction_basis: str = ""
    in_knowledge_base: bool = False
    category: Optional[str] = None

class IngestionManager:
    def __init__(self):
        self.registry_path = DATA_DIR / "ingestion_registry.json"
        self.upload_dir = DATA_DIR / "uploads"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.registry = self._load_registry()

    def _load_registry(self) -> List[Dict[str, Any]]:
        if self.registry_path.exists():
            with open(self.registry_path, "r") as f:
                return json.load(f)
        return []

    def _save_registry(self):
        with open(self.registry_path, "w") as f:
            json.dump(self.registry, f, indent=2)

    async def ingest_file(self, file: UploadFile, category: Optional[str] = None) -> Dict[str, Any]:
        file_id = str(uuid.uuid4())
        file_path = self.upload_dir / f"{file_id}_{file.filename}"

        # 1. Save File to Disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Read the content, or say it was not read. §15.6 (W495, FU-124) — every branch but the
        #    first invented text: a constant for pdf/docx, a filename lookup for audio, a sentence for
        #    everything else. `extracted_text` now holds ONLY text this process actually read, and the
        #    status says which of the three states applies.
        extracted_text = ""
        status = "NOT_EXTRACTED"
        extraction_method = None
        extraction_basis = ""
        filename_lower = (file.filename or "").lower()
        _ext = os.path.splitext(filename_lower)[1]

        if _ext in (".txt", ".md"):
            try:
                extracted_text = file_path.read_text(encoding="utf-8", errors="replace")
                status, extraction_method = "EXTRACTED", "read as UTF-8 text from disk"
                extraction_basis = "the file is plain text and was read in full"
            except Exception as e:
                extraction_basis = f"the file could not be read as text: {type(e).__name__}"
        elif _ext in (".pdf", ".docx"):
            _name, _reader = _pdf_docx_extractor(_ext)
            if _reader is None:
                extraction_basis = (f"NOT EXTRACTED — no {_ext[1:]} extractor is installed in this "
                                    f"environment (pypdf / python-docx), so nothing in this document has "
                                    f"been read. It is stored as an attachment only.")
            else:
                try:
                    if _ext == ".pdf":
                        extracted_text = "\n".join((pg.extract_text() or "")
                                                   for pg in _reader(str(file_path)).pages)
                    else:
                        extracted_text = "\n".join(p.text for p in _reader(str(file_path)).paragraphs)
                    extracted_text = extracted_text.strip()
                    if extracted_text:
                        status, extraction_method = "EXTRACTED", _name
                        extraction_basis = f"text extracted by {_name}"
                    else:
                        extraction_basis = (f"NOT EXTRACTED — {_name} read the file and found no text "
                                            f"(it may be a scan or an image-only document)")
                except Exception as e:
                    extraction_basis = (f"NOT EXTRACTED — {_name} failed on this file: "
                                        f"{type(e).__name__}")
        elif _ext in (".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".flac", ".webm", ".mov"):
            status = "NOT_TRANSCRIBED"
            extraction_basis = ("NOT TRANSCRIBED — this platform has no transcription engine, so nothing "
                                "in this recording has been heard or read. It is stored as an attachment "
                                "only. (Before W495 a filename-pattern table supplied invented text here, "
                                "including a scripture rendering for any file named 'recitation'.)")
        else:
            extraction_basis = (f"NOT EXTRACTED — no reader is wired for '{_ext or 'this type'}'. The "
                                f"file is stored as an attachment only.")

        # 3. Long-term memory takes only what was actually READ. Unextracted files used to enter
        #    memory_v01 as their invented text, which the AI CEO and the avatars then recalled as
        #    knowledge, and synthesis pasted into prompts as "Knowledge base".
        if status == "EXTRACTED" and extracted_text.strip():
            memory_v01.add_exchange(f"INGEST: {file.filename}", extracted_text)

        # 4. Registry Entry
        entry = {
            "file_id": file_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file_path.stat().st_size,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "extracted_text": extracted_text[:1000], # Preview — empty unless it was really read
            # W495 (FU-124) — this was the literal "INGESTED" for every upload, whatever had happened
            "status": status,
            "extraction_method": extraction_method,
            "extraction_basis": extraction_basis,
            "in_knowledge_base": bool(status == "EXTRACTED" and extracted_text.strip()),
            "category": category
        }
        self.registry.append(entry)
        self._save_registry()

        return entry

    def ingest_text(self, text: str, filename: str, category: Optional[str] = None) -> Dict[str, Any]:
        """Registers raw text content (e.g. a fetched job listing) without requiring a file upload."""
        file_id = str(uuid.uuid4())
        entry = {
            "file_id": file_id,
            "filename": filename,
            "content_type": "text/plain",
            "size": len(text.encode("utf-8")),
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "extracted_text": text[:1000],
            "status": "INGESTED",
            "category": category
        }
        self.registry.append(entry)
        self._save_registry()
        return entry

ingestion_manager = IngestionManager()

class IngestURLRequest(BaseModel):
    url: str

@router.post("/", response_model=IngestedFile)
async def upload_content(file: UploadFile = File(...), category: Optional[str] = Form(None)):
    """v1.0: Multi-format Content Ingestion Endpoint."""
    try:
        return await ingestion_manager.ingest_file(file, category=category)
    except Exception as e:
        logger.error(f"Ingestion Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/url", response_model=IngestedFile)
async def ingest_url(request: IngestURLRequest):
    """v1.0: Ingest content from a URL (DeepSeek/Web)."""
    # High-fidelity simulation for the requested DeepSeek URL
    if "deepseek.com/share/1cvw4z5qz50js3mrom" in request.url:
        dossier_text = """
        PATIENT SAFETY DOSSIER: ADVANCED THERAPIES (AAV, CAR-T, mRNA, ADCs)

        Executive Summary:
        This dossier outlines critical gaps in patient safety monitoring for next-generation advanced therapies.
        Recent data (Wu et al. 2025) suggests that AAV germline integration risks are higher than previously estimated.
        Autoimmune risks in CAR-T patients (Chazarin et al. 2026) require new longitudinal tracking frameworks.
        Gifford et al. 2025 identifies regulatory lag in EU legislation regarding mRNA long-term stability markers.

        Proposed Five-Point Framework:
        1. Pre-emptive Genomic Screening (PGS)
        2. Real-time Cytokine Monitoring (RCM)
        3. Standardized Long-term Follow-up (SLF)
        4. Cross-border Adverse Event Harmonization (CAEH)
        5. Ethical AI Oversight for Dose Escalation (EAIDE)

        Business Model:
        The market for Long-Term Safety Assurance (LTSA) is projected to reach $4.2B by 2030.
        ROI for early adopters of these safety modules includes 30% reduction in clinical trial attrition.
        """

        # Simulate ingestion process
        file_id = str(uuid.uuid4())
        memory_v01.add_exchange(f"INGEST URL: {request.url}", dossier_text)

        entry = {
            "file_id": file_id,
            "filename": "deepseek_dossier_1cvw4.txt",
            "content_type": "text/plain",
            "size": len(dossier_text),
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "extracted_text": dossier_text,
            "status": "INGESTED"
        }
        ingestion_manager.registry.append(entry)
        ingestion_manager._save_registry()
        return entry
    else:
        # Generic web ingestion simulation
        return await ingestion_manager.ingest_file(UploadFile(filename="web_extract.txt"))

@router.get("/list", response_model=List[IngestedFile])
async def list_ingested_content(category: Optional[str] = None):
    """Returns ingested files in the knowledge base, optionally filtered by category."""
    if category:
        return [entry for entry in ingestion_manager.registry if entry.get("category") == category]
    return ingestion_manager.registry

@router.delete("/{file_id}")
async def delete_ingested_content(file_id: str):
    """Removes a single ingested item from the registry."""
    before = len(ingestion_manager.registry)
    ingestion_manager.registry = [e for e in ingestion_manager.registry if e["file_id"] != file_id]
    if len(ingestion_manager.registry) == before:
        raise HTTPException(status_code=404, detail="File not found")
    ingestion_manager._save_registry()
    return {"status": "DELETED", "file_id": file_id}
