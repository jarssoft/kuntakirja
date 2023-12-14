import css from "./Tiedot.module.css";
import { Link } from "react-router-dom";

function Tietosivu({ talo }) {
  const getImageName = (perheId) =>
    `http://ohjelmakartta.fi/kuntakirja/photos/${
      Math.floor(perheId / 4) + 69
    }.png-${perheId % 4}.jpg`;

  return (
    <span>
      <div className="card">
        <h1 className={css.nimi}>{talo.tontti ? `${talo.tontti}` : ""}</h1>
        <div>
          Eurajoki &gt; <Link to={`/haku/${talo.kyla}`}>{talo.kyla}</Link>
          {talo["pinta-ala"] && talo["pinta-ala"] > 1
            ? ` (${talo["pinta-ala"]} ha)`
            : ""}
        </div>
      </div>

      <div className="card">
        <img className={css.isokuva} src={getImageName(talo.id)}></img>
      </div>

      <div className={css.tooltip}>
        {talo.rakennusvuosi ? (
          <p className={css.tooltipp}>
            <span className={css.attributeName}>Rakennusvuosi </span>
            <span className={css.attributeValue}>{talo.rakennusvuosi}</span>
          </p>
        ) : (
          ""
        )}
        {talo.rakennusmateriaali ? (
          <p className={css.tooltipp}>
            <span className={css.attributeName}>Materiaali </span>
            <span className={css.attributeValue}>
              {talo.rakennusmateriaali.map((materiaali) => (
                <span>{materiaali} </span>
              ))}
            </span>
          </p>
        ) : (
          ""
        )}
        {talo["laajennus/remontti"] ? (
          <p className={css.tooltipp}>
            <span className={css.attributeName}>Remontti </span>
            <span className={css.attributeValue}>
              {talo["laajennus/remontti"]}
            </span>
          </p>
        ) : (
          ""
        )}

        {talo["pinta-ala"] ? (
          <p className={css.tooltipp}>
            <span className={css.attributeName}>Pinta-ala </span>
            <span className={css.attributeValue}>
              {talo["pinta-ala"]} hehtaaria
            </span>
          </p>
        ) : (
          ""
        )}

        {talo["tuotanto"] ? (
          <p className={css.tooltipp}>
            <span className={css.attributeName}>Tuotanto </span>
            <span className={css.attributeValue}>
              {talo["tuotanto"].map((tuote) => (
                <span>{tuote}</span>
              ))}
            </span>
          </p>
        ) : (
          ""
        )}

        {talo["omistajanvaihdos"] ? (
          <p className={css.tooltipp}>
            <span className={css.attributeName}>Omistajavaihdos </span>
            <span className={css.attributeValue}>
              {talo["omistajanvaihdos"]}
            </span>
          </p>
        ) : (
          ""
        )}

        {talo.id ? (
          <p className={css.tooltipp}>
            <span className={css.attributeName}>Kirjan sivu </span>
            <span className={css.attributeValue}>
              {Math.floor(talo.id / 4) + 69}
            </span>
          </p>
        ) : (
          ""
        )}
      </div>

      {/*
  <p className={css.todos}>
    {toDo.teksti}
  </p>
  */}
    </span>
  );
}

export default Tietosivu;
