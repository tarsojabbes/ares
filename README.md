# Ares Framework

Ares is a framework to make Load and Stress Testing easy for all developers. It's built with Open Source tools to facilitate to track behaviour of your Web microservices resource usage under common and high workload scenarios.

Ares is meant to be a Git repository, as a truth source to keep all your tests, as we want your team to be able to collaborate in a single place with a version control tool that every engineer understands.

## Dependencies
- Docker
- Python

## Services

Ares is a collection of Open Source tools used by Site Reliability Engineers to address the basic data collection and display for services. Our framework uses the following tools:

- [cAdvisor](https://github.com/google/cadvisor)
- Prometheus
- Grafana

## Test Types

Ares comes with 3 built-in types of tests for you to use:

1. Gradual Ramp Up, to simulate a common workload for your microservice

2. Spike Load, to simulate a spike workload

3. Sustained High Load, to simulate a scenario of high workload under a period of time

These three types of test were designed to perform case scenarios for microservices that communicate with HTTP or gRPC.

### Custom Tests

Under the hood, each test perfomed by Ares is a [k6](https://k6.io/) test, therefore you can create your own kind of test that fits your needs.

#### Creating your own tests

In order to create your own test, you may use `make`

1. Create a custom test directory for your project

```sh
make create-test-directory <project_name>
```

2. Create your test file

```sh
make create-test-file <project_name> <protocol>.<test_name>.js
```

This will create a basic template for a k6 test that you can edit. As a good practice, we recommend that you prepend your test name with the protocol you're using (HTTP or gRPC).

## Executing tests

Each test execution is defined by an YAML configuration file, where you declare what tests will be executed and other possible options. You can find an example at `projects/default/example-test.yaml`

1. Run your test file

```sh
make run-test <project_name> <test_name.yaml>
```