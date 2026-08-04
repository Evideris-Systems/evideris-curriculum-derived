.PHONY: check schema-check validate release-hashes completeness self

check: schema-check validate release-hashes completeness
	@echo "✓ All derived-layer checks passed."

schema-check:
	@python3 scripts/validate.py --self

validate:
	@python3 scripts/validate.py

release-hashes:
	@python3 scripts/update-release-hashes.py --root derived releases/*.json

completeness:
	@python3 scripts/completeness.py

self: schema-check
