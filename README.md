Проект делают - Ktulhu777 and VKalaitanov

Проект состоит из 5 приложений, а именно:

1. Cart - в данном приложении вся логика корзины(работает через сессии) и оформления заказа.

2. Product - самое основное приложение с API:
Вывод всех товаров с группировкой по рейтингу, есть возможность фильтрации по цене и тд, так же и с пагинацией;
Разработаны GET, POST, DELETE, PUT запросы к отзывам;
Вывод всех категорий если в url не указано название категории, если указано вывод всех товаров связанных с этой категорией если есть хотя бы 1 товар;
Добавление, удаление лайков у товара, так же вывод всех пролайканных товаров.

3. Search - приложение связанное с ElasticSearch.

4. Users - в приложении реализовано вся логика юзера. Регистрация происходит через активацию по Email, когда юзер переходит по ссылке профиль становится активным. Так же можно работать через JWT токены.

5. Telegrambot - асинхронный телеграм бот реализованный на aiogram, делался как дополнение к сайту(не доработан).

6. И прочие файлы - docker файлы, manage.py, директория с настройками sportpit, requirements.txt и т.д
Проект стоит на сервере url -> "https://project-pit.ru/" ФРОНТЕНД НЕ ДОРАБОТАН.