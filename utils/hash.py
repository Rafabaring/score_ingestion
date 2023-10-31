from hashlib import sha256


def create_student_entity_id(student_id):
    entity_id_string = f'{student_id}'
    sha_object = sha256(entity_id_string.encode('utf-8'))
    
    return sha_object.hexdigest()
