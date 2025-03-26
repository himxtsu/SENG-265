from json import JSONDecoder
from clinic.patient import Patient

# Decoder Json, returns a dict of the decoded json object
class PatientDecoder(JSONDecoder):
  def __init__(self, *args, **kwargs):
    super().__init__(object_hook=self.object_hook, *args, **kwargs)

  def object_hook(self, dct):
    if '__type__' in dct and dct['__type__'] == 'Patient':
      return Patient(dct['phn'], dct['name'], dct['DoB'], dct['phone'], dct['email'], \
                     dct['address'])
    return dct
