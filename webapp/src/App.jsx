import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/eurajoki.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
      </div>
      <h1>Eurajoki</h1>
      <div className="card">
        <input></input>
        <button onClick={() => setCount((count) => count + 1)}>Etsi</button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
