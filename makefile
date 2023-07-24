PROJECT_NAME = PyInvestAnalyser

.PHONY: run
run:
	@pipenv run streamlit run app.py

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@pipenv --rm
	@echo "Cleanup complete."

.PHONY: install
install:
	@echo "Installing dependencies..."
	@pipenv install
	@echo "Installation complete."

.PHONY: uninstall
uninstall:
	@echo "Uninstalling dependencies..."
	@pipenv --rm
	@echo "Uninstallation complete."

.PHONY: test
test:
	@pipenv run pytest tests/