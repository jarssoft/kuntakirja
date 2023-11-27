import React from 'react';
import css from './Tiedot.module.css';

export const Tulokset = ({asukkaat}) => {
  if (asukkaat === undefined || !asukkaat.length) return null;

  return (
      asukkaat.length > 700 ?
        <div className={css.todos}>Kirjoita tarkempi haku</div>
      :
        <div className={css.todos}>
          {asukkaat.map((toDo, index) => (
            <span
              nav-selectable="true"
              key={index}
              className={`${css.todo} ${toDo.completed ? css.completed : ''}`}>
              <b>{toDo.sukunimi}</b>, 
              {" "+toDo.asukkaat[0].etunimet[0]}
              {toDo.asukkaat[0].syntymäaika ? `, ${toDo.asukkaat[0].syntymäaika}` : ""}
            </span>
          ))}
        </div>
    )
}