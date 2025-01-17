from app import db,  create_app
from app.models import Employee, Shift,Attendance  # استيراد النماذج

from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=3000)
