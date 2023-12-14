import axios from "axios";
//const baseUrl = "http://localhost:3001/api/talot";
const baseUrl = "https://kuntakirja.onrender.com/api/talot";

const getAll = (pattern, offset, sort) => {
  return axios.get(baseUrl, {
    params: { pattern: pattern, offset: offset, sort: sort },
  });
};

const get = (id) => {
  console.log(baseUrl + "/" + id);
  return axios.get(baseUrl + "/" + id);
};

export default {
  get: get,
  getAll: getAll,
};
