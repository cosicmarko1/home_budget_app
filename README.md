## Home Budget API


REST API for tracking personal expenses by category, payment method and time period


## Features:
- user registration and authentication (JWT)
- expense CRUD
- category management
- expense filters by category, amount, date or description
- predefined default categories
- expense summary in last 7 days, last month, last 3 month or last year


## Tech Stack:
- backend: Python 3.13.4, FastAPI
- ORM: SQLAlchemy
- database: MySQL
- migrations: Alembic
- auth: OAuth2 with JWT tokens
- testing: Pytest


## Setup instructions


1. Clone the repository
```bash
git clone https://github.com/your-username/home-budget-api.git
cd home-budget-api
```


2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate # for MacOS 
# for Windows: venv\Scripts\activate
```


3. Install dependencies
```bash
pip install -r requirements.txt
```


4. Create a .env file in the root directory
```bash
touch .env
```


5. Paste the following into .env file and update with your actual credentials
```bash
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=

SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


6. Run Alembic migrations
```bash
alembic upgrade head
```


7. Start the FastAPI app
```bash
uvicorn app.main:app --reload
```


8. Open /docs to test the API
```bash
http://127.0.0.1:8000/docs
```