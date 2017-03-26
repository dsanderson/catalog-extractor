FROM library/node:7-wheezy
RUN ["npm","install","-g","webppl"]

COPY ["test_ppl.ppl", "test_ppl.ppl"]

CMD ["webppl", "test_ppl.ppl"]
