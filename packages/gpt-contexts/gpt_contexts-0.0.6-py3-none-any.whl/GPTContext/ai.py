from __future__ import annotations
from json import JSONDecodeError

import openai
import json
from typing import *
from dataclasses import dataclass, field
from .schema import GPTContext, write_schema


class ContextClient:
    def __init__(self, api_key: str, task_text: str, rules: Rules = None):
        self.api_key = api_key
        self.task_text = task_text
        self.rules = rules
    def create_task(self, inputs: GPTContext | List[GPTContext], output: Type[GPTContext], object_context: bool = False) -> dict:
        result = create_task(self.api_key, self.task_text, inputs, output, rules=self.rules, object_context=object_context)
        return result


class InvalidJson(Exception):
    def __init__(self, data: str, message="Unable to process json returned by gpt"):
        self.data = data
        self.message = message
        super().__init__(self.message)

@dataclass
class Rules:
    # main rules
    follow_input_and_output: bool = field(default=True)
    output_must_be_json: bool = field(default=True)
    output_must_follow_schema: bool = field(default=True)

    treat_numbers_as_currency: bool = field(default=False)

    others: List[str] = field(default_factory=list)

    @property
    def flatten(self) -> str:
        rules = ["All inputs will be valid json"]
        if self.follow_input_and_output:
            rules.append("Follow the Input and Output formats provided")
        if self.output_must_be_json:
            rules.append("All outputs must be valid json")
        if self.output_must_follow_schema:
            rules.append("All outputs must follow the schema provided")

        if self.treat_numbers_as_currency:
            rules.append("Treat all integers as USD currency")

        for rule in self.others:
            rules.append(rule)
        return "\n- ".join(rules)


def create_task(api_key: str, task: str, input_obj: GPTContext | List[GPTContext], output_obj: Type[GPTContext],
                rules: Rules = None, object_context: bool = False) -> dict | None:
    openai.api_key = api_key
    if rules is None:
        rules = Rules()
    if isinstance(input_obj, list):
        temp_input_obj = input_obj[0]
        input_data = []
        for item in input_obj:
            input_data.append(item.flatten)
    else:
        temp_input_obj = input_obj
        input_data = input_obj.flatten

    if object_context:
        context_str = f"Input Object Name: {temp_input_obj.__class__.__name__}\nOutput Object Name: {output_obj.__name__}"
    else:
        context_str = ""

    messages = [
        {
            "role": "system",
            "content": "You are a program that completes the following task and responds with valid json.\n\n"
                       ""
                       f"Task:\n{task}\n\n\n"
                       f"Rules:\n- {rules.flatten}\n\nInput Format:\n{str(temp_input_obj.schema)}\n\nOutput Format:\n{str(write_schema(output_obj))}\n\n{context_str}\n\n"
        },
        {"role": "user", "content": str(input_data)}
    ]
    # print(messages[0]["content"])
    # print(messages[1]["content"])
    # return
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        # stop=[".............."]

    )
    try:
        loaded_resp = dict(response["choices"][0]["message"]["content"])
    except ValueError:
        try:
            loaded_resp = json.loads(response["choices"][0]["message"]["content"])
        except JSONDecodeError:
            print(repr(response["choices"][0]["message"]["content"]))
            raise InvalidJson(response["choices"][0]["message"]["content"])

    return loaded_resp
