from flask_sqlalchemy import SQLAlchemy
from constants import EMOTIONS

db = SQLAlchemy()

class Sentence(db.Model):
  user_id = db.Column(db.String(50), primary_key=True)
  entry_id = db.Column(db.String(50), primary_key=True)
  sentence_id = db.Column(db.String(50), primary_key=True)
  topic_id = db.Column(db.String(50), nullable = True)
  video_link = db.Column(db.String(255), nullable = True)
  timestamp = db.Column(db.String(255))
  start_time = db.Column(db.Float, nullable = True)
  end_time = db.Column(db.Float, nullable = True)
  transcript_text = db.Column(db.String(4096))
  
  def __init__(self):
    for name in EMOTIONS:
      setattr(Sentence, name, db.Column(db.Float, nullable=False, default=False))

  def __repr__(self):
      return f"<{self.user_id}-{self.entry_id}-{self.sentence_id}>"
    