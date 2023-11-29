import { useState } from "react";

function Hakukentta({ hakusana, etsi }) {
  const [haku, setHaku] = useState(hakusana);

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        etsi(haku);
      }}
    >
      <input
        value={haku}
        onChange={(event) => {
          //console.log(haku);
          setHaku(event.target.value);
        }}
      ></input>
      <button type="submit">Etsi</button>
    </form>
  );
}

export default Hakukentta;
