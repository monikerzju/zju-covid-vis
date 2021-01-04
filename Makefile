default: all

json:
	@python3 ./src/python/auto.py

all: json
	@npm run start
