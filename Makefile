.PHONY: status check checkpoint new-exp new-skill test
status:
	python3 -m arca_cli status
check:
	python3 -m arca_cli check
checkpoint:
	python3 -m arca_cli checkpoint
new-exp:
	@echo './arca experiment new "experiment title"'
new-skill:
	@echo 'python3 scripts/new_skill.py skill-name "When to invoke"'
test:
	python3 -m unittest discover -s tests -v
