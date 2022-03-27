from core.models import Category

data = [
    "Outras",
    "Bares & Restaurantes",
    "Comida & Supermercado",
    "Lazer & Entretenimento",
    "Educação",
    "Saúde & Farmácias",
    "Viagem"
]

def populate():
    print('Populando novas categorias...')
    for item in data:
        obj = Category.objects.filter(readableText=item).first()

        if obj is None:
            obj = Category(
                readableText=item
            )
            obj.save()