## How to Run

1. Clone the repository:

   git clone https://github.com/froozy3/test-task.git 
   cd test-task

2. Create a virtual environment:

   python -m venv venv

3. Activate the virtual environment:

   - **Windows**:

     .\venv\Scripts\activate

4. Install the dependencies:

   pip install -r requirements.txt

5. Run the FastAPI application:

   uvicorn main:app --reload

Now you can interact with the project via the API. Open your browser and go to: 

http://127.0.0.1:8000/docs

This will open the automatically generated API documentation, where you can test the endpoints.
