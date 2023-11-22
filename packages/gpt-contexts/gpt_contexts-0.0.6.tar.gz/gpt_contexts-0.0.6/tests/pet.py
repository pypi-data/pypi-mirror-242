from enviroment import load_env_vars
from typing import *
from dataclasses import dataclass
from GPTContext.GPTContext import GPTContext, Rules, create_task


env_vars = load_env_vars()


@dataclass
class Toy(GPTContext):
    color: str
    price: int


@dataclass
class Dog(GPTContext):
    name: str
    age: int

    favorite_toy: Toy
    favorite_toys: List[Toy]


@dataclass
class DogDesc(GPTContext):
    name: str
    description: str


def test_single():
    bob_toys = [Toy("red", 5), Toy("blue", 6), Toy("green", 7)]

    bob = Dog("Bob", 5, bob_toys[1], bob_toys)
    rules = Rules(treat_numbers_as_currency=True)
    task = "write a description for each pet based on the provided characteristics"
    result = create_task(env_vars.openai_api_key, task, bob, DogDesc, rules=rules)
    print(DogDesc(**result))


def test_multi():
    bob_toys = [Toy("red", 5), Toy("blue", 6), Toy("green", 7)]
    jade_toys = [Toy("pink", 10), Toy("orange", 600), Toy("yellow", 799)]

    bob = Dog("Bob", 5, bob_toys[1], bob_toys)
    jade = Dog("Jade", 14, jade_toys[1], jade_toys)

    rules = Rules(treat_numbers_as_currency=True)
    task = "write a description for each pet based on the provided characteristics"
    result = create_task(env_vars.openai_api_key, task, [bob, jade], DogDesc, rules=rules, object_context=True)
    for res in result:
        print(DogDesc(**res))


test_multi()
