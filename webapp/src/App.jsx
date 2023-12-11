import { useState, useEffect } from "react";
import viteLogo from "/eurajoki.svg";
import "./App.css";
import Hakukentta from "./controls/Hakukentta.jsx";
import Hakutulos from "./controls/Hakutulos.jsx";
import Tietosivu from "./controls/Tietosivu.jsx";
import Ylapalkki from "./controls/Ylapalkki.jsx";
import kylat from "./data/kylat.json";
import noteService from "./services/asukkaat";
import { useMatch, Routes, Route, useNavigate, Link } from "react-router-dom";

function App() {
  const [asukkaat, setAsukkaat] = useState([]);
  const [asukas, setAsukas] = useState(null);
  const navigate = useNavigate();

  const match = useMatch("/talo/:id");
  const taloid = match ? match.params.id : null;
  const match2 = useMatch("/haku/:id");
  const hakusana = match2 ? match2.params.id : null;

  console.log(taloid);
  console.log(asukas);

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
        setAsukas(null);
      });
    }
  }, [hakusana]);

  useEffect(() => {
    console.log("useEffect" + taloid);
    if (taloid) {
      noteService.get(taloid).then((response) => {
        console.log(response.data);
        setAsukas(response.data);
      });
    }
  }, [taloid]);

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
                  <p>Etsi tilaa, tonttia, kylää tai rakennusvuotta.</p>
                </div>
                <p className="read-the-docs">
                  {kylat.map((kyla) => (
                    <>
                      <Link to={`/haku/${kyla}`}>{kyla}</Link> -{" "}
                    </>
                  ))}
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
                {asukas ? <Tietosivu talo={asukas} /> : <>dad</>}
              </>
            }
          />
        </Routes>
      </div>
    </>
  );
}

export default App;
