from datetime import datetime
from core.models import *
from core.models.consent import OB_PERMISSION_VALUES
from core.serializers import *
from rest_framework.exceptions import PermissionDenied
from dateutil.relativedelta import relativedelta
from core.exceptions.exceptions import ConsentAlreadyCreatedException, ConsentNotFoundException

import uuid


def getUserConsents(user):#, filterParams):
    # As seguintes listas de banco e de conta são simplificadas pois estas listagens dependem da implementação da parte de Consentimentos
    # validar inputs
    accounts = user.accounts.all()
    
    consents = MockedConsent.objects.none()
    for account in accounts:
        consentQS = MockedConsent.objects.filter(
            bankAccount = account,
            user = user
        )
        consent = consentQS.first()
        if (consent is not None) and (consent.status != CONSENT_STATUS.REVOKED):
            consents = consents | consentQS
             
    return consents

def getSpecificConsent(user, account):#, filterParams):
    # validar inputs
    
    consent = MockedConsent.objects.filter(
        bankAccount = account,
        user = user
    ) 

    return consent

def getUniqueConsent(consentId):
    
    consent = MockedConsent.objects.filter(consentId=consentId).first() 

    return consent

def createConsent(user, account, permissions, extraMonths):
    
    #validar inputs
    # Checkar se consent já existe 
    consent = MockedConsent.objects.filter(user=user, bankAccount=account).first()
    if consent is None:
        newConsent = MockedConsent( #"urn:bancoex:C1DD33123", por enquanto tá uuid puro, mas depois da para tratar e deixar mais bonito
            consentId = "urn:" + account.brandName + ":" + str(uuid.uuid4()),
            user = user,
            bankAccount = account,
            expirationDateTime = datetime.now() + relativedelta(months=extraMonths)
        )
        newConsent.save()
        
        for permission in permissions:
            permissionObj = OBPermissions.objects.filter(value=permission).first()
            
            if newConsent.permissions is None:
                newConsent.permissions.set([permissionObj])
            else:
                newConsent.permissions.add(permissionObj)

            newConsent.save()
            
        id = newConsent.consentId
        #TODO: Adicionar serializer para consent criado
        return {
            "status_code": 200,
            "message": f"Consent {id} criado com sucesso"
        }, None
    
    return None, ConsentAlreadyCreatedException.serialize(ConsentAlreadyCreatedException)

def revokeConsent(consentId, user):
    consent = MockedConsent.objects.filter(consentId=consentId).first()
    if user.pk != consent.user.pk:
        raise PermissionDenied()
    
    if consent.status == CONSENT_STATUS.REVOKED:
        return {
            "status_code": 412,
            "message": "Consentimento já estava revogado"
        }, None
    else:
        consent.status = CONSENT_STATUS.REVOKED
        consent.statusUpdateDateTime = datetime.now()
        consent.save()
        return {
            "status_code": 200,
            "message": "Consentimento revogado"
        }, None

def renovateConsent(consentId, user, extraMonths):
    consent = MockedConsent.objects.filter(consentId=consentId).first()
    if user.pk != consent.user.pk:
        raise PermissionDenied()
    
    if consent.status == CONSENT_STATUS.REVOKED:
        return {
            "status_code": 405,
            "message": "Consentimento revogado não pode ser renovado"
        }, None
    else:
        consent.status = CONSENT_STATUS.AUTHORIZED
        consent.statusUpdateDateTime = datetime.now()
        newDate = datetime.now() + relativedelta(months=extraMonths)
        consent.expirationDateTime = newDate
        consent.transactionToDateTime = newDate
        consent.save()
        return {
            "status_code": 200,
            "message": "Consentimento renovado"
        }, None

def editConsentPermission(consentId, user, newPermission):
    consent = MockedConsent.objects.filter(consentId=consentId).first()
    if user.pk != consent.user.pk:
        raise PermissionDenied()
    
    if consent.status == CONSENT_STATUS.REVOKED:
        return {
            "status_code": 405,
            "message": "Consentimento revogado não pode ser alterado"
        }, None
    else:
        consent.permissions = newPermission
        consent.statusUpdateDateTime = datetime.now()
        consent.save()
        return {
            "status_code": 200,
            "message": "Consentimento atualizado"
        }, None

def revokeConsent(user, consentId):
    consent = MockedConsent.objects.filter(user=user, consentId=consentId).first()
    if consent is None:
        return {
            None,
            ConsentNotFoundException.serialize(ConsentNotFoundException)
        }
    
    consent.delete()

    return (
        {
            "message": "Consentimento revogado com sucesso"
        },
        None
    )