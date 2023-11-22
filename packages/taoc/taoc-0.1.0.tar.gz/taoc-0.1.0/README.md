# TAOC
A system for doing Advent of Code in python.

> Note: to set your session, please put it in the environment variable `AOC_SESSION` or `~/.config/aocd/token`.

To use, just do this:
```py
from taoc import solution

# day and year are optional, but parens forced
@solution(day=1, year=2022)
def mysolution(input: str):
    ...
    return answer

if __name__ == "__main__":
    # attempt=True will make it try to autosubmit the result
    print(mysolution(attempt=True))
```