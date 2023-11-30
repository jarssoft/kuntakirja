const express = require("express");
const app = express();
const asukkaat = require("./data/eurajoki.json");
app.use(express.json());

app.get("/", (req, res) => {
  res.send("<h1>Hello World!</h1>");
});

app.get("/api/notes", (request, response) => {
  const pattern = request.body["pattern"].toLowerCase();
  const selected = asukkaat
    .filter((talo) => talo["sukunimi"].toLowerCase().includes(pattern))
    .slice(0, 30);
  response.json(selected);
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
