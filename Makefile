install:

	python -m venv venv
	. venv/bin/activate ; pip install robotframework --upgrade pip
	. venv/bin/activate ; pip install requests
	. venv/bin/activate ; pip install docutils
	sudo apt install sqlite3
	cd ./services ; docker build -t flask_bluerint:latest .
	sqlite3 mydatabase.db ".read init.sql"
	
run:

	docker run -d -p 5000:5000 --name flask_blueprint_service flask_bluerint:latest

down:

	docker stop flask_blueprint_service

console:

	sqlite3 mydatabase.db

show:

	docker ps
	docker ps -a

flush:

	docker rm flask_blueprint_service
	docker rmi flask_bluerint:latest

	