.PHONY: run

run:
	docker build -t cat-test .
	docker run -v c:\Users\dsa\Documents\GitHub\catalog-extractor\data:c:\data cat-test

score:
	docker build -t cat-score .
	docker run -v c:\Users\dsa\Documents\GitHub\catalog-extractor\data:c:\data -p 2234 cat-score
