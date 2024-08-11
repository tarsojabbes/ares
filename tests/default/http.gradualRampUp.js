import http from 'k6/http';
import { check, sleep } from 'k6';

const totalRequests = {{ares_config.total_requests}}
const durationInSeconds = {{ares_config.duration}}
const requestsPerSecond = totalRequests/durationInSeconds
const url = "{{ares_config.url}}"
const body = "{{ares_config.body}}"

export const options = {
  stages: [
    { duration: '10s', target: Math.floor(requestsPerSecond / 6) },
    { duration: '10s', target: Math.floor(requestsPerSecond / 3) },
    { duration: '10s', target: Math.floor(requestsPerSecond / 2) },
    { duration: '10s', target: Math.floor((requestsPerSecond * 2) / 3) },
    { duration: '10s', target: Math.floor((requestsPerSecond * 5) / 6) },
    { duration: '10s', target: Math.floor(requestsPerSecond) },
  ],
}

export default function() {
  const res = http.{{ares_config.request_type}}(url, body);
  check(res, {'status was 200': (r) => r.status == 200});
  sleep(1 / requestsPerSecond);
}