# Проект Alfa 

# 1 Структура проекта

1. API&AI - сервис Django Rest Framework (DRF) + модули для работы с искусственный интеллект (AI)
2. front -фронт

# 2 Настройка и сборка сервис API + AI 

Приводим пример настройки проекта в контейнере Docker, что значительно упрощает первоночальную настройк, поэтому необходимл предварительно установить ```dockeer``` и ```docker-compose```. 

создайте пустой каталог:
```mkdir alfa```

перейдите в созданный каталог:
```cd alfa```

импортируйте проект из github в текущий каталог:
```git clone https://github.com/salfa-ru/leaders2022.git .```


Настройка проекта осуществляется в каталоге drf/config, все параметры соответствую параметрами проекта django, в формате yaml.

В каталоге могу содержаться следующие файлы:
* settings.yaml - хранятся базовые настройки проекта (обязательный файл)
* .secrets.yaml - хранятся настройки для локальной отладки и тестирования (не обязательный файл)

Для настройки продуктивной базы необходимо добавить строку в файле ```config/.secrets.yaml```:
  * ```DEBUG: false```

Проект собираетсяна трех контейнерах:

*drf_db_1 - контейнер с базой данных PostgresSQL
*drf_web_1 - контейнер с сервсисом gunicorn, Django Rest Framework, и модулем искусственного интелекта
*drf_nginx_1 - контейнер с сервисом nginx

Сборка и запуск контейнеров
```docker-compose up -d --build```

# 4. Описание

## 4.1 Описание API&AI

Сервис API работает на порту 8000.

Доступе сервис свагер ```http://host:8000/```
![image](https://user-images.githubusercontent.com/42509323/200182544-5f6e02ea-2e3d-4281-976f-ac5fe3a8541b.png)

предустановлены пользователи/пароли "user1/123", ..., "user6/123"

Доступна стандартная админка базы данных: ```http://host:8000/admin/```
Доступ осуществляется через предустановленный имя пользователя и пароля "admin/admin"

![image](https://user-images.githubusercontent.com/42509323/200182266-6f17acce-1984-4525-9ea2-f2b95b670fe5.png)

