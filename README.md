# KNUST Axis

An API Gateway for verifying Student and Staff IDs.

# Features
- [x] Verify Identity Cards Using Machine Learning
- [x] Extract Information from Identity Cards
- [x] Verify Authentication Status from School DB

# Core Requirements
- FastAPI
- Requests
- EasyOCR

# Project Setup

- Clone this repository to your local machine.
- Create a virtual environment for your project and activate it. Install all dependencies from  requirements.txt file.

```bash
python3 -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```
  
- In the root directory of the project, start the FastAPI server.
  
```bash
python3 app.py
```

- Head to `localhost:8000/docs` in your browser to test the Implementation of the Axis Endpoints and view the coding documentation in an interactive SWAGGER API playground
