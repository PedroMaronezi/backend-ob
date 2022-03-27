from email.policy import default
from rest_framework.exceptions import APIException

# Classe customizada a partir de APIException para facilitar serialização para responses
class SerializableAPIException(APIException):
    def serialize(self):
        return {
            "status_code": self.status_code,
            "default_code": self.default_code,
            "default_detail": self.default_detail
        }

#Exceptions
class EmailAlreadyTakenException(SerializableAPIException):
    status_code=409 # Conflict
    default_code="EMAIL_ALREADY_TAKEN"
    default_detail="O email enviado já está associado à outra conta."

class InvalidEmailException(SerializableAPIException):
    status_code=422 # Unprocessable Entity
    default_code="INVALID_EMAIL_FORMAT"
    default_detail="O email enviado não é válido."

class MissingRequestFieldException(SerializableAPIException):
    status_code=400 # Bad request
    default_code="MISSING_REQUEST_FIELD"
    default_detail="Um dos campos obrigatórios não foi enviado na requisição."

class ConsentAlreadyCreatedException(SerializableAPIException):
    status_code=409 # Conflict
    default_code="CONSENT_ALREADY_CREATED"
    default_detail="O consentimento para este par de usuário e conta ja existe."

class ConsentNotFoundException(SerializableAPIException):
    status_code=404 # Conflict
    default_code="CONSENT_NOT_FOUND"
    default_detail="O consentimento não foi encontrado"