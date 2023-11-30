import css from "./Tiedot.module.css";

function Tietosivu({ talo }) {
  const getImageName = (perheId) =>
    `../../photos/${Math.floor(perheId / 4) + 69}.png-${perheId % 4}.jpg`;

  return (
    <span>
      <div className="card">
        <h1 className={css.nimi}>{talo["sukunimi"]}</h1>
        <div>
          Eurajoki &gt; {talo.kyla}
          {talo.tontti ? ` > ${talo.tontti}` : ""}
          {talo["pinta-ala"] && talo["pinta-ala"] > 1
            ? ` (${talo["pinta-ala"]} ha)`
            : ""}
        </div>
      </div>

      <div className="card">
        <img
          className={css.isokuva}
          src={getImageName(talo.asukkaat[0].perhe)}
        ></img>
      </div>

      <div className="card">
        {talo.asukkaat.map((asukas, index) => (
          <>
            <div className={css.asukkaat} key={index}>
              {`${asukas.etunimet.join(" ")}`}
              {/* </div><div className={css.asukkaat}>*/}

              {asukas.osnimi ? ` O.s. ${asukas.osnimi}, ` : " "}
              {asukas.syntymäaika ? `s. ${asukas.syntymäaika} ` : " "}
              {asukas.syntymäpaikka ? asukas.syntymäpaikka : ""}
            </div>
            <div>{asukas.ammatit ? asukas.ammatit.join(", ") : ""}</div>
          </>
        ))}
        <div>
          {talo.liitto
            ? `${talo.liitto.tyyppi} 
           ${talo.liitto.alkaen ? `${talo.liitto.alkaen}` : ""}`
            : ""}
        </div>
      </div>

      {talo.lapset ? (
        <div className="card">
          Lapset:&nbsp;
          {talo.lapset
            .map((lapsi) => lapsi.etunimet[0] + " " + lapsi.syntymäaika)
            .join(", ")}
        </div>
      ) : (
        ""
      )}

      <div className="card">
        Päärakennus:
        {talo.rakennusmateriaali
          ? ` ${talo.rakennusmateriaali.join(", ")} `
          : ""}
        {talo.rakennusvuosi ? ` (${talo.rakennusvuosi})` : ""}
      </div>

      <div className="card">{talo.kuvaus ? <p>{talo.kuvaus}</p> : ""}</div>
      {/*
  <p className={css.todos}>
    {toDo.teksti}
  </p>
  */}
    </span>
  );
}

export default Tietosivu;
