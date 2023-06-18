import { useReactMediaRecorder } from "react-media-recorder";
import { getStorage, ref, uploadBytes } from "firebase/storage"
import { useState } from 'react'
import 'firebase/firestore';
import { initializeApp } from 'firebase/app'
import { Button } from "@mui/material";
import { Stack } from "@mui/system";

// const firebaseConfig = {
//     apiKey: "AIzaSyBAnQ-KG1AwIlyqJn3npw6xc2qoLWgZbWE",
//     authDomain: "calhacks-a01b9.firebaseapp.com",
//     projectId: "calhacks-a01b9",
//     storageBucket: "calhacks-a01b9.appspot.com",
//     messagingSenderId: "653429600980",
//     appId: "1:653429600980:web:6c574063844b79ef97c141",
//     measurementId: "G-01XXZWF961"
//   };

// Initialize Firebase
// initializeApp(firebaseConfig);
// const storage = getStorage();
// const storageRef = ref(storage, 'videos');

const VideoRecorder = () => {

    const [blob, setBlob] = useState(null);

    const handleStop = (blobUrl, blob) => {
        setBlob(blob)
        // var formData = new FormData();
        var fileName = 'local.mp4'
        // formData.append("blob", blob, fileName)
        const file = new File([blob], fileName, {type: 'video/mp4'})
        fetch('http://localhost:5000/video', {
            method: 'POST',
            body: file,
            mode: 'no-cors',
        }).then(console.log("sent to backend"))
    }

    const { status, startRecording, stopRecording, mediaBlobUrl } =
        useReactMediaRecorder({ video: true, onStop: handleStop });

    return (
        <>
            <p>{status}</p>
            <video src={mediaBlobUrl} controls autoPlay loop />
            <Stack direction="row" spacing={2}>
                <Button onClick={startRecording} variant="contained" color="success">
                    Start Recording
                </Button>
                <Button onClick={stopRecording} variant="outlined" color="error">
                    Stop Recording
                </Button>
            </Stack>
        </>
    );
};

export default VideoRecorder;