import React, { useState } from "react";
import { Container, Button, Stack, Input} from '@mui/material';
import DateTime from "./DateTime";
import InputTabs from "./InputTabs"

const MainPage = () => {
    //const [query, setQuery] = useState("");

    return (
        <>
            <DateTime />  
            <h1 style={{textAlign: "center"}}>What's on your mind?</h1>
            <InputTabs />
        </>
    );
};

export default MainPage;