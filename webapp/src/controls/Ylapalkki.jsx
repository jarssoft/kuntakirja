import { Link } from "react-router-dom";
import viteLogo from "/eurajoki.svg";
import Hakukentta from "./Hakukentta.jsx";

function Ylapalkki({ hakusana, etsi }) {
  return (
    <>
      <Link to="/">
        <img src={viteLogo} className="slogo" alt="Eurajoen vaakuna" />
      </Link>
      <Hakukentta hakusana={hakusana} etsi={etsi} />
    </>
  );
}

export default Ylapalkki;
