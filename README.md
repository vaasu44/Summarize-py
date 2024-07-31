Project Setup Instructions
Prerequisites
Python 3.8 or higher
Node.js and npm
Docker (optional, for LLM deployment)
Backend Setup
Clone the repository:


git clone <repository_url>
cd <repository_directory>/backend
Create a virtual environment and activate it:


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:


pip install -r requirements.txt
Run the backend server:


flask run  # or `uvicorn main:app --reload` if using FastAPI
Frontend Setup
Navigate to the frontend directory:


cd ../frontend
Install dependencies:


npm install
Start the React application:


npm start
LLM Deployment Setup
Navigate to the LLM deployment directory:


cd ../llm
Set up the local environment:


docker build -t local-llm .
docker run -p 8000:8000 local-llm
Ensure the LLM is running and accessible.

Usage
Upload a document via the frontend.
Receive the summarized text displayed on the frontend.

Additional Information
Ensure all services (backend, frontend, LLM) are running concurrently.
Refer to the detailed documentation in the repository for more information.
