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