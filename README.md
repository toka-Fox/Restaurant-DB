# HOW TO SET UP
 - Firstly, clone the repo wherever you want it.


 - Run these commands in the cloned project folder:
   - 'python3 -m venv venv' (Create virtual environment)
   - 'venv/Scripts/activate' (Activate virtual environment)
   - 'pip install --upgrade pip' (Update pip)
   - 'pip install -r requirements.txt' (Install required python packages)

    
 - Once that is done, create a new '.env' file and copy and paste 'dotenvexample.txt' into it.
   - In .env fill the fields with the necessary credentials


 - Run 'setup.py' to create the database
   - 'python app/database/setup.py'


 - Run 'main.py' and connect to the server
   - 'python app/main.py'
   - Go to '[DB_HOST]:[DB_PORT]' in your browser