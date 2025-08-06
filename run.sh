#!/bin/bash

# Set environment variables
export DATABASE_URL="postgresql://postgres:admin@localhost:5432/cap_table_db"
export APP_ENV="development"

# Activate virtual environment (Windows style)
source venv/Scripts/activate

# Install required packages
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head

# Initialize database with seed data
python -m app.db.init_db

# Start the FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# cmd to run the run.sh
# ./run.sh