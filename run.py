
from job_chan import app
import os

@app.before_first_request
def create_table():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
