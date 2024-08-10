import http from 'k6/http';
import { check, sleep } from 'k6';

const totalRequests = 25000
const durationInSeconds = 60
const requestsPerSecond = totalRequests / durationInSeconds
const url = ""
const body = ""

const spikeTarget = 10 * Math.floor(requestsPerSecond)

export const options = {
  stages: [
    { duration: '10s', target: 0 },
    { duration: '15s', target: spikeTarget },
    { duration: '10s', target: 0 }, 
    { duration: '15s', target: spikeTarget },
    { duration: '10s', target: 0 }, 
  ],
}

export default function() {
  const res = http.post(url, body);
  check(res, {'status was 200': (r) => r.status == 200});
  sleep(1 / requestsPerSecond);
}