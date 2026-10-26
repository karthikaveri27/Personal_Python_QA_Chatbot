from pathlib import Path
import json

import matplotlib.pyplot as plt

from chatbot import PythonChatbot


# ================================================================
# PATHS
# ================================================================

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ================================================================
# TEST DATA
# ================================================================

# Each tuple contains:
# (question, expected knowledge-base question)

IN_SCOPE_TESTS = [
    # ------------------------------------------------------------
    # Python basics
    # ------------------------------------------------------------
    ("What is Python?", "What is Python?"),
    ("Why is Python popular?", "Why is Python popular?"),
    ("What can Python be used for?", "What can Python be used for?"),
    ("Is Python difficult to learn?", "Is Python difficult to learn?"),

    # ------------------------------------------------------------
    # Lists
    # ------------------------------------------------------------
    ("What is a list?", "What is a list?"),
    ("How do I create a list?", "How do I create a list?"),
    ("How do I copy a list?", "How do I copy a list?"),
    ("How do I sort a list?", "How do I sort a list?"),
    ("What is a list comprehension?", "What is a list comprehension?"),

    # ------------------------------------------------------------
    # Tuples
    # ------------------------------------------------------------
    ("What is a tuple?", "What is a tuple?"),
    ("How do I create a tuple?", "How do I create a tuple?"),

    # ------------------------------------------------------------
    # Dictionaries
    # ------------------------------------------------------------
    ("What is a dictionary?", "What is a dictionary?"),
    ("How do I create a dictionary?", "How do I create a dictionary?"),
    ("What is dictionary get()?", "What is dictionary get()?"),

    # ------------------------------------------------------------
    # Sets
    # ------------------------------------------------------------
    ("What is a set?", "What is a set?"),
    ("How do I create a set?", "How do I create a set?"),

    # ------------------------------------------------------------
    # Strings
    # ------------------------------------------------------------
    ("What is a string?", "What is a string?"),
    ("How do I reverse a string?", "How do I reverse a string?"),

    # ------------------------------------------------------------
    # Functions
    # ------------------------------------------------------------
    ("What is a function?", "What is a function?"),
    ("How do I define a function?", "How do I define a function?"),
    ("What are function arguments?", "What are function arguments?"),

    # ------------------------------------------------------------
    # OOP
    # ------------------------------------------------------------
    ("What is a class?", "What is a class?"),
    ("What is inheritance?", "What is inheritance?"),

    # ------------------------------------------------------------
    # Generators / iterators
    # ------------------------------------------------------------
    ("What is a generator?", "What is a generator?"),
    ("What is an iterator?", "What is an iterator?"),
    ("What does yield do?", "What does yield do?"),

    # ------------------------------------------------------------
    # Lambda
    # ------------------------------------------------------------
    ("What is a lambda function?", "What is a lambda function?"),

    # ------------------------------------------------------------
    # Exceptions
    # ------------------------------------------------------------
    ("What is an exception?", "What is an exception?"),
    ("How do I handle exceptions?", "How do I handle exceptions?"),

    # ------------------------------------------------------------
    # Loops
    # ------------------------------------------------------------
    ("What is a for loop?", "What is a for loop?"),
    ("What is a while loop?", "What is a while loop?"),

    # ------------------------------------------------------------
    # Built-ins
    # ------------------------------------------------------------
    ("What does len() do?", "What does len() do?"),
    ("What does range() do?", "What does range() do?"),

    # ------------------------------------------------------------
    # File handling
    # ------------------------------------------------------------
    ("How do I open a file?", "How do I open a file?"),

    # ------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------
    ("What is a virtual environment?", "What is a virtual environment?"),

    # ------------------------------------------------------------
    # Type conversion
    # ------------------------------------------------------------
    ("How do I convert a string to an integer?",
     "How do I convert a string to an integer?"),

    # ------------------------------------------------------------
    # Comprehensions
    # ------------------------------------------------------------
    ("What is a dictionary comprehension?",
     "What is a dictionary comprehension?"),

    # ------------------------------------------------------------
    # Advanced
    # ------------------------------------------------------------
    ("What is recursion?", "What is recursion?"),
    ("What is variable scope?", "What is variable scope?"),
]


# Questions that intentionally depend on previous conversation context.
#
# Each sequence is evaluated independently using a fresh chatbot.
CONTEXT_TESTS = [
    {
        "name": "List creation follow-up",
        "conversation": [
            ("What is a list?", "What is a list?"),
            ("How do I create one?", "How do I create a list?"),
        ],
    },
    {
        "name": "Tuple creation follow-up",
        "conversation": [
            ("What is a tuple?", "What is a tuple?"),
            ("How do I create one?", "How do I create a tuple?"),
        ],
    },
    {
        "name": "Dictionary creation follow-up",
        "conversation": [
            ("What is a dictionary?", "What is a dictionary?"),
            ("How do I create one?", "How do I create a dictionary?"),
        ],
    },
    {
        "name": "Set creation follow-up",
        "conversation": [
            ("What is a set?", "What is a set?"),
            ("How do I create one?", "How do I create a set?"),
        ],
    },
    {
        "name": "Generator follow-up",
        "conversation": [
            ("What is a generator?", "What is a generator?"),
            ("What does it do?", "What is a generator?"),
        ],
    },
]


OUT_OF_DOMAIN_TESTS = [
    "What is the capital of France?",
    "Who is the president of the United States?",
    "What is the weather today?",
    "How do I cook pasta?",
    "Who won the cricket match?",
    "What is the best phone to buy?",
    "Tell me a joke.",
    "What is machine learning?",
    "How do I learn guitar?",
    "What is the population of India?",
    "How do I edit a photo?",
    "What is the latest movie?",
]


# ================================================================
# HELPERS
# ================================================================

def normalize(text):
    return " ".join(
        str(text).lower().strip().split()
    )


def calculate_metrics(results):
    total = len(results)

    correct = sum(
        result["correct"]
        for result in results
    )

    if total:
        accuracy = correct / total
    else:
        accuracy = 0.0

    similarities = [
        result["similarity"]
        for result in results
        if result["accepted"]
    ]

    if similarities:
        average_similarity = (
            sum(similarities) / len(similarities)
        )
    else:
        average_similarity = 0.0

    top3_correct = sum(
        result["top3_correct"]
        for result in results
    )

    top3_accuracy = (
        top3_correct / total
        if total
        else 0.0
    )

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "top3_correct": top3_correct,
        "top3_accuracy": top3_accuracy,
        "average_similarity": average_similarity,
    }


# ================================================================
# IN-SCOPE EVALUATION
# ================================================================

def evaluate_in_scope(chatbot):

    results = []

    for question, expected_question in IN_SCOPE_TESTS:

        response = chatbot.get_response(question)

        matches = response["matches"]

        matched_question = (
            matches[0]["question"]
            if matches
            else None
        )

        top3_questions = [
            match["question"]
            for match in matches
        ]

        correct = (
            normalize(matched_question)
            == normalize(expected_question)
        )

        top3_correct = any(
            normalize(question_name)
            == normalize(expected_question)
            for question_name in top3_questions
        )

        results.append({
            "question": question,
            "expected": expected_question,
            "matched": matched_question,
            "category": response["category"],
            "confidence": response["confidence"],
            "similarity": response["similarity"],
            "accepted": response["category"] != "Out of Domain",
            "correct": correct,
            "top3_correct": top3_correct,
        })

    return results


# ================================================================
# OUT-OF-DOMAIN EVALUATION
# ================================================================

def evaluate_out_of_domain(chatbot):

    results = []

    for question in OUT_OF_DOMAIN_TESTS:

        response = chatbot.get_response(question)

        rejected = (
            response["category"]
            == "Out of Domain"
        )

        matched_question = (
            response["matches"][0]["question"]
            if response["matches"]
            else None
        )

        results.append({
            "question": question,
            "rejected": rejected,
            "matched": matched_question,
            "similarity": response["similarity"],
            "confidence": response["confidence"],
            "category": response["category"],
        })

    return results


# ================================================================
# CONTEXT EVALUATION
# ================================================================

def evaluate_context():

    results = []

    for test in CONTEXT_TESTS:

        chatbot = PythonChatbot()

        conversation_results = []

        for question, expected_question in test["conversation"]:

            response = chatbot.get_response(
                question
            )

            matched_question = (
                response["matches"][0]["question"]
                if response["matches"]
                else None
            )

            correct = (
                normalize(matched_question)
                == normalize(expected_question)
            )

            conversation_results.append({
                "question": question,
                "expected": expected_question,
                "matched": matched_question,
                "similarity": response["similarity"],
                "confidence": response["confidence"],
                "correct": correct,
            })

        all_correct = all(
            item["correct"]
            for item in conversation_results
        )

        results.append({
            "name": test["name"],
            "conversation": conversation_results,
            "correct": all_correct,
        })

    return results


# ================================================================
# CONFIDENCE ANALYSIS
# ================================================================

def confidence_distribution(results):

    distribution = {
        "High": 0,
        "Medium": 0,
        "Low": 0,
    }

    for result in results:

        confidence = result["confidence"]

        if confidence in distribution:
            distribution[confidence] += 1

    return distribution


# ================================================================
# PLOT
# ================================================================

def create_plot(metrics):

    labels = [
        "In-scope\nTop-1",
        "In-scope\nTop-3",
        "Out-of-domain\nRejection",
        "Overall",
    ]

    values = [
        metrics["in_scope_accuracy"],
        metrics["in_scope_top3_accuracy"],
        metrics["out_of_domain_rejection"],
        metrics["overall_accuracy"],
    ]

    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        labels,
        [value * 100 for value in values],
    )

    plt.ylabel("Percentage")
    plt.title(
        "Personal Python QA Chatbot - Evaluation"
    )

    plt.ylim(0, 105)

    for bar, value in zip(
        bars,
        values,
    ):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{value:.1%}",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()

    plot_path = OUTPUT_DIR / "evaluation_plot.png"

    plt.savefig(
        plot_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()

    return plot_path


# ================================================================
# MAIN
# ================================================================

def main():

    print("=" * 65)
    print(
        "       PERSONAL PYTHON QA CHATBOT EVALUATION"
    )
    print("=" * 65)

    # ------------------------------------------------------------
    # In-scope
    # ------------------------------------------------------------

    print("\n[1/4] Evaluating Python questions...")

    chatbot = PythonChatbot()

    in_scope_results = evaluate_in_scope(
        chatbot
    )

    in_scope_metrics = calculate_metrics(
        in_scope_results
    )

    # ------------------------------------------------------------
    # Out-of-domain
    # ------------------------------------------------------------

    print(
        "[2/4] Evaluating out-of-domain rejection..."
    )

    chatbot = PythonChatbot()

    out_results = evaluate_out_of_domain(
        chatbot
    )

    out_rejected = sum(
        result["rejected"]
        for result in out_results
    )

    out_total = len(out_results)

    out_rejection_rate = (
        out_rejected / out_total
        if out_total
        else 0.0
    )

    # ------------------------------------------------------------
    # Context
    # ------------------------------------------------------------

    print(
        "[3/4] Evaluating conversation context..."
    )

    context_results = evaluate_context()

    context_correct = sum(
        result["correct"]
        for result in context_results
    )

    context_total = len(context_results)

    context_accuracy = (
        context_correct / context_total
        if context_total
        else 0.0
    )

    # ------------------------------------------------------------
    # Overall
    # ------------------------------------------------------------

    total_tests = (
        len(IN_SCOPE_TESTS)
        + len(OUT_OF_DOMAIN_TESTS)
    )

    overall_correct = (
        in_scope_metrics["correct"]
        + out_rejected
    )

    overall_accuracy = (
        overall_correct / total_tests
        if total_tests
        else 0.0
    )

    confidence = confidence_distribution(
        in_scope_results
    )

    metrics = {
        "in_scope_total": in_scope_metrics["total"],
        "in_scope_correct": in_scope_metrics["correct"],
        "in_scope_accuracy": in_scope_metrics["accuracy"],
        "in_scope_top3_correct": in_scope_metrics["top3_correct"],
        "in_scope_top3_accuracy": in_scope_metrics[
            "top3_accuracy"
        ],
        "average_in_scope_similarity": in_scope_metrics[
            "average_similarity"
        ],
        "out_of_domain_total": out_total,
        "out_of_domain_rejected": out_rejected,
        "out_of_domain_rejection": out_rejection_rate,
        "context_total": context_total,
        "context_correct": context_correct,
        "context_accuracy": context_accuracy,
        "overall_total": total_tests,
        "overall_correct": overall_correct,
        "overall_accuracy": overall_accuracy,
        "confidence_distribution": confidence,
    }

    # ------------------------------------------------------------
    # Save JSON
    # ------------------------------------------------------------

    evaluation = {
        "metrics": metrics,
        "in_scope_results": in_scope_results,
        "out_of_domain_results": out_results,
        "context_results": context_results,
    }

    results_path = (
        OUTPUT_DIR / "evaluation_results.json"
    )

    with open(
        results_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            evaluation,
            file,
            indent=2,
            ensure_ascii=False,
        )

    # ------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------

    plot_path = create_plot(metrics)

    # ------------------------------------------------------------
    # Console report
    # ------------------------------------------------------------

    print("\n" + "=" * 65)
    print("                    RESULTS")
    print("=" * 65)

    print(
        f"\nIn-scope questions       : "
        f"{metrics['in_scope_correct']}/"
        f"{metrics['in_scope_total']}"
    )

    print(
        f"In-scope Top-1 accuracy : "
        f"{metrics['in_scope_accuracy']:.2%}"
    )

    print(
        f"In-scope Top-3 accuracy : "
        f"{metrics['in_scope_top3_accuracy']:.2%}"
    )

    print(
        f"Average similarity      : "
        f"{metrics['average_in_scope_similarity']:.2%}"
    )

    print(
        f"\nOut-of-domain rejected  : "
        f"{metrics['out_of_domain_rejected']}/"
        f"{metrics['out_of_domain_total']}"
    )

    print(
        f"Out-of-domain rejection : "
        f"{metrics['out_of_domain_rejection']:.2%}"
    )

    print(
        f"\nContext accuracy        : "
        f"{metrics['context_accuracy']:.2%}"
    )

    print(
        f"\nOverall accuracy        : "
        f"{metrics['overall_accuracy']:.2%}"
    )

    print("\nConfidence distribution:")

    for level, count in confidence.items():

        print(
            f"  {level:7s}: {count}"
        )

    print("\nFiles created:")

    print(
        f"  JSON : {results_path}"
    )

    print(
        f"  Plot : {plot_path}"
    )

    print("=" * 65)


if __name__ == "__main__":
    main()