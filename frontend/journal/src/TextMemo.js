import { useReactMediaRecorder } from "react-media-recorder";
import { useState } from 'react'
import 'firebase/firestore';
import { TextField, Box, Button, Typography, Stack } from "@mui/material";
import { FormControl } from "@mui/base";

const TextMemo = () => {

    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('submitted')
        // Perform desired action with the form data
        console.log('Form submitted with value:', inputValue);
        // Reset the input value
        fetch('http://localhost:5000/text', {
            method: 'POST',
            body: inputValue,
            mode: 'no-cors',
        }).then(console.log("sent to backend"))
        setInputValue('');
    };

    const handleChange = (event) => {
        setInputValue(event.target.value);
    };

    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: 'center',
            }}
        >
                <TextField
                    sx={{ width: '75%'}}
                    id="outlined-multiline-static"
                    label="Journal your Thoughts"
                    multiline
                    defaultValue=""
                    onChange={handleChange}
                    onSubmit={handleSubmit}
                />

                <Button onClick={handleSubmit} variant="contained">
                    Submit Entry
                </Button>
        </Box>

    );
};

export default TextMemo;