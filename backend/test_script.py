import json
from hume_embeding import (
    processChunks,
    combineFullDataFromJournal,
    getEmbeddingsLanguage,
)
from pprint import pprint


# EDIT HERE FOR A SINGLE BACKEND CALL
def stimulateSingleUploadCall(userInfo, path):
    # Assumes it has been uploaded to S3 bucket and is in metadata database
    file = open(path, "r")
    response = json.load(file)
    processedLanguage = processChunks(response, model="language")
    # Contains all necessary metadata here
    fullData = combineFullDataFromJournal(userInfo, processedLanguage)
    print(
        "journalId",
        fullData["journal_id"],
        "date",
        fullData["date"],
        "numChunks",
        len(fullData["chunks"]),
    )


def runSimulator():
    for i in range(1, 10):
        # getEmbeddingsLanguage(f"resources/text{i}.txt", i)
        if i < 6:
            userInfo = {
                "userId": 0,
                "type": "text",
                "date": f"2022-12-{i*5}",
                "time": f"{10 + i}:00",
                "journalId": i,
            }
        else:
            userInfo = {
                "userId": 0,
                "type": "text",
                "date": f"2023-01-{(i-5)*5}",
                "time": f"{10 + i}:00",
                "journalId": i,
            }
        stimulateSingleUploadCall(userInfo, f"embeddings/text{i}.json")

    # Video 1 (back home)
    userInfo = {
        "userId": 0,
        "type": "video",
        "date": "2022-12-25",
        "time": "13:00",
        "journalId": 10,
    }
    stimulateSingleUploadCall(userInfo, f"embeddings/video{1}.json")

    # Video 2 (breakup)
    userInfo = {
        "userId": 0,
        "type": "video",
        "date": "2023-01-14",
        "time": "20:00",
        "journalId": 11,
    }
    stimulateSingleUploadCall(userInfo, f"embeddings/video{2}.json")

    # Audio 1 (exams)
    userInfo = {
        "userId": 0,
        "type": "audio",
        "date": "2022-12-04",
        "time": "20:00",
        "journalId": 12,
    }
    stimulateSingleUploadCall(userInfo, f"embeddings/audio{1}.json")

    # Audio 2 (dull day after europe)
    userInfo = {
        "userId": 0,
        "type": "audio",
        "date": "2023-01-07",
        "time": "08:00",
        "journalId": 13,
    }
    stimulateSingleUploadCall(userInfo, f"embeddings/audio{2}.json")


# def upload():
#     getEmbeddingsLanguage(f"resources/record1.m4a", 1)
#     getEmbeddingsLanguage(f"resources/record2.m4a", 2)


# upload()
runSimulator()
