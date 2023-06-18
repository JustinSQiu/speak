# Speak: Your Life, Interpreted

## Inspiration

Our team has always found journaling to be a therapeutic and reflective process, but the barrier to entry and the static nature of traditional journals can be limiting and turn people away from journalling their thoughts. We aim to create a "living artifact" - a journal that not only stores memories but allows users to interact with them.

## Functionality

Speak is designed to be a user-friendly, interactive journal. Here's how it works:

1. **Input Submission:** Users submit their entries in video, audio, or text format. The exact pipeline depends on the data format, because Hume has models such as speech prosody and facial expression in addition to language that offer more emotional insights, as compared to only language for text. 

2. **Processing:** Each entry is processed for emotions, semantic meaning, and metadata using Hume’s API and OpenAI’s embedding generation models (ada-002).
Hume’s API outputs 48 emotional features for every ~3-5 second chunk of audio/video/text input. 

3. **Data Storage:** The processed data is stored in two Pinecone databases (one for sentence embeddings and one for emotion embeddings) and SQLite (for metadata and faster querying of top emotions).

4. **Data Chunking:** Data is chunked by sentence for processing. Each sentence is set to be 20-30 words long - which we believe is the appropriatelength to capture one main idea in a personal blog. 

We also conduct clustering of the sentences’s embeddings, to come up with clusters of similar semantic meaning, which we call experiences.

5. **Querying:** Users can ask questions like "What was my most angry week on average?" or "When did I first meet my boyfriend?". Our OpenAI agent (Langchain wrapper) uses OpenAI’s new function API to intelligently decide whether to do a SQL metadata search, emotion vector database or content vector database search, to provide the answer. Experiences (obtained from the clustering algorithms detailed above) will be ranked based on the ranking of top sentences and top emotions that are retrieved. Our ranking algorithms take into account both the embedding of the whole experience and the individual sentences.

6. **User Output:** Speak summarizes data in the case of text, and splices video to create new video in the case of video/audio.

## Takeaways and Learnings

- The project was eye-opening in terms of what AI can do, especially in simulating emotional intelligence. The rapid evolution of machine learning, particularly in areas like emotion recognition, was fascinating to witness.

- Organizing and diagramming the project before starting to build saved us a lot of time. It highlighted the importance of efficient teamwork and division of labor in group projects.

## Challenges

- Bringing together the backend, frontend, and various scripts and pipelines was a significant challenge due to the many APIs, frameworks, and different models with different inputs and outputs that we used.

- Setting up the input pipeline for video data was particularly challenging.

## Local Deployment Instructions

BACKEND:
```cd backend```

1. Setup virtual env:
https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
(PLEASE ENTER INTO VIRTUAL ENV FIRST)

2.  ~ pip install -r requirements.txt

3. to run: flask run --host=0.0.0.0 --debug

FRONTEND: 
``` frontend/journal```

1. npm run start 
OR
npm start