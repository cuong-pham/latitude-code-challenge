# Data Engineering Coding Challenges

## Build Docker Image
~~~
docker build . --tag=lat-code-challenge:latest
~~~

## How to run it:
0. Create a tempory directory for test files:
~~~
mkdir -p ~/temp-file/
~~~
1. Create spec file and put in `~/temp-file/`

2. Generate random fixed-width file according to spec:
~~~
docker run -it -v ~/temp-file/:/app/temp-file --rm lat-code-challenge:latest ./generate-fw-file.py --output /app/temp-file/fwf.txt --spec /app/temp-file/spec.json
~~~

3. Convert fixed-width file to csv according to spec:
~~~
docker run -it -v ~/temp-file/:/app/temp-file --rm lat-code-challenge:latest ./fw-to-csv.py --input /app/temp-file/fwf.txt --output /app/temp-file/output.csv --spec /app/temp-file/spec.json
~~~

## Run tests:
~~~
docker run -it --rm lat-code-challenge:latest python tests/test_fixed_width_io.py
~~~

## Judgment Criteria
- Beauty of the code (beauty lies in the eyes of the beholder)
- Testing strategies
- Basic Engineering principles

## Parse fixed width file
- Generate a fixed width file using the provided spec.
- Implement a parser that can parse the fixed width file and generate a csv file. 
- DO NOT use pre built python libraries like pandas for parsing. You can use a library to write out a csv file (If you feel like)
- Language choices (Python or Scala)
- Deliver source via github or bitbucket
- Bonus points if you deliver a docker container (Dockerfile) that can be used to run the code (too lazy to install stuff that you might use)
- Pay attention to encoding



