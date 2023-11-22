from typing import *
import types
import builtins
from datetime import datetime

builtin_types = [getattr(builtins, d) for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
builtin_types += [datetime]


def write_schema(input_data: object) -> dict:
    output = {}
    type_hints = get_type_hints(input_data)
    # type_hints = input_data.__annotations__
    for index, (key, value) in enumerate(type_hints.items()):



        # print("\n")
        str_val = str(value)
        try:
            issubclass(value, str)
        except TypeError:
            value = type(value)
        # print(str_val)
        # print(type(value))
        type_indicator = None
        if str_val.startswith("typing."):
            if str_val.startswith("typing.List"):
                # get the type hints inside the List type hint
                list_args = type_hints.get(key).__args__
                # make sure that the object is a subclass
                if issubclass(list_args[0], GPTContext):
                    class_dict = write_schema(list_args[0])
                    type_indicator = f"List[{class_dict}]"
                else:
                    type_indicator = str_val.split(".")[1]
            elif str_val.startswith("typing.Tuple"):
                tuple_args = type_hints.get(key).__args__
                temp = []
                for arg in tuple_args:
                    if issubclass(arg, GPTContext):
                        class_dict = write_schema(arg)
                        temp.append(f"{arg.__name__}({str(class_dict)})")
                    else:
                        temp.append(str(arg).split("'")[1])
                type_indicator = f"Tuple[{', '.join(temp)}]"
            elif str_val.startswith("typing.Dict"):
                dict_args = type_hints.get(key).__args__
                temp = []
                for arg in dict_args:
                    if issubclass(arg, GPTContext):
                        class_dict = write_schema(arg)
                        temp.append(f"{arg.__name__}({str(class_dict)})")
                    else:
                        temp.append(str(arg).split("'")[1])
                type_indicator = f"Dict[{', '.join(temp)}]"
        elif issubclass(value, GPTContext):
            type_indicator = write_schema(value)

        elif value is types.UnionType:
            union_args = type_hints.get(key).__args__
            temp = []
            for arg in union_args:
                if issubclass(arg, GPTContext):
                    class_dict = write_schema(arg)
                    temp.append(f"{arg.__name__}({str(class_dict)})")
                else:
                    temp.append(str(arg).split("'")[1])
            type_indicator = f"Union[{', '.join(temp)}]"
        else:
            type_indicator = value.__name__


        output[key] = type_indicator
    return output


class GPTContext:

    @property
    def schema(self) -> dict:
        return write_schema(self)

    @property
    def flatten(self) -> dict:
        flattened = {}
        for attr_name in self.__annotations__.keys():
            current_val = self.__getattribute__(attr_name)
            if type(current_val) not in builtin_types and issubclass(type(current_val), GPTContext):
                flattened_val = current_val.flatten
            elif isinstance(current_val, list) or isinstance(current_val, tuple):
                flattened_val = []
                for item in current_val:
                    if issubclass(type(item), GPTContext):
                        flattened_val.append(item.flatten)
                    else:
                        flattened_val.append(item)
                if isinstance(current_val, tuple):
                    flattened_val = tuple(flattened_val)
            else:
                flattened_val = current_val
            flattened[attr_name] = flattened_val
        return flattened
