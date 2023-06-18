import { useReactMediaRecorder } from "react-media-recorder";
import { useState } from 'react'
import 'firebase/firestore';

const TextMemo = () => {

    const [inputValue, setInputValue] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
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
        <form onSubmit={handleSubmit}>
            <input type="text" value={inputValue} onChange={handleChange} />
            <button type="submit">Submit</button>
        </form>
    );
};

export default TextMemo;