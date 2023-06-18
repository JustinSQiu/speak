import json
from hume import HumeBatchClient
from hume.models.config import FaceConfig, ProsodyConfig, LanguageConfig
import asyncio
from pprint import pprint
from pathlib import Path
from uuid import uuid4


def processChunks(response, model="language"):
    results = response[0].get("results")
    errors = results.get("errors")
    if len(errors) > 0:
        print("Errors: ", errors)
        raise ValueError(errors)
    chunks = results["predictions"][0]["models"][model]["grouped_predictions"][0][
        "predictions"
    ]
    processed = []
    for chunk in chunks:
        # pprint(chunk)
        md = {
            "confidence": chunk["confidence"],
            "text": chunk["text"],
            "chunk_id": str(uuid4()),
        }
        if chunk.get("time") is not None:
            md["start_time"] = chunk["time"]["begin"]
            md["end_time"] = chunk["time"]["end"]

        unProcessedEmotions = (
            chunk["emotions"][:48] if len(chunk["emotions"]) > 48 else chunk["emotions"]
        )
        emotions = []

        for emotion in unProcessedEmotions:
            score = emotion["score"]
            emotions.append(score)
        md["emotions"] = emotions
        processed.append(md)
    return processed


def getEmbeddingsLanguage(path):
    client = HumeBatchClient("cRASOeAzmGOUQveP3vrNBb1MpSEPGejdvWPG8UAQYrEkOrpu")
    # Check if file exists
    absolute_path = Path(path).resolve()
    if not absolute_path.exists():
        raise ValueError("File does not exist")
    urls = [str(absolute_path)]
    # What other configs are there to use?
    config = [LanguageConfig(granularity="utterance")]

    job = client.submit_job(None, config, files=urls)

    details = job.await_complete()
    print("Details status", details.get_status())
    response = job.get_predictions()
    job.download_predictions(f"test.json")
    processedLanguage = processChunks(response, model="language")

    return processedLanguage


def combineFullDataFromJournal(journalMetadata, processedChunks):
    return {
        "user_id": journalMetadata["user_id"],
        "entry_id": journalMetadata["entry_id"],
        "type": journalMetadata["type"],
        "date": journalMetadata["date"],
        "time": journalMetadata["time"],
        "chunks": processedChunks,
    }


def main():
    # file = open("predictions.json", "r")
    # response = json.load(file)[0]
    # results = response.get("results")
    # errors = results.get("errors")
    # if len(errors) > 0:
    #     print("Errors: ", errors)
    #     raise ValueError(errors)
    # chunks = results["predictions"][0]["models"]["face"]["grouped_predictions"][0][
    #     "predictions"
    # ]
    # relative_path = "resources/video.mp4"
    # absolute_path = str(Path(relative_path).resolve())
    # if Path(relative_path).resolve().exists():
    #     processed = getEmbeddingsLanguage(absolute_path)
    #     pprint(processed)
    # else:
    #     print("File does not exist")

    # text = "Today was a terrible day, it was terrible. I have never had a worst day, and it's all because of her!"
    # getEmbeddings(type="text", text=text)

    file = open("predictions_videoaudio.json", "r")
    response = json.load(file)
    processed = processChunks(response)
    print(processed)


# if __name__ == "__main__":
#     main()

# getEmbeddingsLanguage(
#     "local.mp4",
# )
