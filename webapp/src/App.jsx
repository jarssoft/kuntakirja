import { useState } from "react";
import viteLogo from "/eurajoki.svg";
import "./App.css";
import Hakukentta from "./controls/Hakukentta.jsx";
import Hakutulos from "./controls/Hakutulos.jsx";
import Tietosivu from "./controls/Tietosivu.jsx";
import Ylapalkki from "./controls/Ylapalkki.jsx";
import asukkaat from "./data/eurajoki.json";
import { useMatch, Routes, Route, useNavigate, Link } from "react-router-dom";

function App() {
  const [count, setCount] = useState(0);
  const navigate = useNavigate();
  const match = useMatch("/talo/:id");
  const talo = match ? asukkaat[match.params.id] : null;

  console.log(match);

  return (
    <>
      <div className="card">
        <Routes>
          <Route
            path="/"
            element={
              <div className="etusivu">
                <div>
                  <img src={viteLogo} className="logo" alt="Eurajoen vaakuna" />
                </div>
                <h1>Eurajoki</h1>
                <div className="card">
                  <Hakukentta etsi={() => navigate("/haku")} />
                  <p>
                    Edit <code>src/App.jsx</code> and save to test HMR
                  </p>
                </div>
                <p className="read-the-docs">
                  Click on the Vite and React logos to learn more
                </p>
              </div>
            }
          />
          <Route
            path="/haku"
            element={
              <>
                <Ylapalkki />
                {asukkaat.map((talo) => (
                  <Hakutulos talo={talo} />
                ))}
              </>
            }
          />
          <Route
            path="/talo/:id"
            element={
              <>
                <Ylapalkki />
                <Tietosivu talo={talo} />
              </>
            }
          />
        </Routes>
      </div>
    </>
  );
}

export default App;
