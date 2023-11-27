import React, { useState } from "react";
import { Header, Input, Tulokset, Lisatiedot2, Softkey } from "./components";
import { useNavigation } from "./hooks";
//import { asukkaat } from "./data";
import asukkaat from './data/eurajoki.json'


export default function App() {

  const [filter, setFilter] = useState("");
  const [filtertype, setFiltertype] = useState(0);
  const [selected, setSelected] = useState(-1);
  const [current, setNavigation] = useNavigation();

  const hakutyypit=["sukunimi", "syntymäaika", "syntymäpaikka", "kylä", "ammatti"]


  const hakuteksti = (asukas) => {
    switch(filtertype) {
      case 0:
        return asukas.sukunimi + " "
            + asukas.asukkaat.map(asukas => asukas.osnimi).join(" ");
     case 1:
        return " "+asukas.asukkaat.map(asukas => asukas.syntymäaika).join(" ")+
           " "+(asukas.lapset ? 
            asukas.lapset.map(lapsi => lapsi.syntymäaika).join(" ")
            :"")
      case 2:
        return " "+asukas.asukkaat.map(asukas => asukas.syntymäpaikka).join(" ")
      case 3:
        return asukas.kyla
      case 4:
        return asukas.asukkaat.map( asukas => 
            (asukas.ammatit ? asukas.ammatit.join(" "):"")).join(" ")
      default:
        // code block
    } 
  }

  let filtered = asukkaat.filter((asukas) => (
        (" "+hakuteksti(asukas)).toLowerCase().includes(filter)
        ));

  console.log(`reload with filter=(${filter})`);
  console.log(`reload with selected=(${selected})`);
  console.log(`reload with filtered=(${filtered})`);

  const onKeyCenter = () => {
    const currentElement = document.querySelector("[nav-selected=true]");

    /*const isATask = currentNavigationIndex > 0;
    if (isATask) {
      setToDo(prevState => {
        const current = [...prevState];
        current[currentNavigationIndex - 1].completed = !current[currentNavigationIndex - 1].completed;
        return current;
      });
    } else {
      */

    if(currentElement){
      
      const currentNavigationIndex = parseInt(currentElement.getAttribute("nav-index"), 10);
      //console.log(currentNavigationIndex);

      if(currentNavigationIndex===0){
        setFilter(""+currentElement.value.toLowerCase())
      }else{
        console.log(`setSelected(${currentNavigationIndex-1})`);
        setSelected(currentNavigationIndex-1)
      }

    }else{

      //setFilter("")
      setSelected(-1)

    }

  };

  const onKeyRight = () => {
    console.log(`filtered=${filtered}`);
      
    if(selected<filtered.length-1){
      setSelected(selected+1)
    }else{
      setSelected(0)
    }
  };

  const onKeyLeft = () => {
    if(filtertype<hakutyypit.length-1){
      setFiltertype(filtertype+1)
    }else{
      setFiltertype(0)
    }
  };

  const avaaKirja = () => {     
    var win = window.open(`file:///home/jari/Kuvat/skannatut/eurajoki/images/${parseInt(parseInt(filtered[selected].asukkaat[0].perhe)/4)+69}.png`,  '_blank');
    win.focus();
  };

  return (
    <>      
      {selected===-1 ? 
        <>
          <Header title="Asukkaat" />
          <Input type="text" label={""/*hakutyypit[filtertype]*/} />                     
          <Tulokset asukkaat={filtered} />

          <Softkey
            left={hakutyypit[filtertype]}
            onKeyLeft={onKeyLeft}
            center={current.type === "INPUT" ? "Etsi":"Avaa"}
            onKeyCenter={onKeyCenter}
            selected={selected}
          />

        </>
      : <>
          <Lisatiedot2 asukas={filtered[selected]} />
        
          <p></p>
          <Softkey
            onKeyLeft={avaaKirja}
            left={"Kirja"}
            center={"Sulje"}
            onKeyCenter={onKeyCenter}
            right={selected!==-1 ? "Seuraava" : ""}
            onKeyRight={onKeyRight}
            selected={selected}
          />
        </>
      }
    </>
  );
}
