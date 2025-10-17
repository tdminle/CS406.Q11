
# Makefile for Lab-03: Image Enhancing (Windows version)

APP_NAME = lab03_app.py
VENV_DIR = venv

# --- Create virtual environment ---
setup:
	@echo ">>> Creating virtual environment..."
	python -m venv $(VENV_DIR)
	@echo ">>> Installing dependencies..."
	$(VENV_DIR)\Scripts\pip install --upgrade pip
	$(VENV_DIR)\Scripts\pip install -r requirements.txt
	@echo ">>> Setup completed!"

# --- Run the Streamlit app ---
run:
	@echo ">>> Running Streamlit app..."
	$(VENV_DIR)\Scripts\streamlit run $(APP_NAME)

# --- Clean the environment ---
clean:
	@echo ">>> Removing virtual environment and cache..."
	if exist $(VENV_DIR) rmdir /s /q $(VENV_DIR)
	if exist __pycache__ rmdir /s /q __pycache__
	@echo ">>> Clean done!"
