import css from "./Tiedot.module.css";

function Tietosivu({ talo }) {
  return (
    <span>
      <div className="card">
        <h2 className={css.nimi}>{talo["sukunimi"]}</h2>
        <div>
          {talo.tontti ? `${talo.tontti}, ` : ""}
          {talo["pinta-ala"] && talo["pinta-ala"] > 0
            ? `${talo["pinta-ala"]} ha, `
            : ""}
          {talo.kyla}
        </div>
        <div>
          Päärakennus:
          {talo.rakennusmateriaali
            ? ` ${talo.rakennusmateriaali.join(", ")} `
            : ""}
          {talo.rakennusvuosi ? ` (${talo.rakennusvuosi})` : ""}
        </div>
      </div>

      <div className="card">
        {talo.asukkaat.map((asukas, index) => (
          <>
            <div className={css.asukkaat} key={index}>
              {`${asukas.etunimet.join(" ")}`}
              {/* </div><div className={css.asukkaat}>*/}
            </div>
            <div>
              {asukas.osnimi ? `O.s. ${asukas.osnimi}, ` : " "}
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

      <div className="card">
        {talo.lapset ? (
          <div>
            Lapset:&nbsp;
            {talo.lapset
              .map((lapsi) => lapsi.etunimet[0] + " " + lapsi.syntymäaika)
              .join(", ")}
          </div>
        ) : (
          ""
        )}
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
