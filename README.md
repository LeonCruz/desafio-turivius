### Desafio Turivius

Para executar o projeto, primeiro é preciso instalar as dependências:

	pip install -r requirements.txt

ou

	poetry install

Em seguida, em uma janela do terminal, entre na pasta **toscrape/** e execute os
comandos a seguir para realizar as migrações do banco de dados:

	python manager.py makemigrations

e

	python manager.py migrate

Depois execute o comando a seguir para levantar o servidor do Django:

	python manager.py runserver


Em outra janela do terminal, entre na pasta **crawler/** execute o comando:

	python crawler.py


Depois que o crawler tiver sido executado, acesse o link: <http://localhost:8000/books/>
