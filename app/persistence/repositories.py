from sqlalchemy.orm import Session
from typing import Any


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def log(self, payload: Any) -> None:
        self.db.execute(
            "INSERT INTO audit_ledger (payload) VALUES (:payload)",
            {"payload": payload},
        )
        self.db.commit()
