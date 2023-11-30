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
  const navigate = useNavigate();
  const match = useMatch("/talo/:id");
  const talo = match ? asukkaat[match.params.id] : null;
  const match2 = useMatch("/haku/:id");
  const hakusana = match2 ? match2.params.id : null;

  //console.log(match);

  const hae = (haku) => {
    console.log(haku);
    if (haku && haku != "") {
      navigate("/haku/" + haku);
    }
  };

  return (
    <>
      <div>
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
                  <Hakukentta etsi={hae} />
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
            path="/haku/:id"
            element={
              <>
                <Ylapalkki hakusana={hakusana} etsi={hae} />
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
                <Ylapalkki hakusana={hakusana} etsi={hae} />
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
