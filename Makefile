gen_db:
	PYTHONPATH=$(abspath .) python ./scripts/gen_db.py

run_bot:
	PYTHONPATH=$(abspath bot) ./scripts/run_bot.sh