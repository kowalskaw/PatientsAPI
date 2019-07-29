from marshmallow import Schema, fields as ma_fields, post_load

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
