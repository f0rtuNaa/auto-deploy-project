# Sales Automation

Автоматизация обработки кассовых данных для торговой сети. Скрипты генерируют CSV-выгрузки из кассового ПО, а затем загружают их в PostgreSQL.

## Структура репозитория

```
.
├── generate-sales-data.py   # Генерация CSV-выгрузок + импорт в БД
├── pgdb.py                    # Класс PGDatabase для работы с PostgreSQL
├── utils.py                 # Вспомогательные функции
├── config.ini               # Конфигурация проекта
├── start.bat                # Запуск через планировщик Windows
├── data/
│   └── 1_1.csv              # Пример сгенерированной выгрузки
├── sql/
│   └── CreateTable.sql    # DDL-команда для создания таблицы
└── img/
    ├── CompletedTable.png  # Скриншот заполненной таблицы после запуска скрипта
    ├── EmptyTable.png      # Скриншот пустой таблицы перед запуском скрипта
    ├── TaskAfterWork.png   # Скриншот планировщика Windows после выполнения скрипта
    └── TaskBeforeWork.png  # Скриншот планировщика Windows перед выполнением скрипта
```

## Схема базы данных

```sql

CREATE TABLE public.sales (
	doc_id varchar NULL,
	item varchar NULL,
	category varchar NULL,
	amount int4 NULL,
	price numeric NULL,
	discount numeric NULL,
	shop varchar NULL,
	cash varchar NULL,
	id serial4 NOT NULL,
	CONSTRAINT sales_pk PRIMARY KEY (id)
);
```

Файл с полным DDL: [`sql/CreateTable.sql`](sql/CreateTable.sql)

## Формат CSV-выгрузки

Файлы называются `{shop_num}_{cash_num}.csv` — номер магазина и номер кассы.  
Пример: `11_2.csv` — магазин №11, касса №2.

| Поле | Тип | Пример |
|------|-----|--------|
| `doc_id` | string | `PLW-75345` |
| `item` | string | `Гель для посуды Fairy 900мл` |
| `category` | string | `Бытовая химия` |
| `amount` | int | `3` |
| `price` | float | `189.0` |
| `discount` | float | `9.45` |

Один чек (`doc_id`) может содержать несколько строк с разными товарами.

## Запуск на новой машине

### 1. Клонировать репозиторий

```bash
git clone https://github.com/f0rtuNaa/auto-deploy-project.git
cd retail-automation
```

### 2. Создать и активировать виртуальное окружение

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать базу данных

Подключись к PostgreSQL и выполни:

```sql
CREATE DATABASE salesdata;
```

Затем применить DDL.

### 5. Настроить config.ini

Открыть `config.ini` и прописать свои параметры подключения:

```ini
[Database]
HOST     = localhost
DATABASE = retail
USER     = postgres
PASSWORD = your_password
```

При необходимости скорректировать магазины и кассы:

```ini
[Shops]
SHOPS = {1: 3, 2: 2, 11: 3}
```

> Сохранить `config.ini` в кодировке **UTF-8**.

### 6. Запустить вручную

```bash
python generate-sales-data.py
```

Скрипт создаст CSV-файлы в папке `data/` и загрузит их в БД.  
В воскресенье генерация автоматически пропускается.

### 7. Автоматизация — Планировщик Windows

Сначала необходимо открыть файл `start.bat`, затем прописать полный путь интерпретатора проекта и путь исполняемого файла.
Содержимое `start.bat`:
```bat
chcp 65001
C:\path\to\venv\Scripts\python.exe C:\path\to\generate-sales-data.py
```
Далее для настройки автоматизации выполнить следующие действия:

1. Открыть **Планировщик заданий** → Создать простую задачу
2. Триггер: **Ежедневно** в нужное время
3. Действие: **Запустить программу**
   - Программа: полный путь к `start.bat`


