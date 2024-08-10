// THIS FILE WAS AUTOGENERATE
// IF YOU ARE SEING THIS AT ./tests/baseTest.js DO NOT DELETE IT
// YOU MAY DELETE IF YOU CREATED THIS FILE THROUGH THE CLI

import http from 'k6/http';
import grpc from 'k6/net/grpc';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};


const client = new grpc.Client();
client.load([], 'path/to/your.proto');

export default function () {
  const httpRes = http.get('https://jsonplaceholder.typicode.com/posts/1');
  check(httpRes, {
    'HTTP status is 200': (r) => r.status === 200,
  });

  client.connect('localhost:50051', { plaintext: true });

  const grpcRes = client.invoke('your.Service/Method', {
    id: 1,
  });

  check(grpcRes, {
    'gRPC status is OK': (r) => r.status === grpc.StatusOK,
  });

  client.close();
  sleep(1);
}
