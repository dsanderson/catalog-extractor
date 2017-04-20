.PHONY: all git

all:
	docker build -t web-ppl-testing .
	docker run web-ppl-testing

git:
	git add -u
	git commit -m "Autocommit"
	git push
