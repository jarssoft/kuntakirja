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

app.get("/api/notes", (request, response) => {
  console.log(request);
  const pattern = request.query["pattern"].toLowerCase();
  const selected = asukkaat
    .filter((talo) =>
      (talo["tontti"] + " " + talo["kyla"]).toLowerCase().includes(pattern)
    )
    .slice(0, 30);
  response.json(selected);
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
