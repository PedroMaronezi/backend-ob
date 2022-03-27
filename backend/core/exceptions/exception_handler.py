from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == (401 or 403):
          response.data['code'] = "NOT_AUTHENTICATED"
          response.data['detail'] = "Usuário não autenticado. Verifique se o login foi realizado."

        else :
            response.data['status_code'] = response.status_code

    return response