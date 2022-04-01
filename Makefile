#install deppendencies
install:

	python -m venv venv
	. venv/bin/activate ; python -m pip install -r requirements.txt --upgrade pip
	. venv/bin/activate ; pip install requests
	. venv/bin/activate ; pip install docutils
	sudo apt install sqlite3
	cd ./services ; docker build -t flask_blueprint:latest .
	cd ./services ; docker-compose build
	- sqlite3 mydatabase.db ".read init.sql"
	docker images
	
#run service in syncronous mode to check what is going on	
#you will need another console to run tests and the main app
up:

	cd ./services ; docker-compose up 

#run in detach mode
up_d:

	cd ./services ; docker-compose up -d
	docker ps

#run main app
run:
	. venv/bin/activate ; python main.py

#put docker containers
down:

	cd ./services ; docker-compose down
	docker ps
	docker ps -a

#access sqlite3 console
console:

	sqlite3 mydatabase.db

#show relevatn container info
show:

	docker ps
	docker ps -a

#remove the containers created by this app from you pc
flush:

	- docker rm flask_blueprint_service
	- docker rmi flask_blueprint:latest
	- rm ./testdatabase.db

#access to redis container cli
cli:
	-docker exec -it redis_service redis-cli 


#run automated unittesting
test:

	- rm ./testdatabase.db
	sqlite3 testdatabase.db ".read init.sql"
	. venv/bin/activate ; python test.py
	- rm ./testdatabase.db

#use this in case a local redis server may interfeer with the docker-redis-server
stop_local_redis:
	/etc/init.d/redis-server stop

#put your local redis server back online
start_local_redis:
	/etc/init.d/redis-server start