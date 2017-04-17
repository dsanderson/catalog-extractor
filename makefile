.PHONY: all

all:
	docker build -t web-ppl-testing .
	docker run web-ppl-testing
