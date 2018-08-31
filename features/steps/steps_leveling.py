from behave import *
import random
import math
from trolls import *


@given('mytroll.level is 1')
def step_impl(context):
    trl = troll.Troll("Tester")
    context.mytroll = trl
    assert context.mytroll.level == 1


@when('i call mytroll.add_exp with random number between 1 and 10000 as X')
def step_impl(context):
    context.rand_X = random.randint(1, 10001)
    context.mytroll.add_exp(context.rand_X)


@then('mytroll.level becomes rounded integer square root of X, minimum 1')
def step_impl(context):
    assert context.mytroll.level == int(math.sqrt(context.rand_X))

