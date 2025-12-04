# Teisatsu

## WIP DISCLAMER
**Проект находится в ранней стадии разработки, и большинство заявленных функций все еще не работают**


**Teisatsu** - это утилита, которая позволяет разыскивать данные о любых входных данных, которые вы ей дадите.

## Использование
```
usage: teisatsu [-h] [command] ...

will find everything (almost)

positional arguments:
  [command]   teisatsu command
    find      find anyTHING
    list      shows available things

options:
  -h, --help  show this help message and exit

see https://github.com/wandderq/teisatsu
```

## Примеры команд
 - Простой поиск: `teisatsu find google.com`
 - Поиск с отладкой: `teisatsu find localhost -v`
 - Просмотр списка доступных скриптов: `teisatsu list scripts` (WIP)


## Принцип работы
1. Классификация
   Входные данные проходят через **классификатор** - набор скриптов, который присваивает входным данным **теги**.

2. Запуск скриптов и динамичное выведение результатов
    По ранее найденным тегам отбираются нужные **скрипты**, которые находят какую-либо информацию о входных данных
    В этом же этапе происходит очистка информации от лишних данных, а так же выведение результатов в консоль


## Установка
1. Через **pip** (проще всего)
    ```bash
    pip install git+https://github.com/wandderq/teisatsu@main
    ```

2. Через исходный код (для разработки)
    - Клонируем репозиторий
        ```bash
        git clone https://github.com/wandderq/teisatsu
        cd teisatsu
        ```
    
    - Создаем venv (рекомендовано)
        ```bash
        python -m venv .venv
        source .venv/scripts/activate
        ```
    
    - Устанавливаем пакет
        ```bash
        pip install .
        ```


## Лицензия
Этот проект использует [лицензию MIT](LICENSE)