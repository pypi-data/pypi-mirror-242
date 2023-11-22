from aocd import get_data, submit
from typing import Callable

def solution(day=None, year=None, part: 'a'|'b' = 'a'):
    def inner(f: Callable[[str], int]):
        def wrapper(attempt=False):
            answer = f(get_data(day=day, year=year))
            if attempt: submit(answer, part=part, day=day, year=year)
            return answer
        return wrapper
    return inner
