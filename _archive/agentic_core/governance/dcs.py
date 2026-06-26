import logging
import datetime
from typing import Dict, Any, List, Optional
from agentic_core.ueg.ueg_manager import UEGManager

logger = logging.getLogger(__name__)

class DCSDocument:
    """Represents a version-controlled document in the DCS."""
    def __init__(self, doc_id: str, title: str, content: str, author: str):
        self.doc_id = doc_id
        self.title = title
        self.versions: List[Dict[str, Any]] = []
        self.status = "DRAFT"
        self.checked_out_by: Optional[str] = None
        self.add_version(content, author, "Initial Version")

    def add_version(self, content: str, author: str, comment: str):
        version_num = len(self.versions) + 1
        self.versions.append({
            "version": version_num,
            "timestamp": datetime.datetime.now().isoformat(),
            "content": content,
            "author": author,
            "comment": comment
        })
        logger.info(f"DCS: Document '{self.title}' updated to version {version_num} by {author}.")

    def approve(self, approver: str):
        self.status = "APPROVED"
        logger.info(f"DCS: Document '{self.title}' APPROVED by {approver}.")

class DocumentControlSystem:
    """
    ARTICLE 346, 359 & 531: Document Control System (DCS).
    Integrates with UEG for versioned storage and approval workflows.
    """
    def __init__(self, ueg_manager: Optional[UEGManager] = None):
        self.ueg = ueg_manager or UEGManager()
        self.documents: Dict[str, DCSDocument] = {}
        self.snapshots: List[Dict[str, Any]] = []

    def check_in(self, doc_id: str, title: str, content: str, author: str, comment: str):
        """Checks in a new version of a document."""
        if doc_id not in self.documents:
            self.documents[doc_id] = DCSDocument(doc_id, title, content, author)
        else:
            doc = self.documents[doc_id]
            if doc.checked_out_by and doc.checked_out_by != author:
                raise PermissionError(f"Document {doc_id} is checked out by {doc.checked_out_by}")
            doc.add_version(content, author, comment)
            doc.checked_out_by = None

        # Synchronize with UEG
        self.ueg.add_audit_log("DCS", f"Document {title} version {len(self.documents[doc_id].versions)} checked in by {author}", {
            "doc_id": doc_id,
            "title": title,
            "version": len(self.documents[doc_id].versions),
            "author": author,
            "comment": comment
        })

    def check_out(self, doc_id: str, user: str):
        """Checks out a document for editing."""
        if doc_id not in self.documents:
            raise FileNotFoundError(f"Document {doc_id} not found.")
        doc = self.documents[doc_id]
        if doc.checked_out_by:
            raise PermissionError(f"Document {doc_id} is already checked out by {doc.checked_out_by}")
        doc.checked_out_by = user
        logger.info(f"DCS: Document '{doc_id}' checked out by {user}.")

    def approve_document(self, doc_id: str, approver: str):
        """Formally approves a document version."""
        if doc_id not in self.documents:
            raise FileNotFoundError(f"Document {doc_id} not found.")
        self.documents[doc_id].approve(approver)

    def snapshot_constitution(self, version: str, content: str):
        """ARTICLE 531: Takes a formal snapshot of the constitution."""
        snapshot = {
            "version": version,
            "timestamp": datetime.datetime.now().isoformat(),
            "content": content,
            "type": "CONSTITUTION_SNAPSHOT"
        }
        self.snapshots.append(snapshot)
        self.check_in(f"CONST_{version}", f"Constitution v{version}", content, "GrandSynthesisEngine", "Automated Snapshot")
        logger.info(f"DCS: Snapshot of Constitution v{version} taken.")

    def get_document_history(self, doc_id: str) -> List[Dict[str, Any]]:
        if doc_id not in self.documents:
            return []
        return self.documents[doc_id].versions
