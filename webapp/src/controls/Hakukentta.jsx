import { useState } from "react";

function Hakukentta({ etsi }) {
  const [count, setCount] = useState(0);

  return (
    <form onSubmit={etsi}>
      <input></input>
      <button onClick={() => setCount((count) => count + 1)}>Etsi</button>
    </form>
  );
}

export default Hakukentta;
