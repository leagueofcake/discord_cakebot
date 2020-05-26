gen_db:
	PYTHONPATH=$(abspath .) python ./scripts/gen_db.py

run_bot:
	PYTHONPATH=$(abspath bot) ./scripts/run_bot.sh

docker_build:
	docker build -t discord_cakebot .

docker_run:
	make docker_build && docker run -it --rm --name discord_cakebot discord_cakebot
