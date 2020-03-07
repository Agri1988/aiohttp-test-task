For run production environment run command:
docker-compose -f ./docker-compose.yml up --build -d

you can access to UI on 0.0.0.0:5443
(if you would like to change port, you can do that in docker-compose.yml)


For run test environment run command:
docker-compose -f ./docker-compose-test.yml up --build -d

you can find test result in ./test/test_result.txt



API REFERENCE

# GET spares list
GET http://<host>:<port>/spares/


# GET filtered spares list
GET http://<host>:<port>/spares/?field=country&search_data=USA


# create new spares
POST http://<host>:<port>/spares/
Content-Type: application/json

{"name": "Wheel 15\"", "country": "Canada", "car_id": 1}


# update spares
PUT http://<host>:<port>/spares/2/
Content-Type: application/json

{"id": 2, "name": "Wheel 15\"", "country": "Canada", "car_id": 1}


# GET car list
GET http://<host>:<port>/car/


# GET filtered car list
GET http://<host>:<port>/car/?field=name&search_data=Ford Mustang


# create new car
POST http://<host>:<port>/car/
Content-Type: application/json

{"model": "Ford Mustang", "year": 2020}


# update car
PUT http://<host>:<port>/car/2/
Content-Type: application/json

{"id": 2, "model": "Chevrolet Camaro", "year": 2010}


# GET employee list
GET http://<host>:<port>/employee/


# GET filtered employee list
GET http://<host>:<port>/employee/?field=name&search_data=Jane


# create new employee
POST http://<host>:<port>/employee/
Content-Type: application/json

{"name": "zxcc", "surname": "Doe", "patronymic": "Sam daughter", "sex": "female"}


# update employee
PUT http://<host>:<port>/employee/2/
Content-Type: application/json

{"id": 2, "name": "QWER", "surname": "Doe", "patronymic": "Sam daughter", "sex": "female"}