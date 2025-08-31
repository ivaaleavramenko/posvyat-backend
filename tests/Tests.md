Сперва запустите сервак

1. Создай тестовые данные (тебе же нужно с чем-то работать) <br>
```python3 manage.py shell``` <br>

---

2. Выполни в джанго-шелле команды:
```
from registration.models import EventWave, BlackList

# Создайте тестовые волны
wave1 = EventWave.objects.create(name="Волна 1", max_capacity=3, current_count=0, is_active=True)
wave2 = EventWave.objects.create(name="Волна 2", max_capacity=2, current_count=0, is_active=False)

# Добавьте людей в черный список
BlackList.objects.create(first_name="Роман", last_name="Ковалев", reason="Тестовая запись")
BlackList.objects.create(first_name="Максим", last_name="Афонии", reason="Зайцы на мероприятии")

print("Тестовые данные созданы!")
```

---

3. Непосредственно сами тесты. Предварительно выйди из джанго-шелл, это надо выполнять в обычном терминале. <br>
    3.1 Проверка черного списка:
    ```
    # Человек ЕСТЬ в черном списке
    curl -X POST http://127.0.0.1:8000/api/blacklist/check_visitor/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Роман", "last_name": "Ковалев"}'

    # Человека НЕТ в черном списке  
    curl -X POST http://127.0.0.1:8000/api/blacklist/check_visitor/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Иван", "last_name": "Иванов"}'
    ```

    3.2 Тестирование регистрации
    ```
    # Успешная регистрация (без волны)
    curl -X POST http://127.0.0.1:8000/api/visitors/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Иван", "last_name": "Иванов"}'

    # Успешная регистрация (с волной)
    curl -X POST http://127.0.0.1:8000/api/visitors/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Петр", "last_name": "Петров", "wave_id": 1}'

    # Попытка регистрации человека из черного списка
    curl -X POST http://127.0.0.1:8000/api/visitors/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Роман", "last_name": "Ковалев", "wave_id": 1}'

    # Регистрация на неактивную волну
    curl -X POST http://127.0.0.1:8000/api/visitors/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Сергей", "last_name": "Сергеев", "wave_id": 2}'
    ```

    3.3 Проверка лимимта волны
    ```
    # Заполните волну до предела
    curl -X POST http://127.0.0.1:8000/api/visitors/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Анна", "last_name": "Иванова", "wave_id": 1}'

    curl -X POST http://127.0.0.1:8000/api/visitors/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Мария", "last_name": "Петрова", "wave_id": 1}'

    # Попытка регистрации сверх лимита
    curl -X POST http://127.0.0.1:8000/api/visitors/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Олег", "last_name": "Олегов", "wave_id": 1}'
    ```

    3.4 Просмотр данных (эти же ссылки можно открыть прямо в браузере)
    ```
    # Посмотреть всех посетителей
    curl http://127.0.0.1:8000/api/visitors/

    # Посмотреть все волны
    curl http://127.0.0.1:8000/api/waves/
    ```

    3.5 Синхронизация чёрного списка (У МЕНЯ НЕ РАБОТАЕТ)
    ```
    # Синхронизация с Supabase
    curl -X POST http://127.0.0.1:8000/api/blacklist/sync_blacklist/
    ```

    3.6 Проверка работы волн
    ```
    # Активировать/деактивировать волну
    curl -X POST http://127.0.0.1:8000/api/waves/1/toggle_active/
    ```