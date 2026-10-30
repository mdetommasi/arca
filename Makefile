.PHONY: check checkpoint new-exp new-skill
check:
	python3 scripts/arca_check.py
checkpoint:
	python3 scripts/session_checkpoint.py
new-exp:
	@echo 'python3 scripts/new_experiment.py "experiment title"'
new-skill:
	@echo 'python3 scripts/new_skill.py skill-name "When to invoke"'
