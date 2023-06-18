import React, { useState } from 'react';
import { Button, Stack, Input } from '@mui/material';

const Upload = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [error, setError] = useState(false);
    const [fileType, setFileType] = useState(0) // 0 is nothing, 1 is video, 2 is audio
    const [success, setSuccess] = useState(false)

    const handleFileChange = (event) => {
        var file = event.target.files[0]
        if (file.type == 'audio/wav') {
            setSelectedFile(event.target.files[0]);
            setFileType(2)
            setError(false)
        } else if (file.type == 'video/mp4') {
            setSelectedFile(event.target.files[0]);
            setFileType(1)
            setError(false)
        } else {
            document.getElementById("file-input").value = ''
            setError(true);
            setSelectedFile(null);
            setFileType(0)
            setSuccess(false)
        }
    };

    const handleUpload = () => {
        document.getElementById("file-input").value = ''
        if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);

            if (fileType == 1) {
                fetch('http://localhost:5000/video', {
                    method: 'POST',
                    body: selectedFile,
                    mode: 'no-cors',
                }).then(console.log("sent to backend video"))
                setSuccess(true)
                setFileType(0)
                setError(0)
                setSelectedFile(null)
                //video
            } else {
                fetch('http://localhost:5000/audio', {
                    method: 'POST',
                    body: selectedFile,
                    mode: 'no-cors',
                }).then(
                    console.log("sent to backend audio")
                )
                setSuccess(true)
                setFileType(0)
                setError(0)
                setSelectedFile(null)
            }
        }
    };

    return (
        <div>
            <Stack direction="row" spacing={2}>
                <Button variant="contained" component="label">
                    Choose File
                    <Input id='file-input' type="file" onChange={handleFileChange} />
                </Button>
                <Button variant="contained" onClick={handleUpload}>Upload</Button>
            </Stack>
            <p>{error ? "Invalid file type" : ""}</p>
            <p>{success ? "Successfully uploaded" : ""}</p>
        </div>
    );
};

export default Upload;