import logo from './logo.svg';
import './App.css';
import fetchFromEndpoint from './utils';

function App() {

  const test = async () => {
    const data = await fetchFromEndpoint("", "GET");
    console.log(data);
  }

  return (
    <div className="App">
      <button onClick={test}>Test</button>
    </div>
  );
}

export default App;
