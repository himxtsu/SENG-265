from json import JSONEncoder
from clinic.patient import Patient

# Json encoding function, checks if instance and returns the encoded object
class PatientEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Patient):
            return {"__type__": "Patient", "phn": obj.phn, "name": obj.name, "birth_date": obj.birth_date, "phone": obj.phone, \
                    "email": obj.email, "address": obj.address}
        return super().default(obj)