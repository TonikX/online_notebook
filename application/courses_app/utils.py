def get_object_or_none(model, filtering_features):
    """
    Функция позволяет получить экземляр модели,
    либо убедиться, что такового не существует
    :param model: Модель, по которой осуществлять поиск
    :param filtering_features: Признаки фильтрации
    :return: Экземпляр модели или None
    """
    objects = model.objects.filter(**filtering_features)

    return objects.first() if objects.count() == 1 else None



