HLOOKUP := $(shell which hfst-lookup)

xmls:
	@find . -type file -name "*.xml" -print0 | xargs -0 xmllint --format 1>err.tmp
	@rm err.tmp

lexicon: xmls
	HLOOKUP=$(HLOOKUP) sh scripts/checksemclasses.sh
	HLOOKUP=$(HLOOKUP) sh scripts/testlexicon.sh
	HLOOKUP=$(HLOOKUP) sh scripts/checkgrammartags.sh

check: lexicon

