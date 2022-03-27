from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from core.exceptions.exceptions import (
    EmailAlreadyTakenException,
    InvalidEmailException    
)

from core.models import User

def create_account(email, password, name, cpf, tel):
    try:
        validate_email(email)
    except ValidationError as e:
        return None, InvalidEmailException.serialize(InvalidEmailException)
        
    user = User.objects.filter(email=email).first()
    if user:
        return None, EmailAlreadyTakenException.serialize(EmailAlreadyTakenException)
    
    if len(str(cpf)) < 14:
        return {
            "status_code": 409,
            "message": "O CPF enviado é inválido"
        }, None
    if cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
        return {
            "status_code": 409,
            "message": "O CPF enviado é inválido"
        }, None
    try:
        cpfpart1 = int(cpf[0]+cpf[1]+cpf[2])
        cpfpart2 = int(cpf[4]+cpf[5]+cpf[6])
        cpfpart3 = int(cpf[8]+cpf[9]+cpf[10])
        cpfpart4 = int(cpf[12]+cpf[13])
    except:
        return {
            "status_code": 409,
            "message": "O CPF enviado é inválido"
        }, None
    user = User.objects.filter(cpf=cpf).first()
    if user:
        return {
            "status_code": 409,
            "message": "O CPF enviado já está associado à outra conta."
        }, None
    
    user = User.objects.create_user(email=email, password=password, name=name, cpf=cpf, tel=tel)
    return {
        "status_code": 200,
        "message": "Usuário criado com sucesso"
    }, None