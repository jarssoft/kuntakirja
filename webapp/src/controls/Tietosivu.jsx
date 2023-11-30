import css from "./Tiedot.module.css";

function Tietosivu({ talo }) {
  const getImageName = (perheId) =>
    `../../photos/${Math.floor(perheId / 4) + 69}.png-${perheId % 4}.jpg`;

  return (
    <span>
      <div className="card">
        <h1 className={css.nimi}>{talo.tontti ? `${talo.tontti}` : ""}</h1>
        <div>
          Eurajoki &gt; {talo.kyla}
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
              {talo.rakennusmateriaali}
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
