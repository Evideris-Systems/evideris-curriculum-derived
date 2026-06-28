.PHONY: check schema-check validate completeness self

check: schema-check validate completeness
	@echo "✓ All derived-layer checks passed."

schema-check:
	@python3 scripts/validate.py --self

validate:
	@python3 scripts/validate.py

completeness:
	@python3 scripts/completeness.py

self: schema-check
