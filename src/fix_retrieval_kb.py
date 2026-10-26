from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
KB_PATH = BASE_DIR / "data" / "python_knowledge_base.csv"


NEW_ENTRIES = [
    {
        "question": "What is a string?",
        "answer": "A string is a sequence of characters used to represent text in Python. Strings can be written using single quotes, double quotes, or triple quotes.",
        "category": "Strings",
    },
    {
        "question": "How do I reverse a string?",
        "answer": "You can reverse a string using slicing with [::-1]. For example, text[::-1] returns the characters of text in reverse order.",
        "category": "Strings",
    },
    {
        "question": "What is a function?",
        "answer": "A function is a reusable block of code that performs a specific task. Functions are defined using the def keyword and can accept arguments and return values.",
        "category": "Functions",
    },
    {
        "question": "What is a class?",
        "answer": "A class is a blueprint for creating objects in Python. It defines attributes and methods that describe the data and behavior of those objects.",
        "category": "OOP",
    },
    {
        "question": "What is an exception?",
        "answer": "An exception is an error or unexpected event that occurs while a Python program is running. Exceptions can be handled using try and except blocks.",
        "category": "Exceptions",
    },
    {
        "question": "How do I handle exceptions?",
        "answer": "You can handle exceptions using try and except blocks. Put code that may raise an exception inside try, and use except to handle the error.",
        "category": "Exceptions",
    },
    {
        "question": "What is a for loop?",
        "answer": "A for loop is used to iterate over the items of a sequence or other iterable, such as a list, tuple, string, or range.",
        "category": "Loops",
    },
    {
        "question": "What is a while loop?",
        "answer": "A while loop repeatedly executes a block of code as long as its condition remains true.",
        "category": "Loops",
    },
    {
        "question": "How do I open a file?",
        "answer": "You can open a file using Python's open() function. For example, file = open('example.txt', 'r') opens a text file for reading.",
        "category": "File Handling",
    },
    {
        "question": "What is variable scope?",
        "answer": "Variable scope determines where a variable can be accessed in a Python program. Common scopes include local, enclosing, global, and built-in scope.",
        "category": "Advanced",
    },
]


def main():

    if not KB_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KB_PATH}"
        )

    df = pd.read_csv(KB_PATH)

    required_columns = {
        "question",
        "answer",
        "category",
    }

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Expected columns: {required_columns}"
        )

    existing_questions = {
        str(question).strip().lower()
        for question in df["question"].dropna()
    }

    added = 0

    for entry in NEW_ENTRIES:

        key = entry["question"].strip().lower()

        if key not in existing_questions:

            df = pd.concat(
                [
                    df,
                    pd.DataFrame([entry]),
                ],
                ignore_index=True,
            )

            existing_questions.add(key)
            added += 1

    df.to_csv(
        KB_PATH,
        index=False,
    )

    print("=" * 60)
    print("TARGETED KNOWLEDGE BASE UPDATE")
    print("=" * 60)
    print(f"Entries added : {added}")
    print(f"Total entries : {len(df)}")
    print("=" * 60)


if __name__ == "__main__":
    main()