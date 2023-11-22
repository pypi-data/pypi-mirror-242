from enviroment import load_env_vars
from dataclasses import dataclass
from GPTContext.src.GPTContext import GPTContext, Rules, create_task

env_vars = load_env_vars()


@dataclass
class Author(GPTContext):
    name: str


@dataclass
class Book(GPTContext):
    title: str
    author: Author

    description: str


@dataclass
class Review(GPTContext):
    book_title: str
    review: str


author = Author("Angie Thomas")
book = Book("The Hate U Give", author, "Sixteen-year-old Starr Carter moves between two worlds: the poor neighborhood where she lives and the fancy suburban prep school she attends. The uneasy balance between these worlds is shattered when Starr witnesses the fatal shooting of her childhood best friend Khalil at the hands of a police officer.")
rules = Rules(others=["limit response to 20 words"])
task = "Write a negative review about the book. Add heavy criticism towards the author"

result = create_task(env_vars.openai_api_key, task, book, Review, rules, object_context=True)
print(Review(**result))