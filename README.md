# ⚡ Ares Framework

**Ares** is a framework designed to make Load and Stress Testing easy for all developers. Built with Open Source tools, Ares helps you track the behavior of your microservices' resource usage under both common and high workload scenarios.

Ares is designed to be a Git repository, serving as the single source of truth for all your tests. This allows your team to collaborate easily using a version control tool that every engineer is familiar with. 🎯

## 🛠️ Dependencies

- **Docker**
- **Python**

## 🧰 Services

Ares is a collection of Open Source tools commonly used by Site Reliability Engineers for data collection and visualization of service behavior. Our framework leverages the following tools:

- [cAdvisor](https://github.com/google/cadvisor) 🐳
- Prometheus 📊
- Grafana 📉

## 🚀 Test Types

Ares includes three built-in test types designed to simulate different workload scenarios for microservices:

1. **Gradual Ramp Up** — Simulates a normal workload increase for your microservice.
2. **Spike Load** — Simulates a sudden spike in traffic.
3. **Sustained High Load** — Simulates a prolonged high workload over a period of time.

These tests are specifically tailored for microservices that communicate using HTTP or gRPC protocols.

### 🔧 Custom Tests

Under the hood, Ares uses [k6](https://k6.io/) for testing, which means you can create your own custom tests based on your specific needs.

#### Creating Your Own Tests

To create custom tests, simply use `make`:

1. **Create a test directory for your project:**
   ```sh
   make create-test-directory <project_name>
   ```

2. **Create your test file:**
   ```sh
   make create-test-file <project_name> <protocol>.<test_name>.js
   ```

This will generate a basic k6 test template that you can modify. Note that the created file is a template, not the actual test to be executed. This allows engineers to define test parameters using a YAML file.

For example, if you check `tests/default/http.gradualRampUp.js`, you’ll see `{{ares_config.<parameter>}}` placeholders throughout the file. These placeholders will be replaced by values defined in the corresponding YAML file, such as `projects/default/example-test.yaml`.

> **Tip:** As a best practice, we recommend prepending your test name with the protocol you are using (e.g., HTTP or gRPC).

## 🚢 Starting Ares

Ares runs on top of several Open Source tools designed to collect and display data. To start the infrastructure:

```sh
make ares-start
```

This will spin up:
- cAdvisor at `localhost:3010`
- Prometheus at `localhost:3011`
- Grafana at `localhost:3012`

### 🛑 Stopping Ares

To stop all services, simply run:

```sh
make ares-stop
```

## 📊 Visualizing Microservice Resource Usage with Grafana

Ares includes a pre-built Grafana dashboard template that helps visualize key resource usage metrics, including:

- CPU Load Average (10s)
- Filesystem - IO Current
- Memory Usage (Bytes)
- Network Received/Transmitted (Bytes)

To create your own dashboard for a specific microservice, run:

```sh
make create-dashboard PROJECT=<project_name> TEST_FILE=<test_name.yaml>
```

You can then access your dashboard at `localhost:3012` and search for the dashboard named `<project>.<container_name>`.

## 🧪 Running Tests

Each test execution is defined by a YAML configuration file, where you specify the tests to be run and other relevant options. You can find an example in `projects/default/example-test.yaml`.

1. **Run your test file:**

```sh
make run-test PROJECT=<project_name> TEST_FILE=<test_name.yaml>
```

This command will:
- Parse the YAML file to generate a `docker-compose.yaml` file to bring up your microservice.
- Create a folder `projects/<project_name>/generated_tests/<test_file>` containing all the generated tests.

You can then check the `projects/<project_name>/generated_tests/` folder to find the generated test files, such as `http.gradualRampUp.generated.js` and `http.spikeLoad.generated.js`.

Now, these are the actual tests that will be executed! 🚀

---

### 📄 Example Structure:

- `projects/default/example-test.yaml` ➡️ Declares your test parameters.
- `projects/default/generated_tests/http.gradualRampUp.generated.js` ➡️ Generated test ready to run.

---

Feel free to explore and customize Ares to suit your team's needs.
