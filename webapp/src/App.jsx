import { useState } from "react";
import viteLogo from "/eurajoki.svg";
import "./App.css";
import Hakukentta from "./controls/Hakukentta.jsx";
import asukkaat from "./data/eurajoki.json";

function App() {
  const [count, setCount] = useState(0);

  return count == 0 ? (
    <div className="etusivu">
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Eurajoen vaakuna" />
        </a>
      </div>
      <h1>Eurajoki</h1>
      <div className="card">
        <Hakukentta etsi={() => setCount(1)} />
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  ) : (
    <>
      <img src={viteLogo} className="slogo" alt="Eurajoen vaakuna" />
      <Hakukentta />
      <div className="card">
        {asukkaat.map((talo) => (
          <li>{talo.sukunimi}</li>
        ))}
      </div>
    </>
  );
}

export default App;
