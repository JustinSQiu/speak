import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";
import { textAlign } from "@mui/system";

const SearchBar = ({ onSearch }) => {
    const [searchTerm, setSearchTerm] = useState("");
    const [answer, setAnswer] = useState("");
    const [justAsked, setJustAsked] = useState(false);

    const handleChange = (event) => {
        setJustAsked(false);
        setSearchTerm(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        const query = searchTerm
        console.log(searchTerm)
        const response = await fetch('http://localhost:5000/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
            mode: 'cors',
        });
        console.log(response)
        const data = await response.json();
        console.log(data)
        setAnswer(data)
        setJustAsked(true);
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
                    fullWidth
                    id="outlined-basic"
                    label="Ask me anything"
                    variant="outlined"
                    value={searchTerm}
                    onChange={handleChange} />

                {!justAsked ? <Button onClick={handleSubmit} variant="contained">
                    Search your thoughts
                </Button> : <></>}

                {answer != '' ? (<><br /><TextField
                    sx={{ backgroundColor: '#e6eeff', }}
                    id="outlined-multiline-static"
                    fullWidth
                    multiline
                    label="A look into the past"
                    value={answer} /></>) : <></>}

            </Box>
        </div>

    );
};

export default SearchBar;