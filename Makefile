.PHONY: status check checkpoint new-exp new-skill test package
status:
	python3 arca status
check:
	python3 arca check
checkpoint:
	python3 arca checkpoint
new-exp:
	@echo './arca experiment new "experiment title"'
new-skill:
	@echo 'python3 scripts/new_skill.py skill-name "When to invoke"'
test:
	python3 -m unittest discover -s tests -v
package:
	python3 -m pip wheel --no-deps --wheel-dir .local/dist .
