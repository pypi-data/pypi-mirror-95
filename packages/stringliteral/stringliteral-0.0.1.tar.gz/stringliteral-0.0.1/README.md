[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# stringliteral

```python
from stringliteral import StringLiteral

class AllowedValues(StringLiteral):
    LEFT="left"
    RIGHT="right"

value = AllowedValues.LEFT

AllowedValues.contains("left") # returns True
AllowedValues.contains("up") # returns False
```

Define your class attributes with ALL CAPS only. Non CAP attributes will be ignored.

I created this for my own usage after tripping over using the built in Enum class many, many times..
