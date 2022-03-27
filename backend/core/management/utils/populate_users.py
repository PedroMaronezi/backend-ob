from core.models import User

USER_DATA = [
    {
        "email" : "ricardo@email.com", 
        "password": "senha",
        "name": "Ricardo Gouveia",
        "cpf": "745.394.560-75",
        "tel": "(11)994551458"
    },
    {
        "email" : "giuliana@email.com", 
        "password": "senha",
        "name": "Giuliana dos Reis",
        "cpf": "524.107.100-85",
        "tel": ""
    },
    {
        "email" : "pedro@email.com", 
        "password": "senha",
        "name": "Pedro Carvalho Filho",
        "cpf": "574.440.310-88",
        "tel": "(19)998657481"
    },
]

def populate():
    print('Populando novas contas de usuários...')
    for userData in USER_DATA:
        user = User.objects.filter(email=userData["email"]).first()

        if user is None:
            user = User.objects.create_user(
                email=userData["email"],
                password=userData["password"],
                name=userData["name"],
                cpf=userData["cpf"],
                tel=userData["tel"]
            )
    
    user = User.objects.filter(email="admin@admin.com").first()
    if user is None:
        user = User.objects.create_superuser(
                    email="admin@admin.com",
                    password="admin",
                    name="admin",
                    cpf="999.999.999-99",
                    tel=""
                )