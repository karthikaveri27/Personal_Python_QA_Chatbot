from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
KB_PATH = BASE_DIR / "data" / "python_knowledge_base.csv"


NEW_ENTRIES = [
    {
        "question": "What is a list?",
        "answer": "A list is an ordered, mutable collection in Python that can store multiple values. Lists are created using square brackets, for example [1, 2, 3].",
        "category": "Lists",
    },
    {
        "question": "How do I create a list?",
        "answer": "You can create a list using square brackets, for example numbers = [1, 2, 3]. You can also create an empty list using [].",
        "category": "Lists",
    },
    {
        "question": "What is a tuple?",
        "answer": "A tuple is an ordered, immutable collection in Python. Tuples are commonly written using parentheses, for example (1, 2, 3).",
        "category": "Data Structures",
    },
    {
        "question": "How do I create a tuple?",
        "answer": "You can create a tuple using parentheses, for example values = (1, 2, 3). A single-element tuple requires a trailing comma, such as (5,).",
        "category": "Data Structures",
    },
    {
        "question": "What is a dictionary?",
        "answer": "A dictionary is a mutable collection that stores data as key-value pairs. It is created using curly braces, for example {'name': 'Karthi', 'age': 24}.",
        "category": "Dictionaries",
    },
    {
        "question": "How do I create a dictionary?",
        "answer": "You can create a dictionary using curly braces with key-value pairs, for example student = {'name': 'Karthi', 'age': 24}. You can also create an empty dictionary using {}.",
        "category": "Dictionaries",
    },
    {
        "question": "What is a set?",
        "answer": "A set is an unordered collection of unique elements in Python. Sets are created using curly braces, for example {1, 2, 3}.",
        "category": "Data Structures",
    },
    {
        "question": "How do I create a set?",
        "answer": "You can create a set using curly braces, for example numbers = {1, 2, 3}. An empty set must be created using set(), because {} creates an empty dictionary.",
        "category": "Data Structures",
    },
]


def main():
    if not KB_PATH.exists():
        raise FileNotFoundError(f"Knowledge base not found: {KB_PATH}")

    df = pd.read_csv(KB_PATH)

    required_columns = {"question", "answer", "category"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Expected columns {required_columns}, but found {set(df.columns)}"
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
                [df, pd.DataFrame([entry])],
                ignore_index=True
            )
            existing_questions.add(key)
            added += 1

    df.to_csv(KB_PATH, index=False)

    print("=" * 60)
    print("KNOWLEDGE BASE UPDATED")
    print("=" * 60)
    print(f"Knowledge base: {KB_PATH}")
    print(f"Entries added : {added}")
    print(f"Total entries : {len(df)}")
    print("=" * 60)


if __name__ == "__main__":
    main()