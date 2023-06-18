import React, { useState } from "react";
import { Container, Button, Stack, Input} from '@mui/material';

const MainPage = () => {
    //const [query, setQuery] = useState("");

    return (
        <>
            <Stack spacing={2} direction="row" style={{display: 'flex', justifyContent: 'flex-end'}}>
                <Button variant="contained">Record</Button>
                <Button variant="outlined">Logout</Button>
            </Stack>
            <Container maxWidth="md" sx={{ mt: 20 }}>
                <Input fullWidth placeholder="What are you looking for?" />
            </Container>
        </>
    );
};

export default MainPage;