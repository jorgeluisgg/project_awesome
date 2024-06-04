RUN_DOCKER:
	docker run -e PORT=8000 -p 8000:8000 --env-file /home/jorgeluisgg/code/jorgeluisgg/project_awesome/.env api
