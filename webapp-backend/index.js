const express = require("express");
const app = express();
const asukkaat = require("./eurajoki.json");
const cors = require("cors");

app.use(express.json());
app.use(express.static("dist"));
//app.use('/', express.static(__dirname + '/public'));
app.use("/haku/*", express.static(__dirname + "/dist"));
app.use(cors());

app.get("/", (req, res) => {
  res.send("<h1>Hello World!</h1>");
});

app.get("/api/talot", (request, response) => {
  //console.log(request);
  const pattern = request.query["pattern"].toLowerCase();
  const offset = request.query["offset"]
    ? parseInt(request.query["offset"])
    : 0;
  const sort = request.query["sort"] ? request.query["sort"] : "tontti";
  const selected = asukkaat
    .filter((talo) =>
      (talo["tontti"] + " " + talo["kyla"] + " " + talo["rakennusvuosi"])
        .toLowerCase()
        .includes(pattern)
    )
    .sort((talo1, talo2) => {
      if (sort === "tontti") {
        return talo1["tontti"] > talo2["tontti"] ? 1 : -1;
      }

      const sort1 = talo1[sort] ? parseFloat(talo1[sort]) : 0;
      const sort2 = talo2[sort] ? parseFloat(talo2[sort]) : 0;

      return sort1 < sort2 ? 1 : -1;
    })
    .slice(offset, offset + 30);
  response.json(selected);
});

app.get("/api/talot/:id", (request, response) => {
  const id = Number(request.params.id);
  const talo = asukkaat.find((talo) => talo.id === id);
  response.json(talo);
});

function onlyUnique(value, index, array) {
  return array.indexOf(value) === index;
}

app.get("/api/kylat", (request, response) => {
  //console.log(request);
  const selected = asukkaat
    .map((talo) => talo["kyla"])
    .filter(onlyUnique)
    .filter((kyla) => kyla != null)
    .sort((kyla1, kyla2) => {
      return kyla1 > kyla2 ? 1 : -1;
    });
  response.json(selected);
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
