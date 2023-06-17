
const API_URL = "http://localhost:5000";

export default async function fetchFromEndpoint(endpoint, method, content, headers) {
  const res = await fetch(`${API_URL}/${endpoint}`, {
    method: method,
    headers: headers ? headers : {
      "Content-Type": "application/json",
    },
    ...content
  });
  const data = await res.json();
  return data;
}