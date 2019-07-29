from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, post_load

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/docs')

app.register_blueprint(blueprint)


class Patient_obj(object):
    def __init__(self, patient_id, name):
        self.patient_id = patient_id
        self.name = name

    def __repr__(self):
        return 'Patient with ID {} and name {}.'.format(self.patient_id, self.name)


class PatientSchema(Schema):
    patient_id = ma_fields.Integer()
    name = ma_fields.String()

    @post_load
    def create_patient(self, data):
        return Patient_obj(**data)


a_patient = api.model('Patient', {'patient_id': fields.Integer('Patients ID.'),
                                  'name': fields.String('Patients name.')})

patients = []
patient1 = Patient_obj(name = 'Werka', patient_id=1)
patient2 = Patient_obj(name = 'Marcel', patient_id=2)
patients.append(patient1)
patients.append(patient2)


@api.route('/patients')
class Patients(Resource):
    def get(self):
        schema = PatientSchema(many=True)  # bc it's passing a list of objects
        return schema.dump(patients)

    @api.expect(a_patient)
    def post(self):
        schema = PatientSchema()

        new_patient = schema.load(api.payload)
        #new_patient['id'] = len(patients)
        patients.append(new_patient.data)
        return {'result': 'Patient added'}, 201  # for sth has been created


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
