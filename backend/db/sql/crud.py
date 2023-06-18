from db.sql.models import db, Sentence
from constants import EMOTIONS

def create_sentence(user_id, entry_id, sentence_id, topic_id, video_link, timestamp, start_time, end_time, transcript_text, 
                    emotions):
    
  sentence = Sentence()
  sentence.user_id = user_id
  sentence.entry_id = entry_id
  sentence.sentence_id = sentence_id
  sentence.topic_id = topic_id
  sentence.video_link = video_link
  sentence.timestamp = timestamp
  sentence.start_time = start_time
  sentence.end_time = end_time
  sentence.transcript_text = transcript_text
  
  # Set emotions dynamically
  for i, name in enumerate(EMOTIONS):
      setattr(sentence, name, emotions[i])

  db.session.add(sentence)
  db.session.commit()
  return sentence

def get_all_sentences():
  return Sentence.query.all()