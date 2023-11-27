import React from 'react';
import css from './Tiedot.module.css';

export const Lisatiedot2 = ({asukas: asunto}) => {
  if (asunto === undefined) return null;
  
  return (
      <div autoFocus id="lisatiedot">
          <span>

            <p className={css.todos}>
              <h3 className={css.nimi}>{asunto["sukunimi"]}</h3>
              <div>
                {asunto.tontti ? `${asunto.tontti}, ` : ""} 
                {asunto["pinta-ala"] && asunto["pinta-ala"] > 0 ? `${asunto["pinta-ala"]} ha, ` : ""} 
                {asunto.kyla}
              </div>
              <div>
                  Päärakennus:
                  { asunto.rakennusmateriaali ? ` ${asunto.rakennusmateriaali.join(", ")} `:  ""}
                  { asunto.rakennusvuosi ? ` (${asunto.rakennusvuosi})`:  ""}                  
              </div>
            </p>

            <p className={css.todos}>
            {asunto.asukkaat.map((asukas, index) => (
               <>
                <div className={css.asukkaat} key={index}>
                  {`${asukas.etunimet.join(' ')}`} 
                  {/* </div><div className={css.asukkaat}>*/}
                </div>
                <div>
                  { asukas.osnimi ? `O.s. ${asukas.osnimi}, `: " "}
                  { asukas.syntymäaika ? `s. ${asukas.syntymäaika} `: " "}
                  { asukas.syntymäpaikka ? asukas.syntymäpaikka: ""}
                </div>
                <div>
                  { asukas.ammatit ? asukas.ammatit.join(', '):  ""}
                </div>
               </>
            ))
            }
              <div>
                { asunto.liitto ? 
                  `${asunto.liitto.tyyppi} 
                   ${ asunto.liitto.alkaen ? `${asunto.liitto.alkaen}`:  ""}`
                   : ""}                                
              </div>
            </p>
            
            {asunto.lapset ?            
            <p className={css.todos}>
              Lapset:&nbsp;
              {asunto.lapset.map((lapsi) => (lapsi.etunimet[0]+" "+lapsi.syntymäaika)).join(", ")}  
            </p>
            :""
            }

            {asunto.kuvaus ?            
            <p className={css.todos}>
              {asunto.kuvaus}  
            </p>
            :""
            }

          {/*
          <p className={css.todos}>
            {toDo.teksti}
          </p>
          */}

          </span>
      </div>
  )
}