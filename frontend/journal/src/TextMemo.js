import { useReactMediaRecorder } from "react-media-recorder";
import { useState } from 'react'
import 'firebase/firestore';
import { TextField, Box, Button, Typography, Stack } from "@mui/material";
import { FormControl } from "@mui/base";

const TextMemo = () => {

    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        // Perform desired action with the form data
        console.log('Form submitted with value:', inputValue);
        fetch('http://localhost:5000/text', {
            method: 'POST',
            body: inputValue,
            mode: 'no-cors',
        }).then(console.log("sent to backend"))
        // Reset the input value
        setInputValue('');
    };

    const handleChange = (event) => {
        setInputValue(event.target.value);
    };

    const style = {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    }

    return (
        <div style={style}>
            <Box
                sx={{
                    width: '80%',
                    display: 'flex',
                    justifyContent: 'center',
                    flexDirection: 'column'
                }}
            >
                <TextField
                    // sx={ }
                    id="outlined-multiline-static"
                    label="Journal your Thoughts"
                    multiline
                    defaultValue=""
                    value={inputValue}
                    onChange={handleChange}
                />
                <Button onClick={handleSubmit} variant="contained">
                    Submit Entry
                </Button>
            </Box>
        </div>


    );
};

export default TextMemo;