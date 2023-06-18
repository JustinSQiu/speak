import React, { useState } from "react";
import { TextField } from "@mui/material";
import { textAlign } from "@mui/system";

const SearchBar = ({ onSearch }) => {
    const [searchTerm, setSearchTerm] = useState("");

    const handleChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(searchTerm)
    };

    return (
        <div class="container">
            <div class="centered-div">
                    <TextField
                        fullWidth
                        id="outlined-basic"
                        label="Search your Entries"
                        variant="outlined"
                        value={searchTerm}
                        onChange={handleChange}
                        onSubmit={handleSubmit} />
            </div>
        </div>

    );
};

export default SearchBar;