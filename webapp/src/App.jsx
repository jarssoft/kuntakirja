import { useState, useEffect } from "react";
import viteLogo from "/eurajoki.svg";
import "./App.css";
import Hakukentta from "./controls/Hakukentta.jsx";
import Hakutulos from "./controls/Hakutulos.jsx";
import Tietosivu from "./controls/Tietosivu.jsx";
import Ylapalkki from "./controls/Ylapalkki.jsx";
//import asukkaat from "./data/eurajoki.json";
import noteService from "./services/asukkaat";
import { useMatch, Routes, Route, useNavigate, Link } from "react-router-dom";

function App() {
  const [asukkaat, setAsukkaat] = useState([]);
  const navigate = useNavigate();
  const match = useMatch("/talo/:id");
  const talo = match
    ? asukkaat.filter((talo) => talo.id == match.params.id)[0]
    : null;
  const match2 = useMatch("/haku/:id");
  const hakusana = match2 ? match2.params.id : null;

  //console.log(match);

  const hae = (haku) => {
    console.log(haku);
    if (haku && haku != "") {
      navigate("/haku/" + haku);
    }
  };

  useEffect(() => {
    if (hakusana) {
      noteService.getAll(hakusana).then((response) => {
        console.log(response.data);
        setAsukkaat(response.data);
      });
    }
  }, [hakusana]);

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
                  <p>Etsi taloa, tonttia tai kylää.</p>
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
                {asukkaat.length > 29 ? (
                  <div className="card">
                    Ladattiin 30 ensimmäistä. Tarkenna hakua.{" "}
                  </div>
                ) : (
                  <div className="card">
                    Kaikki tulokset hakusanalla '{hakusana}'.
                  </div>
                )}
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
