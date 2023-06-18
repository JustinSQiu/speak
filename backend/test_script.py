import json
from hume_embedding import (
    processChunks,
    combineFullDataFromJournal,
    getEmbeddingsLanguage,
)
from pprint import pprint


# EDIT HERE FOR A SINGLE BACKEND CALL
def simulateSingleUploadCall(entryInfo):
    # Assumes it has been uploaded to S3 bucket and is in metadata database
    file = open(entryInfo['path'], "r")
    response = json.load(file)
    processedLanguage = processChunks(response, model="language")
    # Contains all necessary metadata here
    fullData = combineFullDataFromJournal(entryInfo, processedLanguage)
    
    return fullData
    
    # Save fullData as a json
    # with open(f"test/{userInfo['entry_id']}.json", "w") as outfile:
    #     json.dump(fullData, outfile)
    print(
        "entry_id",
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
            entryInfo = {
                "user_id": 0,
                "type": "text",
                "date": f"2022-12-{i*5}",
                "time": f"{10 + i}:00",
                "entry_id": i,
                "path": f"embeddings/text{i}.json"
            }
        else:
            entryInfo = {
                "user_id": 0,
                "type": "text",
                "date": f"2023-01-{(i-5)*5}",
                "time": f"{10 + i}:00",
                "entry_id": i,
                "path": f"embeddings/text{i}.json"
            }
        simulateSingleUploadCall(entryInfo)

    # Video 1 (back home)
    entryInfo = {
        "user_id": 0,
        "type": "video",
        "date": "2022-12-25",
        "time": "13:00",
        "entry_id": 10,
        "path": f"embeddings/video{1}.json"
    }
    simulateSingleUploadCall(entryInfo)

    # Video 2 (breakup)
    entryInfo = {
        "user_id": 0,
        "type": "video",
        "date": "2023-01-14",
        "time": "20:00",
        "entry_id": 11,
        "path": f"embeddings/video{2}.json"
    }
    simulateSingleUploadCall(entryInfo)

    # Audio 1 (exams)
    entryInfo = {
        "user_id": 0,
        "type": "audio",
        "date": "2022-12-04",
        "time": "20:00",
        "entry_id": 12,
        "path": f"embeddings/audio{1}.json"
    }
    simulateSingleUploadCall(entryInfo)

    # Audio 2 (dull day after europe)
    entryInfo = {
        "user_id": 0,
        "type": "audio",
        "date": "2023-01-07",
        "time": "08:00",
        "entry_id": 13,
        "path": f"embeddings/audio{2}.json"
    }
    simulateSingleUploadCall(entryInfo)


# def upload():
#     getEmbeddingsLanguage(f"resources/record1.m4a", 1)
#     getEmbeddingsLanguage(f"resources/record2.m4a", 2)


# upload()
# runSimulator()
