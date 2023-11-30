import { Link } from "react-router-dom";

function Hakutulos({ talo }) {
  const getImageName = (perheId) =>
    `../../photos/${Math.floor(perheId / 4) + 69}.png-${perheId % 4}.jpg`;
  return (
    <div className="search-result new-job">
      <div className="thumbnail">
        <Link to={`/talo/${talo.asukkaat[0].perhe}`}>
          <img src={getImageName(talo.asukkaat[0].perhe)} width="160" />
        </Link>
      </div>
      <div className="content">
        <h2>
          <Link to={`/talo/${talo.asukkaat[0].perhe}`}>{talo.sukunimi}</Link>
        </h2>
        <p>
          <span className="company">
            <a href="/job/1234">{talo.kyla}</a>
          </span>
          -
          <a href="/reviews/1234">
            <span className="stars">
              <span className="stars-inner"></span>
            </span>
            <span className="reviews">{talo.tontti}</span>
          </a>
        </p>
        <div>
          <p>{talo.kuvaus} &hellip;</p>
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
