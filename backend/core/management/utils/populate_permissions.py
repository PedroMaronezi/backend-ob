from core.models.consent import OB_PERMISSION_VALUES, OBPermissions

def populate():
    print('Populando novas permissões...')
    for value in OB_PERMISSION_VALUES:
        OBPermissions.objects.create(value=value)

    #TODO: Insert permissions on accounts