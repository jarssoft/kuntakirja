import axios from "axios";
const baseUrl = "http://localhost:3001/api/notes";

const getAll = (pattern) => {
  return axios.get(baseUrl, { params: { pattern: pattern } });
};

/*
const create = (newObject) => {
  return axios.post(baseUrl, newObject);
};

const update = (id, newObject) => {
  return axios.put(`${baseUrl}/${id}`, newObject);
};
*/

export default {
  getAll: getAll,
  //create: create,
  //update: update,
};
