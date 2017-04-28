.PHONY: run

run:
	docker build -t cat-test .
	docker run -v c:\Users\dsa\Documents\GitHub\catalog-extractor\data:c:\data cat-test
