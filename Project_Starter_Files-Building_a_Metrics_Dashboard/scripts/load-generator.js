import { sleep } from "k6";
import http from "k6/http";

export let options = {
  vus: 10,
  duration: '1800s',
};

export default function main() {
  let response;

  // Trial-Service
  response = http.get("http://localhost:8083/");
  sleep(1);

  // Backend-Service:Home
  response = http.get("http://localhost:8081/");
  sleep(1);

  // Frontend-Service:Home
  response = http.get("http://localhost:8080/");
  sleep(1);

  // Backend-Service:API
  response = http.get("http://localhost:8081/api");
  sleep(1);
}