# The-Direct-Professional
# Async Video Processing Queue 🎬⚙️

A lightweight, non-blocking REST API built to handle simulated heavy video rendering tasks asynchronously. 

Instead of forcing the user to wait for a 10-minute video to process, this API instantly accepts the job, hands it off to a background worker, and provides a tracking ID so the client can poll for real-time progress updates.

## Tech Stack
* **Framework:** FastAPI (Python)
* **Database:** SQLite + SQLAlchemy ORM
* **Validation:** Pydantic
* **Server:** Uvicorn
* **Concurrency:** FastAPI `BackgroundTasks`

## Architecture
1. **`POST /render`**: Accepts video rendering parameters, creates a `PENDING` job in the database, spawns a background worker, and immediately returns the job ID (`202 Accepted`).
2. **Background Worker**: Queries the database for the job, updates the status to `PROCESSING`, and simulates a heavy computational load while incrementally updating the job's `progress` percentage (0-100%).
3. **`GET /status/{job_id}`**: Allows the client to poll the current status and completion percentage of their specific task.

## How to Run Locally

**1. Clone and enter the repository:**
\`\`\`bash
git clone <your-github-repo-url>
cd async-video-queue
\`\`\`

**2. Set up the virtual environment and install dependencies:**
\`\`\`bash
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic
\`\`\`

**3. Start the server:**
\`\`\`bash
uvicorn main:app --reload
\`\`\`

**4. Test the API:**
Open your browser and navigate to the interactive Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).