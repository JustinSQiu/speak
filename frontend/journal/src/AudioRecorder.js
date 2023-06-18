import { useReactMediaRecorder } from "react-media-recorder";
import { getStorage, ref, uploadBytes } from "firebase/storage"
import {useState} from 'react'
import 'firebase/firestore';
import { initializeApp } from 'firebase/app'

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

const AudioRecorder = () => {

    const [blob, setBlob] = useState(null);

    const handleStop = (blobUrl, blob) => {
        setBlob(blob)
        fetch('http://localhost:5000/audio', {
            method: 'POST',
            body: blob,
            mode: 'no-cors',
        }).then(console.log("sent to backend"))
    }

    const { status, startRecording, stopRecording, mediaBlobUrl } =
        useReactMediaRecorder({ video: false, onStop: handleStop });

    return (
        <div>
            <p>{status}</p>
            <button onClick={startRecording}>Start Recording</button>
            <button onClick={stopRecording}>Stop Recording</button>
            <audio src={mediaBlobUrl} controls autoPlay loop />
        </div>
    );
};

export default AudioRecorder;