import http from 'k6/http';
import { check, sleep } from 'k6';

const totalRequests = {{ares_config.total_requests}}
const durationInSeconds = {{ares_config.duration}}
const requestsPerSecond = totalRequests / durationInSeconds
const url = "{{ares_config.url}}"
const body = "{{ares_config.body}}"

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
  const res = http.{{ares_config.request_type}}(url, body);
  check(res, {'status was 200': (r) => r.status == 200});
  sleep(1 / requestsPerSecond);
}