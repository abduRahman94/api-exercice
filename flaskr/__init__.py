from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



def create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)
    db = SQLAlchemy()
    migrate = Migrate(app, db)
    db.init_app(app)
    # db.create_all()
    
    class Tutor(db.Model):
        __tablename__='tutors'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        surname = db.Column(db.String(100))
        speciality = db.Column(db.String(200))
        
        def format(self):
            return {
                'id': self.id,
                'name': self.name,
                'surname': self.surname,
                'speciality': self.speciality
            }
        
    
    
    @app.route('/tutors', methods=['GET', 'POST'])
    def tutors():
        if request.method == 'GET':
            tutors = [tutor.format() for tutor in Tutor.query.all()]

            return jsonify({
                'tutors': tutors
            })
        
        if request.method == 'POST':
            data = request.get_json()
            name = data.get('name') # None
            surname = data.get('surname')
            speciality = data.get('speciality')
            tutor = Tutor(name=name, surname=surname, speciality=speciality)
            db.session.add(tutor)
            db.session.commit()
            return jsonify({
                'id': tutor.id,
                'message': 'Tutor created successfully'
            })
    
    @app.route('/tutors/<int:id>', methods=['GET'])
    def get_tutor(id):
        try:
            tutor = Tutor.query.get(id)
            return jsonify({
                'id': tutor.id,
                'name': tutor.name,
                'surname': tutor.surname,
                'speciality': tutor.speciality
            })
        except AttributeError:
            return jsonify({
                'message': 'Tutor does\'nt exist' 
            })
    
    @app.route('/tutors/<int:id>', methods=['PUT'])
    def update_tutor(id):
        try:
            tutor = Tutor.query.get(id)
            data = request.get_json()
            tutor.name = data.get('name')
            tutor.surname = data.get('surname')
            tutor.speciality = data.get('speciality')
            db.session.commit()
            
            return jsonify({
                'id': tutor.id,
                'message': 'Tutor updated successfully'
            })
        except AttributeError:
            return jsonify({
                'message': 'Tutor does\'nt exist' 
            })
    
    @app.route('/tutors/<int:id>', methods=['DELETE'])
    def delete_tutor(id):
        try:
            tutor = Tutor.query.get(id)
            db.session.delete(tutor)
            db.session.commit()
            
            return jsonify({
                'id': tutor.id,
                'message': 'Tutor deleted successfully'
            })
        except AttributeError:
            return jsonify({
                'message': 'Tutor does\'nt exist' 
            })
    
    return app


app = create_app('config')