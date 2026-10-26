from pathlib import Path
import json


# ================================================================
# PATHS
# ================================================================

BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_PATH = BASE_DIR / "output" / "evaluation_results.json"


# ================================================================
# MAIN
# ================================================================

def main():

    if not RESULTS_PATH.exists():
        print(
            f"Evaluation results not found:\n"
            f"{RESULTS_PATH}"
        )
        return

    with open(
        RESULTS_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    # ============================================================
    # IN-SCOPE FAILURES
    # ============================================================

    print()
    print("IN-SCOPE RETRIEVAL FAILURES")
    print("=" * 70)

    in_scope_results = data.get(
        "in_scope_results",
        []
    )

    failures = [
        result
        for result in in_scope_results
        if not result.get("correct", False)
    ]

    if not failures:

        print("No in-scope failures found.")

    else:

        for number, result in enumerate(
            failures,
            start=1
        ):

            print()
            print(f"{number}. User question : {result['question']}")
            print(
                f"   Expected        : "
                f"{result['expected']}"
            )
            print(
                f"   Matched         : "
                f"{result['matched']}"
            )
            print(
                f"   Category        : "
                f"{result['category']}"
            )
            print(
                f"   Confidence      : "
                f"{result['confidence']}"
            )
            print(
                f"   Similarity      : "
                f"{result['similarity']:.2%}"
            )
            print(
                f"   Top-3 success   : "
                f"{result['top3_correct']}"
            )

    # ============================================================
    # OUT-OF-DOMAIN RESULTS
    # ============================================================

    print()
    print()
    print("OUT-OF-DOMAIN QUESTIONS")
    print("=" * 70)

    out_results = data.get(
        "out_of_domain_results",
        []
    )

    for number, result in enumerate(
        out_results,
        start=1
    ):

        status = (
            "REJECTED"
            if result["rejected"]
            else "ACCEPTED"
        )

        print()
        print(
            f"{number}. {result['question']}"
        )
        print(
            f"   Status     : {status}"
        )
        print(
            f"   Matched    : {result['matched']}"
        )
        print(
            f"   Similarity : "
            f"{result['similarity']:.2%}"
        )

    # ============================================================
    # CONTEXT RESULTS
    # ============================================================

    print()
    print()
    print("CONVERSATION CONTEXT TESTS")
    print("=" * 70)

    context_results = data.get(
        "context_results",
        []
    )

    for number, test in enumerate(
        context_results,
        start=1
    ):

        status = (
            "PASS"
            if test["correct"]
            else "FAIL"
        )

        print()
        print(
            f"{number}. {test['name']} "
            f"→ {status}"
        )

        for step in test["conversation"]:

            step_status = (
                "PASS"
                if step["correct"]
                else "FAIL"
            )

            print(
                f"   [{step_status}] "
                f"{step['question']}"
            )

            print(
                f"       Expected: "
                f"{step['expected']}"
            )

            print(
                f"       Matched : "
                f"{step['matched']}"
            )

    # ============================================================
    # SUMMARY
    # ============================================================

    print()
    print()
    print("=" * 70)
    print("INSPECTION SUMMARY")
    print("=" * 70)

    print(
        f"In-scope failures : "
        f"{len(failures)}"
    )

    print(
        f"Out-of-domain     : "
        f"{sum(r['rejected'] for r in out_results)}/"
        f"{len(out_results)} rejected"
    )

    print(
        f"Context tests     : "
        f"{sum(r['correct'] for r in context_results)}/"
        f"{len(context_results)} passed"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()