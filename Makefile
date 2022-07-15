env?=production
start:
	python3 server.py
start_dev:
	FLASK_ENV=development python3 server.py --logs=debug
clear:
	tools/clear.py --all
