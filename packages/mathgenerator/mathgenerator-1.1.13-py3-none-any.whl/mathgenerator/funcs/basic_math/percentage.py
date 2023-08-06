from .__init__ import *


def percentageFunc(maxValue=99, maxpercentage=99):
    a = random.randint(1, maxpercentage)
    b = random.randint(1, maxValue)
    problem = f"What is {a}% of {b}?"
    percentage = a / 100 * b
    formatted_float = "{:.2f}".format(percentage)
    solution = f"{formatted_float}"
    return problem, solution


percentage = Generator("Percentage of a number", 80, "What is a% of b?",
                       "percentage", percentageFunc,
                       ["maxValue=99", "maxpercentage=99"])
