from param import Param, params

@params
def say(message: str = Param(default="Hello, World!")):
    print(message)

say("Hello, Bob!")