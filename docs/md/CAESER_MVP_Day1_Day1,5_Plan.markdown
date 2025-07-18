# CÆSER MVP Development Plan: Day 1 and Day 2

This document outlines a detailed, actionable plan for the first two days of the CÆSER MVP development for the Qloo Hackathon, starting at 12:10 AM +06 on Saturday, July 19, 2025. The goal is to create a functional MVP within 10 days, integrating Qloo's API for cultural insights and DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES via OpenRouter.ai for predictive analytics, with a focus on a core use case (e.g., predicting sneaker demand).

---

## Day 1: Obtain API Keys, Set Up Project, and Integrate Qloo API

**Objective**: Establish the project foundation, secure API access, and integrate Qloo's API for cultural insights.

### Step-by-Step Plan

1. **Obtain Qloo API Key (1 hour)**  
   - Navigate to [Qloo's API Documentation](https://www.qloo.com/technology/taste-ai).  
   - Locate and complete the API key request form with project details (e.g., "CÆSER: Cultural Intelligence for E-commerce").  
   - Submit the form and check your email for the API key (expected within 4 hours).  
   - Store the key securely in a `.env` file.  
   - **Mitigation**: If delayed, use mock JSON data for initial setup.

2. **Obtain OpenRouter.ai API Key (1 hour)**  
   - Sign up at [OpenRouter.ai](https://openrouter.ai) and request access to DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES.  
   - Follow the provided instructions to generate an API key (free tier).  
   - Verify access by making a test call with a tool like Postman.  
   - Store the key securely in the `.env` file.  
   - **Mitigation**: If access is limited, focus on DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES and adjust plans if needed.

3. **Set Up Project Structure (2 hours)**  
   - Create a public GitHub repository named `CAESER-mvp`.  
   - Initialize it with a `README.md` and a Python-specific `.gitignore`.  
   - Set up a virtual environment: `python -m venv venv` and activate it.  
   - Install dependencies: `pip install fastapi uvicorn streamlit requests scrapy langchain python-dotenv`.  
   - Create directories: `/api` (backend), `/frontend` (UI), `/data` (storage).  
   - **Deliverable**: A structured, version-controlled project with dependencies installed.

4. **Set Up Backend with FastAPI (2 hours)**  
   - Create `/api/main.py` with a basic FastAPI app:  
     ```python
     from fastapi import FastAPI
     from dotenv import load_dotenv
     import os

     load_dotenv()
     app = FastAPI()

     @app.get("/")
     async def root():
         return {"message": "CÆSER MVP Backend"}
     ```  
   - Add `.env` with `QLOO_API_KEY` and `OPENROUTER_API_KEY`.  
   - Run locally: `uvicorn api.main:app --reload`.  
   - **Deliverable**: A running FastAPI server with secure key management.

5. **Integrate Qloo API for Cultural Insights (3 hours)**  
   - Review Qloo's API docs for endpoints like `/affinities` or `/entities`.  
   - Write a function in `/api/qloo_client.py`:  
     ```python
     import requests
     import os

     QLOO_API_KEY = os.getenv("QLOO_API_KEY")
     BASE_URL = "https://api.qloo.com/v1/"

     def get_cultural_insights(category, region):
         headers = {"Authorization": f"Bearer {QLOO_API_KEY}"}
         params = {"category": category, "region": region}
         response = requests.get(f"{BASE_URL}affinities", headers=headers, params=params)
         return response.json()
     ```  
   - Test with a query (e.g., `get_cultural_insights("sneakers", "New York City")`).  
   - Save sample output to `/data/sample_qloo.json`.  
   - **Deliverable**: A working Qloo API integration.  
   - **Challenge**: Complex data structure. **Mitigation**: Use Postman to explore responses.

6. **Set Up Database with SQLite (1 hour)**  
   - Initialize SQLite in `/data/CAESER.db` with tables:  
     ```python
     import sqlite3

     conn = sqlite3.connect("data/CAESER.db")
     c = conn.cursor()
     c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, category TEXT)''')
     c.execute('''CREATE TABLE IF NOT EXISTS insights (id INTEGER PRIMARY KEY, product_id INTEGER, data TEXT)''')
     conn.commit()
     conn.close()
     ```  
   - Add CRUD functions in `/api/db.py`.  
   - **Deliverable**: A functional database for storing insights.

7. **Document Progress (30 minutes)**  
   - Update `README.md` with setup and integration instructions.  
   - Commit to GitHub: `git add . && git commit -m "feat: Qloo API and backend setup" && git push`.

**Total Time**: 10.5 hours (with breaks)  
**Team Allocation**:  
- Developer 1: API keys, project structure, Qloo integration.  
- Developer 2: FastAPI backend, SQLite setup.  
**Deliverables**:  
- Qloo API integration with sample data.  
- Running FastAPI backend.  
- SQLite database.  
- Updated GitHub repo.

---

## Day 2: Integrate DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES via OpenRouter.ai and Design Prompts

**Objective**: Integrate the LLM, design prompts, and test predictions using Qloo data.

### Step-by-Step Plan

1. **Set Up OpenRouter.ai Integration (2 hours)**  
   - Review OpenRouter.ai docs for DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES integration.  
   - Use LangChain in `/api/llm_client.py`:  
     ```python
     from langchain.llms import OpenRouter
     import os

     llm = OpenRouter(
         api_key=os.getenv("OPENROUTER_API_KEY"),
         model_name="deepseek-r1"
     )

     def test_llm():
         response = llm("Hello, world!")
         return response
     ```  
   - Test connectivity with `test_llm()`.  
   - **Deliverable**: Working DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES connection.

2. **Design Prompts for Predictions (3 hours)**  
   - Define input: product details + Qloo insights.  
   - Create a prompt in `/api/prompts.py`:  
     ```python
     def generate_prediction_prompt(product, insights):
         return f"""
         Given the product '{product}' and cultural insights {insights},
         predict demand uplift as a percentage and suggest a marketing strategy.
         """  
     ```  
   - Experiment in a Jupyter notebook (e.g., `notebooks/prompts.ipynb`).  
   - **Deliverable**: Effective prompts for predictions.  
   - **Challenge**: Inconsistent outputs. **Mitigation**: Refine prompts iteratively.

3. **Implement LLM Output Processing (2 hours)**  
   - Parse LLM responses in `/api/llm_client.py`:  
     ```python
     def process_llm_output(response):
         lines = response.split("\n")
         uplift = next((line for line in lines if "uplift" in line.lower()), "Unknown")
         strategy = next((line for line in lines if "strategy" in line.lower()), "Unknown")
         return {"uplift": uplift, "strategy": strategy}
     ```  
   - Store in SQLite via `/api/db.py`.  
   - **Deliverable**: Processed LLM outputs in the database.

4. **Test Integration with Sample Data (2 hours)**  
   - Use sample data: `product = "New Sneaker Launch"`, `insights = get_cultural_insights("sneakers", "NYC")`.  
   - Run: `response = llm( generate_prediction_prompt(product, insights) )`.  
   - Verify outputs are coherent and store them.  
   - **Deliverable**: Successful predictions for a sample product.

5. **Refine and Optimize (1 hour)**  
   - Check API call and LLM response times.  
   - Optimize code (e.g., reduce redundant calls).  
   - **Deliverable**: Stable, efficient integration.

6. **Document Progress (30 minutes)**  
   - Update `README.md` with LLM setup and prompt details.  
   - Commit to GitHub: `git add . && git commit -m "feat: DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES integration" && git push`.

**Total Time**: 10.5 hours (with breaks)  
**Team Allocation**:  
- Developer 1: OpenRouter.ai integration, prompt design.  
- Developer 2: Output processing, testing.  
**Deliverables**:  
- DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES integration.  
- Working prompts and processed outputs.  
- Successful sample tests.

---

## Conclusion

By completing Day 1 and Day 2, the team will have a solid MVP foundation: a backend with Qloo API integration and a predictive LLM layer via DEEPSEEK R1, DEEPSEEK V3 & KIMI K2 WHICHEVER IS APPROPRIATE FOR SPECIFIC USES. Focus on clear documentation, frequent testing, and the core use case ensures progress aligns with the 10-day timeline. Use tools like Postman and Jupyter notebooks for efficiency, and maintain regular communication to address blockers.