from field import Field, fielded
import inspect


def process_1(data: dict = {}):
    print(id(data))


@fielded
def process_2(data: dict = Field(default_factory=dict)):
    print(id(data))

process_1()
process_1()

process_2()
process_2()

ba = inspect.signature(process_2).bind(process_2)
a = ba.arguments