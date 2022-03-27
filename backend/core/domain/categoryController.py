from core.models import Category

def getCategories():
    return Category.objects.filter()