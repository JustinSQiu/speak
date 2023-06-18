import React, { useState } from 'react';
import { Button, Stack, Input, Alert, Box } from '@mui/material';

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
            setError(true);
            setSelectedFile(null);
            setFileType(0)
            setSuccess(false)
        }
    };

    const handleUpload = () => {
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

    const erroralert = <Alert severity="error">Invalid file type</Alert>
    const successalert = <Alert severity="success">Successfully uploaded</Alert>

    const style = {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    }

    return (
        <div style={style}>
            <div>{error ? erroralert : ""}</div>
            <div>{success ? successalert : ""}</div>
            <Stack sx={{
                m: 1,
                width: '20%',
                display: 'flex',
                justifyContent: 'center',
                // flexDirection: 'column'
            }} direction="row" spacing={2}>
                <Button variant="outlined" component="label">
                    Choose File
                    <input hidden type="file" onChange={handleFileChange} />
                </Button>
                <Button variant="text" onClick={handleUpload}>Upload</Button>
            </Stack>
            <Alert severity="info">Filename: {selectedFile ? selectedFile.name : "No file selected"} </Alert>
        </div>
    );
};

export default Upload;