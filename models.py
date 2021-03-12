from datetime import datetime
from config import db, ma

class Participant(db.Model):
    __tablename__ = "participant"
    study_id = db.Column('study_id', db.String(100), primary_key=True)
    study = db.Column('study', db.String(100))
    oauth_token = db.Column(db.String(100))
    oauth_token_secret = db.Column(db.String(100))
    oauth_verifier = db.Column(db.String(100))
    authorization_redirect_url = db.Column(db.String(500))
    user_oauth_token = db.Column(db.String(100))
    user_oauth_token_secret = db.Column(db.String(100))
    create_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class ParticipantSchema(ma.Schema):
    class Meta:
        model = Participant
        sqla_session = db.session