import React from 'react';
import css from './Tiedot.module.css';

export const Lisatiedot = ({asukas: asunto}) => {
  if (asunto === undefined) return null;
  
  return (
      <div>
          <span>

            <p className={css.todos}>
              <h3 className={css.nimi}>{asunto["sukunimi"]}</h3>
              <div>
                {asunto.tontti ? `${asunto.tontti}, ` : ""} 
                {asunto["pinta-ala"] && asunto["pinta-ala"] > 1 ? `${asunto["pinta-ala"]} ha, ` : ""} 
                {asunto.kyla}
              </div>
            </p>

            <p className={css.todos}>
            {asunto.asukkaat.map((asukas, index) => (
               <>
                <div className={css.asukkaat} key={index}>
                  {`${asukas.etunimet[0].split(" ", 3)[0]}, `} 
                  {/* </div><div className={css.asukkaat}>*/}
                  { asukas.syntymäaika ? `s. ${asukas.syntymäaika} `: " "}
                  { asukas.syntymäpaikka ? asukas.syntymäpaikka: ""}
                </div>
                <div>
                  { asukas.ammatit ? asukas.ammatit: ""}
                </div>
               </>
            ))
            }
            </p>
            
            {asunto.lapset ?            
            <p className={css.todos}>
              <div className={css.asukkaat}>Lapset:</div>
              {asunto.lapset.map((lapsi) => (
                <>{lapsi.etunimet[0]} {lapsi.syntymäaika}, </>
              ))
              }  
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