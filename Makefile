install:
	pip3 install -r requirements.txt

run: install
	python3 main.py

ignore-config-ini:
	git update-index --skip-worktree config.ini

allow-config-ini:
	git update-index --no-skip-worktree config.ini
