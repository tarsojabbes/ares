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

This will create a basic template for a k6 test that you can edit. The created file will not be the test itself to be executed, rather it's a template that will be used and parsed to generate the real test. This is because we offer engineers the option to declare in a YAML file what will be the test parameters.

For example, if you access `tests/default/http.gradualRampUp.js` you'll see that the file is not a common Javascript file, once it has `{{ares_config.<parameter>}}` all over the test code. The values for these parameters are set in a corresponding YAML file that describe the test, in this case, `projects/default/example-test.yaml`, under `tests.default/http.gradual_ramp_up`.

As a good practice, we recommend that you prepend your test name with the protocol you're using (HTTP or gRPC).

## Starting Ares

As said above, Ares is built on top of Open Source tools that are designed to collect, aggregate and display data. So, for you to visualize your microservice behavior, you need to get this infrastructure up and running, by simply running:

```sh
make ares-start
```

### Stopping Ares

To stop all services, do: `make ares-stop`

## Executing tests

Each test execution is defined by an YAML configuration file, where you declare what tests will be executed and other possible options. You can find an example at `projects/default/example-test.yaml`

1. Run your test file

```sh
make run-test PROJECT=<project_name> TEST_FILE=<test_name.yaml>
```

Running your tests mean that we parse your YAML file to a `docker-compose.yaml` that gets your microservice up and running, and we also create a folder `projects/<project_name>/generated_tests/<test_file>` that will contain all tests generated with the values you informed in your test declaration file.

You can check this under `projects/default/generated_tests/example-test` and look for `http.gradualRampUp.generated.js` and `http.spikeLoad.generated.js`. Now, these are the tests we will perform!