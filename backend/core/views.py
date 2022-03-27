from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from .serializers import ChangeAccountInfoSerializer

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from core.exceptions.exceptions import (
    EmailAlreadyTakenException,
    InvalidEmailException,    
    MissingRequestFieldException
)
from core.domain import accounts, transactionsController, consentController, categoryController
from core.serializers import (
    TransactionsSerializer,
    ConsentSerializer,
    CategorySerializer
)
from core.models import *

import json
class ExempleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(f'Usuário com email {request.user.email} autenticado corretamente')


class AccountCreationView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        requestBody = json.loads(request.body)
    

        if ('email' in requestBody) and ('password' in requestBody) and ('name' in requestBody ) and ('cpf' in requestBody):

            (data, error) = accounts.create_account(requestBody['email'], requestBody['password'], requestBody['name'], requestBody['cpf'], requestBody['tel'])

            if error:
                print(error)
                return Response(status=error['status_code'], data=error)

            return Response(status=data['status_code'], data=data)

        return Response(status=MissingRequestFieldException.status_code, data=MissingRequestFieldException.serialize(MissingRequestFieldException))

# EndPoint para obter/alterar dados de usuário
class ManageAccountView(generics.UpdateAPIView):
    serializer_class = ChangeAccountInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get(self, request):
        response = {
            'email': request.user.email,
            'name': request.user.name,
            'cpf': request.user.cpf,
            'tel': request.user.tel,
            'status': 'success',
            'code': status.HTTP_200_OK,
        }
        return Response(response)

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Checa a senha
            if not self.object.check_password(serializer.data.get("password")):
                return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.data.get("new_name"):
                self.object.name = serializer.data.get("new_name")
            if serializer.data.get("new_email"):
                user = User.objects.filter(email=serializer.data.get("new_email")).first()
                if user:
                    return Response(EmailAlreadyTakenException.serialize(EmailAlreadyTakenException),None)
                try:
                    validate_email(serializer.data.get("new_email"))
                except ValidationError as e:
                    return Response(InvalidEmailException.serialize(InvalidEmailException),None)
                self.object.email = serializer.data.get("new_email")
            if serializer.data.get("new_tel"):
                self.object.tel = serializer.data.get("new_tel")
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Account updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# EndPoint para alterar a senha
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Checa a senha antiga
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # Seta a senha nova
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Campos necessários para request de transactions de acordo com o OB:
        # Accept application/json
        # Authorization -> Token do seviço da IT. Como não acessamos o serviço, identificamos o usuário pelo nosso próprio JWT
        # accountId: Identificador da conta
        # compeCode: Pelo que entendi, é um código nosso fornecido pelo banco central
        # branchCode: código da agência detentora da conta
        # number: número da conta
        
        # O fluxo para pegar transações será:
        # for banco in ListaBancos:
        #     for conta in banco:
        #         getTransactions(conta)

        # filtros possíveis:
        # - banco
        # - dispesa/receita
        # - categoria
        queryParams = request.GET.dict() 

        transactions = transactionsController.getUserTransactions(user=request.user,filterParams=queryParams)
        if ('by' in queryParams) and (queryParams["by"] == "account"):
            responseData = transactionsController.formatTransactionsByAccount(transactions)
        else:
            responseData =  TransactionsSerializer(transactions, many=True).data
        
        return Response(data=responseData)

class BalanceView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryParams = request.GET.dict() 

        data = transactionsController.getUserBalance(user=request.user, filterParams=queryParams)
        return Response(data=data)

class ConsentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unserializedData = consentController.getUserConsents(user=request.user)
        data = ConsentSerializer(unserializedData, many=True).data
        return Response(data=data)
    
    def post(self, request):
        requestBody = json.loads(request.body)

        if (
            ('account' in requestBody) and ('brandName' in requestBody['account']) and
            ('permissions' in requestBody) 
        ): 

            user = request.user
            bankAccount = user.accounts.filter(brandName=requestBody['account']['brandName']).first()
            
            extraMonths = 2
            if 'extraMonths' in requestBody: 
                extraMonths = requestBody['extraMonths']
                
            (data, error) = consentController.createConsent(user, bankAccount, requestBody['permissions'], extraMonths)

            if error:
                print(error)
                return Response(status=error['status_code'], data=error)

            return Response(status=data['status_code'], data=data)
            
        return Response(status=MissingRequestFieldException.status_code, data=MissingRequestFieldException.serialize(MissingRequestFieldException))
    
    def put(self, request):
        if request.body: 
            requestBody = json.loads(request.body)
            if ('CPF' in requestBody['user']) and ('email' in requestBody['user']) and ('consentId' in requestBody['consent']) and ('opType' in requestBody):
                
                if requestBody['opType'] == CONSENT_OPTYPE.EDIT_PERMISSION:                    
                    consent= MockedConsent.objects.filter(consentId=requestBody['consent']['consentId']).first()
                    user = User.objects.filter(email=requestBody['user']['email']).first()

                    (data, error) = consentController.editConsentPermission(consent.consentId,user, requestBody['newPermissions'])
                    if error:
                        print(error)
                        return Response(status=error['status_code'], data=error)

                    return Response(status=data['status_code'], data=data)
                
                if requestBody['opType'] == CONSENT_OPTYPE.RENOVATE:                    
                        
                    consent= MockedConsent.objects.filter(consentId=requestBody['consent']['consentId']).first()
                    user = User.objects.filter(email=requestBody['user']['email']).first()
                    
                    (data, error) = consentController.renovateConsent(consent.consentId,user, requestBody['extraMonths'])
                    if error:
                        print(error)
                        return Response(status=error['status_code'], data=error)

                    return Response(status=data['status_code'], data=data)
                
                if requestBody['opType'] == CONSENT_OPTYPE.REVOKE:                          
                    consent= MockedConsent.objects.filter(consentId=requestBody['consent']['consentId']).first()
                    user = User.objects.filter(email=requestBody['user']['email']).first()
                    
                    (data, error) = consentController.revokeConsent(consent.consentId,user)
                    if error:
                        print(error)
                        return Response(status=error['status_code'], data=error)

                    return Response(status=data['status_code'], data=data)

            return Response(status=MissingRequestFieldException.status_code, data=MissingRequestFieldException.serialize(MissingRequestFieldException))

    def delete(self, request):
        requestBody = json.loads(request.body)

        if ("consentId" in requestBody):
            (data, error) = consentController.revokeConsent(request.user, requestBody["consentId"])
            
            if error:
                print(error)
                return Response(status=error['status_code'], data=error)

            return Response(data=data)
        
        return Response(status=MissingRequestFieldException.status_code, data=MissingRequestFieldException.serialize(MissingRequestFieldException))
        
class CategoriesView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        unserializedCategories = categoryController.getCategories()

        return Response(data=CategorySerializer(unserializedCategories, many=True).data)