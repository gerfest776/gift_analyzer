# Удобный сервис для аналитики данных о пользователях

## Описание работы:

Разработан для магазина подарков, который хочет знать, когда и у какого пользователя день рождения и какой родственник собирается дарить ему подарок, чтобы сделать его рассылку эффективной.

Поставщики данных периодически поставляют в магазин выгрузки с информацией о жителях, их родственниках, днях рождения и городе, в котором они проживают.

## <a name="guides"></a> Инструкции

### <a name="launch-app"></a> Запуск приложения

 * Если вы хотите запустить приложение в продакшн, то не указывайте ваши environments в docker-compose, импользуйте переменные среды, или .env файл. В моем случае тестовые environments указаны в docker-compose для простоты запуска
 
 * Docker Compose

Находясь в папке с файлом `docker-compose.yml` выполнить в терминале:

	docker-compose build
	docker-compose up

### <a name="launch-app"></a> Запуск тестов

Находясь в ` /gift_analyzer ` выполнить в терминале:

	python manage.py test

## <a name="handlers"></a> Реализация REST API

### <a name="post-import"></a> 1: POST /imports
Принимает на вход набор с данными о жителях в формате `json` и сохраняет его с уникальным идентификатором `import_id` .

Пример:

	{
		"villagers": [
			{
				"citizen_id": 1,
				"town": "Москва",
				"street": "Льва Толстого",
				"building": "16к7стр5",
				"apartment": 7,
				"name": "Иванов Иван Иванович",
				"birth_date": " 26.12.1986",
				"gender": "male",
				"relatives": [2] // id родственников
			},
			{
				"citizen_id": 2,
				"town": "Москва",
				"street": "Льва Толстого",
				"building": "16к7стр5",
				"apartment": 7,
				"name": "Иванов Сергей Иванович",
				"birth_date": "17.04.1997",
				"gender": "male",
				"relatives": [1] // id родственников
			},
			{
				"citizen_id": 3,
				"town": "Керчь",
				"street": "Иосифа Бродского"
				"building": "2",
				"apartment": 11,
				"name": "Романова Мария Леонидовна",
				"birth_date": "23.11.1986",
				"gender": "female",
				"relatives": []
			},
			...
		]
	}

В случае успеха возвращается ответ с HTTP статусом `201 Created` и идентификатором импорта:

	HTTP 201
	{
		"data": {
			"import_id": 1
		}
	}

### <a name="patch-citizen"></a> 2: PATCH /imports/$import_id/citizens/$citizen_id
Изменяет информацию о конкретном жителе в конкретной поставке

Пример:

	PATCH /imports/1/citizens/3
	{
		"town": "Москва",
		"relatives": [1]
	}

Возвращается актуальная информация об указанном жителе:

	HTTP 200
	{
		"data": {
				"citizen_id": 3,
				"town": "Москва",
				"street": "Иосифа Бродского"
				"building": "2",
				"apartment": 11,
				"name": "Романова Мария Леонидовна",
				"birth_date": "23.11.1986",
				"gender": "female",
				"relatives": [1]
		}
	}

### <a name="get-citizens"></a> 3: GET /imports/$import_id/citizens

Возвращает список всех жителей для указанного набора данных.

	HTTP 200
	{
		"data": [
			{
				"citizen_id": 1,
				"town": "Москва",
				"street": "Льва Толстого",
				"building": "16к7стр5",
				"apartment": 7,
				"name": "Иванов Иван Иванович",
				"birth_date": " 26.12.1986",
				"gender": "male",
				"relatives": [2,3] // id родственников
			},
			{
				"citizen_id": 2,
				"town": "Москва",
				"street": "Льва Толстого",
				"building": "16к7стр5",
				"apartment": 7,
				"name": "Иванов Сергей Иванович",
				"birth_date": "17.04.1997",
				"gender": "male",
				"relatives": [1] // id родственников
			},
			{
				"citizen_id": 3,
				"town": "Москва",
				"street": "Иосифа Бродского"
				"building": "2",
				"apartment": 11,
				"name": "Романова Мария Леонидовна",
				"birth_date": "23.11.1986",
				"gender": "female",
				"relatives": [1]
			},
			...
		]
	}


### <a name="get-birthdays"></a> 4: GET /imports/$import_id/citizens/birthdays

Возвращает жителей и количество подарков, которые они будут покупать своим ближайшим родственникам, сгруппированных по месяцам из указанного набора данных.

	HTTP 200
	{
		"data": {
			"1": [],
			"2": [],
			"3": [],
			"4": [{
				"citizen_id": 1,
				"presents": 1,
			}],
			"5": [],
			"6": [],
			"7": [],
			"8": [],
			"9": [],
			"10": [],
			"11": [{
				"citizen_id": 1,
				"presents": 1
			}],
			"12": [
				{
					"citizen_id": 2,
					"presents": 1
				},
				{
					"citizen_id": 3,
					"presents": 1
				}
			]
		}
	}

### <a name="get-percentile"></a> 5: GET /imports/$import_id/towns/stat/percentile/age

Возвращает статистику по городам для указанного набора данных в разрезе возраста жителей: p50, p75, p99, где число - это значение перцентиля.


	HTTP 200
	{
		"data": [
			{
				"town": "Москва",
				"p50": 20,
				"p75": 45,
				"p99": 100
			},
			{
				"town": "Санкт-Петербург",
				"p50": 17,
				"p75": 35,
				"p99": 80
			}
		]
	}

Что означает:
 * `"p50": 20,` - 50% жителей меньше 20 лет
 * `"p75": 45,` - 75% жителей меньше 45 лет
