from datetime import datetime, timezone
from app.models import db

class Document(db.Model):
    """Secure document storage metadata model."""
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False, index=True)
    document_type = db.Column(db.String(60), nullable=False)  # RC, Insurance, PUCC, Invoice, Other
    filename = db.Column(db.String(255), nullable=False)       # Secure randomized disk identifier
    original_filename = db.Column(db.String(255), nullable=False)
    secure_storage_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False, default=0)  # size in bytes
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    vehicle = db.relationship(
        'Vehicle',
        backref=db.backref('documents', lazy=True, cascade='all, delete-orphan', order_by='Document.uploaded_at.desc()')
    )

    def formatted_size(self) -> str:
        """Returns human readable file size like '1.2 MB' or '340 KB'."""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"

    def __repr__(self):
        return f"<Document {self.document_type} {self.original_filename}>"
