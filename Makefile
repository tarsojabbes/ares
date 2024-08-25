.PHONY: help
help:  ## Displays help message
	@echo "Makefile to control development tasks for $(APP_NAME)"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)


.PHONY: create-test-directory
create-test-directory: ## Creates a directory to store tests for a project
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Usage: make create-test-directory <project_name>"; \
		exit 1; \
	fi
	@PROJECT=$(filter-out $@,$(MAKECMDGOALS)); \
	mkdir -p ./tests/$$PROJECT

%:
	@:

.PHONY: create-test-file
create-test-file: ## Creates a test file in the specified project directory
	@if [ "$(word 2, $(MAKECMDGOALS))" = "" ] || [ "$(word 3, $(MAKECMDGOALS))" = "" ]; then \
		echo "Usage: make create-test-file <project_name> <test_file_name>"; \
		exit 1; \
	fi
	@PROJECT=$(word 2, $(MAKECMDGOALS)); \
	FILE=$(word 3, $(MAKECMDGOALS)); \
	touch ./tests/$$PROJECT/$$FILE; \
	cp ./tests/baseTest.js ./tests/$$PROJECT/$$FILE

%:
	@:

.PHONY: run-test
run-test: ## Run a test defined by a specified YAML file
	@if [ "$(PROJECT)" = "" ] || [ "$(TEST_FILE)" = "" ]; then \
		echo "Usage: make run-test PROJECT=<project_name> TEST_FILE=<test_name.yaml>"; \
		exit 1; \
	fi
	echo "Running test for project: $(PROJECT) with test file: $(TEST_FILE)"; \
	\
	# Generate docker-compose.yml
	python3 ./parser/parse_yaml_to_docker.py ./projects/$(PROJECT)/$(TEST_FILE) ./projects/$(PROJECT)/docker-compose.yml; \
	\
	# Generate test files
	python3 ./parser/parse_yaml_to_test.py ./projects/$(PROJECT)/$(TEST_FILE) ./projects/$(PROJECT)/; \
	\
	# Generate dashboard file for Grafana
	python3 ./parser/parse_yaml_to_dashboard.py ./projects/$(PROJECT)/$(TEST_FILE) ./infra/grafana/template.json ./infra/grafana/dashboards/$(PROJECT).$(basename $(TEST_FILE)).json
	\
	# Run docker-compose
	docker compose -f ./projects/$(PROJECT)/docker-compose.yml up -d; \
	\
	TEST_FILES="./projects/$(PROJECT)/generated_tests/$(basename $(TEST_FILE))/*.generated.js"; \
	for test_file in $$TEST_FILES; do \
		if [ ! -f $$test_file ]; then \
			echo "No test files found in ./projects/$(PROJECT)/generated_tests/$(basename $(TEST_FILE))/"; \
			exit 1; \
		fi; \
		echo "Running test: $$test_file"; \
		k6 run $$test_file; \
	done; \
	\
	# Shut down docker-compose services
	docker compose -f ./projects/$(PROJECT)/docker-compose.yml down

# Capture arguments passed to run-test
run-test-%:
	@$(MAKE) run-test PROJECT=$(word 2,$(MAKECMDGOALS)) TEST_FILE=$(word 3,$(MAKECMDGOALS))

.PHONY: ares start
ares start: ## Start the infrastructure tools for Ares
	docker compose -f./infra/docker-compose.yaml up -d

.PHONY: ares stop
ares stop: ## Stop the infrastructure tools for Ares
	docker compose -f./infra/docker-compose.yaml down