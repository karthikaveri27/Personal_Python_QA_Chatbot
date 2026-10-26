from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(exist_ok=True)

knowledge_base = [
    {
        "question": "What is Python?",
        "answer": "Python is a high-level general-purpose programming language known for its readable syntax and broad ecosystem.",
        "category": "Basics",
    },
    {
        "question": "What are the main features of Python?",
        "answer": "Python offers readable syntax, dynamic typing, object-oriented programming, extensive libraries, and cross-platform support.",
        "category": "Basics",
    },
    {
        "question": "What is a variable in Python?",
        "answer": "A variable is a name that refers to an object in Python. You create one by assigning a value such as x = 10.",
        "category": "Basics",
    },
    {
        "question": "How do I print something in Python?",
        "answer": "Use the print() function. For example, print('Hello') displays Hello.",
        "category": "Basics",
    },
    {
        "question": "What are Python data types?",
        "answer": "Common built-in types include int, float, complex, bool, str, list, tuple, set, dict, and NoneType.",
        "category": "Data Types",
    },
    {
        "question": "What is the difference between a list and a tuple?",
        "answer": "A list is mutable while a tuple is immutable. Lists use square brackets and tuples commonly use parentheses.",
        "category": "Data Structures",
    },
    {
        "question": "What is a dictionary in Python?",
        "answer": "A dictionary stores key-value pairs and is written using braces, such as {'name': 'Karthi'}.",
        "category": "Data Structures",
    },
    {
        "question": "What is a set in Python?",
        "answer": "A set is an unordered collection of unique elements. It is useful for membership tests and removing duplicates.",
        "category": "Data Structures",
    },
    {
        "question": "How do I create a list in Python?",
        "answer": "Use square brackets with comma-separated values, for example numbers = [1, 2, 3].",
        "category": "Data Structures",
    },
    {
        "question": "What is list slicing?",
        "answer": "List slicing extracts part of a sequence using syntax such as items[start:stop:step].",
        "category": "Data Structures",
    },
    {
        "question": "What is a string in Python?",
        "answer": "A string is an immutable sequence of Unicode characters and can be created with single or double quotes.",
        "category": "Strings",
    },
    {
        "question": "How do I convert a string to lowercase?",
        "answer": "Call the lower() method, for example text.lower().",
        "category": "Strings",
    },
    {
        "question": "How do I check the length of a string?",
        "answer": "Use the len() function, for example len('Python') returns 6.",
        "category": "Strings",
    },
    {
        "question": "What is an f-string?",
        "answer": "An f-string is a formatted string literal that lets you embed expressions inside braces, for example f'Hello {name}'.",
        "category": "Strings",
    },
    {
        "question": "What are Python operators?",
        "answer": "Python has arithmetic, comparison, assignment, logical, identity, membership, and bitwise operators.",
        "category": "Operators",
    },
    {
        "question": "What does == mean in Python?",
        "answer": "The == operator tests whether two values are equal.",
        "category": "Operators",
    },
    {
        "question": "What does is mean in Python?",
        "answer": "The is operator tests whether two references point to the same object.",
        "category": "Operators",
    },
    {
        "question": "What is the difference between == and is?",
        "answer": "== compares values while is checks object identity.",
        "category": "Operators",
    },
    {
        "question": "How do I write an if statement?",
        "answer": "Use if followed by a condition and a colon, then indent the statements to execute when it is true.",
        "category": "Control Flow",
    },
    {
        "question": "How do I use elif in Python?",
        "answer": "elif adds another condition after an if statement and before an optional else block.",
        "category": "Control Flow",
    },
    {
        "question": "How does a for loop work?",
        "answer": "A for loop iterates over the items of an iterable such as a list, string, range, or dictionary.",
        "category": "Loops",
    },
    {
        "question": "How does a while loop work?",
        "answer": "A while loop repeatedly executes a block while its condition remains true.",
        "category": "Loops",
    },
    {
        "question": "What does range() do?",
        "answer": "range() produces a sequence of integers commonly used for looping a specified number of times.",
        "category": "Loops",
    },
    {
        "question": "What does break do in Python?",
        "answer": "break immediately exits the nearest enclosing loop.",
        "category": "Loops",
    },
    {
        "question": "What does continue do in Python?",
        "answer": "continue skips the rest of the current loop iteration and moves to the next iteration.",
        "category": "Loops",
    },
    {
        "question": "What does pass do in Python?",
        "answer": "pass is a no-operation statement used when syntax requires a statement but no action is needed.",
        "category": "Control Flow",
    },
    {
        "question": "What is a function in Python?",
        "answer": "A function is a reusable block of code defined with def that can accept arguments and return a value.",
        "category": "Functions",
    },
    {
        "question": "How do I define a function?",
        "answer": "Use the def keyword followed by the function name, parameters, and a colon, then indent the function body.",
        "category": "Functions",
    },
    {
        "question": "What is a return statement?",
        "answer": "return ends a function and optionally sends a value back to the caller.",
        "category": "Functions",
    },
    {
        "question": "What are function arguments?",
        "answer": "Arguments are values supplied to a function when it is called. They can be positional or keyword arguments.",
        "category": "Functions",
    },
    {
        "question": "What are default arguments?",
        "answer": "Default arguments are parameters with predefined values used when the caller does not provide those arguments.",
        "category": "Functions",
    },
    {
        "question": "What is *args?",
        "answer": "*args collects extra positional arguments into a tuple inside a function.",
        "category": "Functions",
    },
    {
        "question": "What is **kwargs?",
        "answer": "**kwargs collects extra keyword arguments into a dictionary inside a function.",
        "category": "Functions",
    },
    {
        "question": "What is a lambda function?",
        "answer": "A lambda is a small anonymous function written with the lambda keyword and usually used for short expressions.",
        "category": "Functions",
    },
    {
        "question": "What is a Python module?",
        "answer": "A module is a Python file containing code such as functions, classes, or variables that can be imported into another program.",
        "category": "Modules",
    },
    {
        "question": "How do I import a module?",
        "answer": "Use import followed by the module name, for example import math.",
        "category": "Modules",
    },
    {
        "question": "What is the math module?",
        "answer": "math is a standard-library module providing mathematical functions and constants.",
        "category": "Modules",
    },
    {
        "question": "What is pip?",
        "answer": "pip is the standard Python package installer used to install and manage packages.",
        "category": "Environment",
    },
    {
        "question": "What is a virtual environment?",
        "answer": "A virtual environment is an isolated Python environment that keeps project dependencies separate from other projects.",
        "category": "Environment",
    },
    {
        "question": "How do I create a virtual environment?",
        "answer": "Run python -m venv .venv in the project directory to create a virtual environment named .venv.",
        "category": "Environment",
    },
    {
        "question": "What is exception handling?",
        "answer": "Exception handling lets a program respond to runtime errors using constructs such as try, except, else, and finally.",
        "category": "Exceptions",
    },
    {
        "question": "How do I use try and except?",
        "answer": "Put code that may fail inside try and handle a matching exception in an except block.",
        "category": "Exceptions",
    },
    {
        "question": "What is finally?",
        "answer": "The finally block runs after try and except processing whether or not an exception occurred.",
        "category": "Exceptions",
    },
    {
        "question": "How do I raise an exception?",
        "answer": "Use the raise statement followed by an exception instance or exception class.",
        "category": "Exceptions",
    },
    {
        "question": "What is a class in Python?",
        "answer": "A class is a blueprint for creating objects and defining their attributes and behavior.",
        "category": "OOP",
    },
    {
        "question": "What is an object in Python?",
        "answer": "An object is an instance of a class containing state and behavior defined by that class.",
        "category": "OOP",
    },
    {
        "question": "What is __init__?",
        "answer": "__init__ is an initializer method commonly used to set up an object's attributes when an instance is created.",
        "category": "OOP",
    },
    {
        "question": "What is self in Python?",
        "answer": "self refers to the current object instance inside an instance method.",
        "category": "OOP",
    },
    {
        "question": "What is inheritance?",
        "answer": "Inheritance lets a class derive attributes and methods from another class.",
        "category": "OOP",
    },
    {
        "question": "What is polymorphism?",
        "answer": "Polymorphism allows different object types to provide compatible behavior through a common interface.",
        "category": "OOP",
    },
    {
        "question": "What is encapsulation?",
        "answer": "Encapsulation groups data and methods together and helps control how implementation details are exposed.",
        "category": "OOP",
    },
    {
        "question": "What is a list comprehension?",
        "answer": "A list comprehension creates a list from an iterable using a compact expression with optional filtering.",
        "category": "Comprehensions",
    },
    {
        "question": "What is a dictionary comprehension?",
        "answer": "A dictionary comprehension creates a dictionary using an expression and iteration syntax.",
        "category": "Comprehensions",
    },
    {
        "question": "What is an iterator?",
        "answer": "An iterator is an object that produces values one at a time through the iterator protocol.",
        "category": "Advanced",
    },
    {
        "question": "What is a generator?",
        "answer": "A generator is an iterator commonly created with a function containing yield and produces values lazily.",
        "category": "Advanced",
    },
    {
        "question": "What does yield do?",
        "answer": "yield pauses a generator and produces a value; execution resumes when the generator is advanced again.",
        "category": "Advanced",
    },
    {
        "question": "What is the difference between append and extend?",
        "answer": "append adds one object as a single list element while extend adds each element from an iterable.",
        "category": "Lists",
    },
    {
        "question": "How do I sort a list?",
        "answer": "Use list.sort() to sort the list in place or sorted(list) to create a new sorted list.",
        "category": "Lists",
    },
    {
        "question": "What is sorted()?",
        "answer": "sorted() returns a new list containing the sorted items from an iterable.",
        "category": "Lists",
    },
    {
        "question": "How do I remove an item from a list?",
        "answer": "Use remove(value), pop(index), or del depending on whether you want to remove by value or position.",
        "category": "Lists",
    },
    {
        "question": "What is None in Python?",
        "answer": "None is a singleton object representing the absence of a value or a null-like state.",
        "category": "Basics",
    },
    {
        "question": "What is a Boolean in Python?",
        "answer": "bool is the Boolean type and has two values: True and False.",
        "category": "Data Types",
    },
    {
        "question": "What is type() used for?",
        "answer": "type() returns the type of an object.",
        "category": "Basics",
    },
    {
        "question": "What is isinstance()?",
        "answer": "isinstance() checks whether an object is an instance of a specified class or tuple of classes.",
        "category": "Basics",
    },
    {
        "question": "What is mutable in Python?",
        "answer": "A mutable object can be changed after creation. Lists, dictionaries, and sets are common mutable types.",
        "category": "Data Types",
    },
    {
        "question": "What is immutable in Python?",
        "answer": "An immutable object cannot be changed after creation. Strings, tuples, and integers are common immutable types.",
        "category": "Data Types",
    },
    {
        "question": "What is indentation in Python?",
        "answer": "Indentation defines code blocks in Python and is required for structures such as functions, loops, and conditional statements.",
        "category": "Basics",
    },
    {
        "question": "What is PEP 8?",
        "answer": "PEP 8 is the main style guide for Python code and recommends conventions that improve readability and consistency.",
        "category": "Best Practices",
    },
    {
        "question": "What is a docstring?",
        "answer": "A docstring is a string literal used to document a module, class, function, or method.",
        "category": "Best Practices",
    },
    {
        "question": "What is the Python standard library?",
        "answer": "The standard library is the collection of modules and packages distributed with Python that provide commonly needed functionality.",
        "category": "Modules",
    },
    {
        "question": "How do I read a text file?",
        "answer": "Use open() with an appropriate mode, commonly with a with statement, then call read() or iterate over the file.",
        "category": "File Handling",
    },
    {
        "question": "Why use with open()?",
        "answer": "The with statement manages the file resource and ensures it is properly closed after the block finishes.",
        "category": "File Handling",
    },
    {
        "question": "What are file modes in Python?",
        "answer": "Common modes include r for reading, w for writing or truncating, a for appending, and b for binary mode.",
        "category": "File Handling",
    },
    {
        "question": "How do I write to a file?",
        "answer": "Open the file with a writable mode such as w or a and call write() or writelines().",
        "category": "File Handling",
    },
    {
        "question": "What is JSON in Python?",
        "answer": "The json standard-library module converts between JSON data and Python objects using functions such as loads() and dumps().",
        "category": "Data Formats",
    },
    {
        "question": "How do I convert a Python dictionary to JSON?",
        "answer": "Use json.dumps(dictionary) to produce a JSON-formatted string or json.dump() to write JSON to a file.",
        "category": "Data Formats",
    },
    {
        "question": "What is a package in Python?",
        "answer": "A package is a way to organize related Python modules under a common namespace.",
        "category": "Modules",
    },
    {
        "question": "What is __name__ == '__main__'?",
        "answer": "It checks whether a Python file is being run directly rather than imported as a module.",
        "category": "Basics",
    },
    {
        "question": "What is recursion?",
        "answer": "Recursion is a technique where a function calls itself to solve a problem by reducing it to smaller cases.",
        "category": "Functions",
    },
    {
        "question": "What is a decorator?",
        "answer": "A decorator is a callable that wraps another function or class to extend or modify its behavior.",
        "category": "Advanced",
    },
    {
        "question": "What is map()?",
        "answer": "map() applies a function to each item of an iterable and returns an iterator containing the results.",
        "category": "Built-ins",
    },
    {
        "question": "What is filter()?",
        "answer": "filter() returns an iterator containing items from an iterable for which a supplied function returns true.",
        "category": "Built-ins",
    },
    {
        "question": "What is zip()?",
        "answer": "zip() combines corresponding elements from multiple iterables into tuples.",
        "category": "Built-ins",
    },
    {
        "question": "What is enumerate()?",
        "answer": "enumerate() produces pairs containing an index and the corresponding item while iterating over an iterable.",
        "category": "Built-ins",
    },
    {
        "question": "What does len() do?",
        "answer": "len() returns the number of items in an object that supports the length protocol.",
        "category": "Built-ins",
    },
    {
        "question": "What does input() do?",
        "answer": "input() reads a line of text from standard input and returns it as a string.",
        "category": "Built-ins",
    },
    {
        "question": "How do I convert a string to an integer?",
        "answer": "Use int(text) to convert a suitable string to an integer.",
        "category": "Type Conversion",
    },
    {
        "question": "How do I convert a string to a float?",
        "answer": "Use float(text) to convert a suitable string to a floating-point number.",
        "category": "Type Conversion",
    },
    {
        "question": "What is type conversion?",
        "answer": "Type conversion changes a value from one data type to another using functions such as int(), float(), str(), and list().",
        "category": "Type Conversion",
    },
    {
        "question": "What is a shallow copy?",
        "answer": "A shallow copy creates a new outer object while nested objects are still shared with the original.",
        "category": "Copying",
    },
    {
        "question": "What is a deep copy?",
        "answer": "A deep copy recursively copies nested objects so the copied structure does not share the same nested objects with the original where possible.",
        "category": "Copying",
    },
    {
        "question": "How do I copy a list?",
        "answer": "You can use list.copy(), slicing with [:], or the copy module depending on whether a shallow or deep copy is required.",
        "category": "Copying",
    },
    {
        "question": "What is tuple unpacking?",
        "answer": "Tuple unpacking assigns elements from an iterable to multiple variables in one statement, such as a, b = (1, 2).",
        "category": "Data Structures",
    },
    {
        "question": "What is dictionary get()?",
        "answer": "dict.get(key, default) returns the value for a key or a default value when the key is absent.",
        "category": "Dictionaries",
    },
    {
        "question": "How do I loop through a dictionary?",
        "answer": "Use for key in dictionary, dictionary.items(), dictionary.keys(), or dictionary.values() depending on what you need.",
        "category": "Dictionaries",
    },
    {
        "question": "What is a namespace?",
        "answer": "A namespace is a mapping from names to objects that helps prevent naming conflicts in Python programs.",
        "category": "Advanced",
    },
    {
        "question": "What is scope in Python?",
        "answer": "Scope determines where a name can be accessed. Python commonly follows the LEGB rule: Local, Enclosing, Global, Built-in.",
        "category": "Advanced",
    },
    {
        "question": "What is LEGB?",
        "answer": "LEGB stands for Local, Enclosing, Global, Built-in and describes the order Python uses when resolving names.",
        "category": "Advanced",
    },
    {
        "question": "What is garbage collection?",
        "answer": "Python manages memory automatically and includes garbage collection mechanisms for reclaiming certain objects that are no longer reachable.",
        "category": "Advanced",
    },
    {
        "question": "What is GIL?",
        "answer": "In standard CPython, the Global Interpreter Lock allows only one thread to execute Python bytecode at a time within a process.",
        "category": "Advanced",
    },
    {
        "question": "What is threading?",
        "answer": "Threading runs multiple threads within a process and is often useful for I/O-bound tasks in Python.",
        "category": "Advanced",
    },
    {
        "question": "What is multiprocessing?",
        "answer": "Multiprocessing uses separate processes and can run CPU-bound Python code in parallel across processes.",
        "category": "Advanced",
    },
    {
        "question": "What is async programming?",
        "answer": "Asynchronous programming allows cooperative concurrency using constructs such as async and await and is useful for many I/O-bound workloads.",
        "category": "Advanced",
    },
        {
        "question": "Is Python difficult to learn?",
        "answer": "Python is generally considered beginner-friendly because its syntax is readable and relatively simple. The difficulty depends on the concepts and applications being learned.",
        "category": "Basics",
    },
    {
        "question": "Is Python easy for beginners?",
        "answer": "Yes. Python is widely used by beginners because of its readable syntax, simple structure, and extensive learning resources.",
        "category": "Basics",
    },
    {
        "question": "How hard is Python to learn?",
        "answer": "Python is relatively easy to start with, although advanced topics such as decorators, generators, concurrency, and memory management require more experience.",
        "category": "Basics",
    },
    {
        "question": "Why is Python popular?",
        "answer": "Python is popular because it has readable syntax, a large standard library, a large package ecosystem, and applications across web development, automation, data science, and machine learning.",
        "category": "Basics",
    },
    {
        "question": "What can Python be used for?",
        "answer": "Python can be used for automation, web development, data analysis, machine learning, scientific computing, scripting, and many other tasks.",
        "category": "Basics",
    },
]


df = pd.DataFrame(knowledge_base)

output_path = DATA_DIR / "python_knowledge_base.csv"
df.to_csv(output_path, index=False)

print(f"Knowledge base created: {output_path}")
print(f"Total questions: {len(df)}")
print("\nCategories:")
print(df["category"].value_counts())