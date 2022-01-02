
DAY ?= $(shell date +%d)
YEAR ?= $(shell date +%Y)
FILE_TEMPLATE = utils/solution_template.py

.PHONY: solution-dir
solution-dir:
	mkdir aoc21/day${DAY} 	\
	&& cp ${FILE_TEMPLATE} aoc21/day${DAY}/part1.py		\
	&& rpl "year=2021" "year=${YEAR}" aoc21/day${DAY}/part1.py \
	&& rpl "day=1" "day=${DAY}" aoc21/day${DAY}/part1.py \
	&& touch aoc21/day${DAY}/test.txt

.PHONY: part2
part2:
	cp aoc21/day${DAY}/part1.py aoc21/day${DAY}/part2.py

.PHONY: tox
tox:
	python -m tox

.PHONY: deps
deps:  ## Install dependencies
	pip install -r requirements.txt
