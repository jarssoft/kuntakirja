import { Link } from "react-router-dom";

function Hakutulos({ talo }) {
  const getImageName = (perheId) =>
    `http://ohjelmakartta.fi/kuntakirja/photos/${
      Math.floor(perheId / 4) + 69
    }.png-${perheId % 4}.jpg`;
  return (
    <div className="search-result new-job">
      <div className="thumbnail">
        <Link to={`/talo/${talo.id}`}>
          <img src={getImageName(talo.id)} width="160" />
        </Link>
      </div>
      <div className="content">
        <h2>
          <Link to={`/talo/${talo.id}`}>{talo.tontti}</Link>
        </h2>
        <p>
          <span className="company">
            <Link to={`/haku/${talo.kyla}`}>{talo.kyla}</Link>
          </span>

          <a href="/reviews/1234">
            <span className="stars">
              <span className="stars-inner"></span>
            </span>
            <span className="reviews">{talo.pintaala}</span>
          </a>
        </p>
        <div>
          <p>
            {talo["pinta-ala"] ? <>{talo["pinta-ala"]} hehtaaria. </> : <></>}
            {talo["rakennusvuosi"] ? (
              <> Rakennettu {talo["rakennusvuosi"]}. </>
            ) : (
              <></>
            )}
          </p>
        </div>

        <div className="more">
          <div className="close">x</div>
          <li>
            View all <a href="/jobs/1234">HEB jobs in Austin, TX</a> -{" "}
            <a href="/jobs/austin">Austin jobs</a>
          </li>
          <li>
            Salary Search:{" "}
            <a href="/salary/1234">
              Staff Software Web Engineer salaries in Austin, TX
            </a>
          </li>
          <li>
            Related forums: <a href="/forum/1234">Austin, TX - HEB</a>
          </li>
        </div>
      </div>
    </div>
  );
}

export default Hakutulos;
