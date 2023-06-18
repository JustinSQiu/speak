import logo from './logo.svg';
import './App.css';
import fetchFromEndpoint from './utils';
import MainPage from './MainPage';
import { useState, useRef } from "react";
import VideoRecorder from './VideoRecorder'
import AudioRecorder from './AudioRecorder'
import TextMemo from './TextMemo'
import InputTabs from './InputTabs'

const App = () => {
    return (
        <MainPage />
    );
};

export default App;