curl -d "name=Water Games" -X POST  http://127.0.0.1:5000/categories
curl -d "name=Old School Games" -X PUT http://127.0.0.1:5000/categories/1
curl -X DELETE http://127.0.0.1:5000/categories/8
curl http://127.0.0.1:5000/categories

# toys

curl http://127.0.0.1:5000/toys
curl http://127.0.0.1:5000/toys/2
curl -d "name=rdn-toy-ziififkq&description=rdn-descr-rbqwegoi&price=200&category=Boardgames" -X POST http://127.0.0.1:5000/toys
curl -d "name=Checkers" -X PUT http://127.0.0.1:5000/toys/4
curl -X DELETE http://127.0.0.1:5000/toys/4

# elves
curl http://127.0.0.1:5000/elves
curl http://127.0.0.1:5000/elves/1
curl -d "first_name=Cathrine&last_name=Kohler&login=login-xszce&password=pwd-dchfkqid" -X POST http://127.0.0.1:5000/elves
curl -d "last_name=Elfman&login=Tlfman" -X PUT http://127.0.0.1:5000/elves/3
curl -d "first_name=Gudrun&last_name=Fay&login=login-gaohh&password=pwd-rrrkttef" -X PUT http://127.0.0.1:5000/elves/4
curl -X DELETE http://127.0.0.1:5000/elves/3

# wishes
curl http://127.0.0.1:5000/wishes
curl -d "childname=Bobby&toy=Chess" -X POST http://127.0.0.1:5000/whishes


# schedules
curl "http://127.0.0.1:5000/schedules?login=login-gaohh&password=pwd-rrrkttef"
curl -X PUT http://127.0.0.1:5000/schedules/2/done


