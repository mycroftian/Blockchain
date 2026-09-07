class Transactions:
    def __init__(self,hospital_id, doctor_id, patient_id, insurance_id, record_id, operation, prescription, amount, timestamp):
        self.hospital_id = hospital_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.insurance_id = insurance_id
        self.record_id = record_id
        self.operation = operation
        self.prescription = prescription
        self.amount = amount
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'hospital_id' : self.hospital_id,
            'doctor_id': self.doctor_id,
            'patient_id':self.patient_id,
            'insurance_id':self.insurance_id,
            'record_id':self.record_id,
            'operation':self.operation,
            'prescription':self.prescription,
            'amount':self.amount,
            'timestamp':self.timestamp
        }