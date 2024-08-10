import http from 'k6/http';
import { check, sleep } from 'k6';

const totalRequests = 25000
const durationInSeconds = 60
const requestsPerSecond = totalRequests / durationInSeconds
const url = ""
const body = ""

// Round the target values to ensure they are integers
const sustainedTarget = Math.floor(requestsPerSecond)

export const options = {
  stages: [
    { duration: '50s', target: sustainedTarget },
    { duration: '10s', target: 0 },                
  ],
}

export default function() {
  const res = http.post(url, body);
  check(res, {'status was 200': (r) => r.status == 200});
  sleep(1);
}