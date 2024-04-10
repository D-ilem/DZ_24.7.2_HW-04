import os

import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """
    Проверяем вход с невалидным email и валидным password
    """
    # отправляем запрос на авторизацию с неправильными данными
    status, result = pf.get_api_key(email=invalid_email, password=invalid_password)
    # проверяем статус
    assert status == 403


def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """
    Проверяем вход с невалидным email и валидным password
    """
    # отправляем запрос на авторизацию с неправильными данными
    status, result = pf.get_api_key(email=invalid_email, password=invalid_password)
    # проверяем статус
    assert status == 403


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """
    Проверяем вход с невалидными данными
    """
    # отправляем запрос на авторизацию с неправильными данными
    status, result = pf.get_api_key(email=invalid_email, password=invalid_password)
    # проверяем статус
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Жук', animal_type='beatle',
                                     age='1', pet_photo='images/zuk.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # # Получаем полный путь к изображению питомца
    # pet_photo = os.path.join(project_root, pet_photo)
    #
    # # Запрашиваем ключ API и сохраняем в переменную auth_key
    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    #
    # # Добавляем питомца
    # status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


@pytest.mark.xfail
def test_add_new_pet_with_gravity_photo(name='Король', animal_type='кроль',
                                        age='1', pet_photo='images/gravity_photo.png'):
    """Проверяем что сайт не станет добавлять питомца с фото > 20 мб"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом = 500
    assert status == 500
    assert result['name'] == name


'''BUG 0,0 - питомец добавляется (медленно) c фото весом 133мб
При "assert status" == 200" и 'assert result['name'] == name' тест не замечает ошибку.'''


@pytest.mark.xfail
def test_add_new_pet_with_data_strange(name='111', animal_type='222',
                                       age='1', pet_photo='images/zuk.jpg'):
    """Проверяем что можно добавить питомца с некорректными данными.
    В name и animal_type меняем тип данных с str на int"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name


'''BUG 000 - питомец добавляется c именем и видом обозначенными числами
При "assert status" == 200" и 'assert result['name'] == name' тест не замечает ошибку.'''


@pytest.mark.xfail
def test_add_new_pet_with_age_letter(name='Хитин', animal_type='шестиног', age='три', pet_photo='images/zuk.jpg'):
    """Проверка невозможности добавления питомца с невалидным вводом age не int, а str """

    # Получаем путь до файла с картинкой "os.path.join(os.path.dirname(__file__), pet_photo)", сохраняем в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert статус код должен быть 4ХХ , реализуем проверку через не равно 200
    assert status == 400
    assert result['age'] != age


'''BUG 001 - питомец добавляется c возрастом обозначенным буквами
При "assert status" == 200" и 'assert result['age'] == age' тест не замечает ошибку.'''


@pytest.mark.xfail
def test_add_new_pet_with_age_negative(name='Хитин', animal_type='шестиног', age='-3', pet_photo='images/zuk.jpg'):
    """Проверка невозможности добавления питомца с невалидным вводом отрицательного значения age """

    # Получаем путь до файла с картинкой "os.path.join(os.path.dirname(__file__), pet_photo)", сохраняем в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # получаем api ключ ('pf.get_api_key(valid_email, valid_password), записываем в переменную (auth_key)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # добавляем используя полученный ключ список питомцев "pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)", записываем в переменную result
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # сверяем полученные данные по имени питомца (name) с ожидаемыми c помощью метода assert статус код должен быть 4ХХ , реализуем проверку через не равно 200
    assert status == 400
    assert result['age'] == age


'''BUG 002 - питомец добавляется c отрицательным возрастом
При "assert status" == 200" тест не замечает ошибку.'''


def test_add_new_pet_only_photo(pet_photo='images/palochka.jpg'):
    """Проверяем возможность добавления фото питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    # Проверяем, есть ли уже фотография у питомца
    if my_pets['pets'][0]['pet_photo'] == "":
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        print("У питомца уже есть фото")


@pytest.mark.xfail
def test_unsuccessful_pet_invalid_photo(name='Роман', animal_type='текст', age='1', pet_photo='images/words.docx'):
    """Проверяем, что при добавлении питомца с файлом неподдерживаемого формата (не JPG, JPEG или PNG) сервер вернет
    ошибку 415 и питомец не будет добавлен"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пытаемся добавить питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Ожидаем, что в ответе будет статус 415 и питомец будет добавлен без фото
    assert status == 415
    assert result['name'] == name


'''
BUG 003 - питомец добавляется (без картинки)
Декоратор @pytest.mark.xfail() означает, что тест при выполнении должен ожидаемо выдать ошибку.
Вызов этого декоратора переводит функцию test_unsuccessful_pet_invalid_photo() в разряд XFAIL.
При "assert status" == 200" тест не замечает ошибку.
'''


def test_add_new_pet_without_photo(name='Бык', animal_type='копытное',
                                   age='7'):
    """Проверяем что можно добавить питомца с корректными данными без фотографии"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Палочка", "Helicobacter pylori", "1", "images/palochka.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Бацылл', animal_type='Shigella', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
