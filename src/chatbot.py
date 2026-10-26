from pathlib import Path
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ================================================================
# CONFIGURATION
# ================================================================

BASE_DIR = Path(__file__).resolve().parents[1]
KB_PATH = BASE_DIR / "data" / "python_knowledge_base.csv"

HIGH_CONFIDENCE = 0.65
MEDIUM_CONFIDENCE = 0.45
OUT_OF_DOMAIN_THRESHOLD = 0.50


# ================================================================
# PYTHON DOMAIN KEYWORDS
# ================================================================

PYTHON_KEYWORDS = {
    "python", "list", "lists", "tuple", "tuples",
    "dictionary", "dictionaries", "dict", "dicts",
    "set", "sets", "string", "strings", "str",
    "integer", "int", "float", "boolean", "bool",
    "variable", "variables", "function", "functions",
    "method", "methods", "class", "classes", "object",
    "objects", "inheritance", "polymorphism",
    "encapsulation", "constructor", "decorator",
    "generator", "generators", "iterator", "iterators",
    "iterable", "iterables", "yield", "lambda",
    "exception", "exceptions", "error", "errors",
    "try", "except", "finally", "loop", "loops",
    "for", "while", "if", "else", "elif",
    "condition", "operator", "operators", "module",
    "modules", "package", "packages", "import",
    "pip", "library", "libraries", "virtual",
    "environment", "environments", "venv", "file",
    "files", "csv", "json", "pickle", "comprehension",
    "comprehensions", "slicing", "slice", "index",
    "indexes", "recursion", "scope", "global",
    "local", "async", "await", "thread", "threads",
    "process", "processes", "regex", "regular",
    "expression", "numpy", "pandas", "matplotlib",
    "debug", "debugging",
}


# ================================================================
# FOLLOW-UP DETECTION
# ================================================================

FOLLOW_UP_WORDS = {
    "it",
    "this",
    "that",
    "one",
    "they",
    "them",
    "these",
    "those",
    "same",
    "above",
    "previous",
}


# ================================================================
# TOPIC ALIASES
# ================================================================

TOPIC_ALIASES = {
    "list": {
        "list",
        "lists",
        "array",
        "arrays",
    },

    "tuple": {
        "tuple",
        "tuples",
    },

    "dictionary": {
        "dictionary",
        "dictionaries",
        "dict",
        "dicts",
        "key value",
        "key-value",
    },

    "set": {
        "set",
        "sets",
        "unique collection",
    },

    "string": {
        "string",
        "strings",
        "str",
        "text",
    },

    "function": {
        "function",
        "functions",
        "def",
        "method",
        "methods",
    },

    "class": {
        "class",
        "classes",
        "object oriented",
        "oop",
    },

    "inheritance": {
        "inheritance",
        "parent class",
        "child class",
        "base class",
        "derived class",
    },

    "generator": {
        "generator",
        "generators",
        "yield",
    },

    "iterator": {
        "iterator",
        "iterators",
        "iterable",
        "iterables",
    },

    "lambda": {
        "lambda",
        "anonymous function",
    },

    "exception": {
        "exception",
        "exceptions",
        "error handling",
        "try except",
        "try-except",
    },

    "loop": {
        "loop",
        "loops",
        "for loop",
        "while loop",
    },

    "virtual environment": {
        "virtual environment",
        "virtual environments",
        "venv",
        "environment",
    },

    "file": {
        "file",
        "files",
        "file handling",
        "read file",
        "write file",
    },
}


# ================================================================
# INTENT PATTERNS
# ================================================================

INTENT_PATTERNS = {
    "definition": [
        r"\bwhat is\b",
        r"\bwhat are\b",
        r"\bwhat does .* mean\b",
        r"\bmeaning of\b",
        r"\bdefine\b",
        r"\bdefinition of\b",
        r"\bexplain\b",
        r"\btell me about\b",
    ],

    "creation": [
        r"\bhow do i create\b",
        r"\bhow can i create\b",
        r"\bhow do you create\b",
        r"\bhow to create\b",
        r"\bcreate a\b",
        r"\bcreate an\b",
        r"\bmake a\b",
        r"\bmake an\b",
    ],

    "copying": [
        r"\bhow do i copy\b",
        r"\bhow can i copy\b",
        r"\bhow to copy\b",
        r"\bcopy a\b",
        r"\bcopy an\b",
        r"\bshallow copy\b",
        r"\bdeep copy\b",
    ],

    "sorting": [
        r"\bhow do i sort\b",
        r"\bhow can i sort\b",
        r"\bhow to sort\b",
        r"\bsort a\b",
        r"\bsort an\b",
    ],

    "conversion": [
        r"\bhow do i convert\b",
        r"\bhow can i convert\b",
        r"\bhow to convert\b",
        r"\bconvert .* to\b",
        r"\bconvert .* into\b",
    ],

    "comparison": [
        r"\bdifference between\b",
        r"\bwhat is the difference\b",
        r"\bcompare\b",
        r"\bvs\b",
        r"\bversus\b",
    ],

    "usage": [
        r"\bhow do i use\b",
        r"\bhow can i use\b",
        r"\bhow to use\b",
        r"\bwhen should i use\b",
        r"\bwhy use\b",
    ],

    "purpose": [
        r"\bwhat is .* used for\b",
        r"\bwhat are .* used for\b",
        r"\bwhy is .* used\b",
        r"\bwhy do we use\b",
        r"\bpurpose of\b",
    ],

    "behavior": [
        r"\bwhat does .* do\b",
        r"\bhow does .* work\b",
        r"\bhow do .* work\b",
        r"\bwhat happens when\b",
    ],

    "syntax": [
        r"\bsyntax\b",
        r"\bhow do i write\b",
        r"\bhow to write\b",
        r"\bsyntax for\b",
    ],

    "advantages": [
        r"\badvantages\b",
        r"\bbenefits\b",
        r"\bwhy is .* popular\b",
        r"\bwhy use\b",
    ],

    "difficulty": [
        r"\bis .* difficult\b",
        r"\bis .* easy\b",
        r"\bhow hard\b",
        r"\bhow difficult\b",
        r"\bhard to learn\b",
        r"\beasy to learn\b",
    ],
}


# ================================================================
# TEXT PREPROCESSING
# ================================================================

def preprocess_text(text):
    text = str(text).lower().strip()

    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text


# ================================================================
# DOMAIN DETECTION
# ================================================================

def contains_python_keyword(text):
    normalized = preprocess_text(text)
    words = set(normalized.split())

    if words & PYTHON_KEYWORDS:
        return True

    for keyword in PYTHON_KEYWORDS:
        if " " in keyword and keyword in normalized:
            return True

    return False


# ================================================================
# FOLLOW-UP DETECTION
# ================================================================

def is_follow_up(text):
    normalized = preprocess_text(text)
    words = set(normalized.split())

    if words & FOLLOW_UP_WORDS:
        return True

    follow_up_patterns = [
        r"^how do i create (it|this|that|one)$",
        r"^how can i create (it|this|that|one)$",
        r"^how do i use (it|this|that|one)$",
        r"^how can i use (it|this|that|one)$",
        r"^how does (it|this|that) work$",
        r"^what does (it|this|that) do$",
        r"^how do i do (it|this|that)$",
        r"^what about (it|this|that)$",
    ]

    return any(
        re.search(pattern, normalized)
        for pattern in follow_up_patterns
    )


# ================================================================
# TOPIC DETECTION
# ================================================================

def detect_topic(text):
    normalized = preprocess_text(text)

    aliases = []

    for topic, values in TOPIC_ALIASES.items():
        for value in values:
            aliases.append((value, topic))

    aliases.sort(
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, topic in aliases:
        if alias in normalized:
            return topic

    return None


# ================================================================
# INTENT DETECTION
# ================================================================

def detect_intent(text):
    normalized = preprocess_text(text)

    for intent, patterns in INTENT_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, normalized):
                return intent

    return "general"


# ================================================================
# QUESTION SPECIFICITY
# ================================================================

def get_specificity_score(user_question, candidate_question):
    """
    Measure how directly the important words in the candidate
    question occur in the user's question.

    This is used only as a tie-breaker. TF-IDF similarity
    remains the primary retrieval signal.
    """

    user_text = preprocess_text(user_question)
    candidate_text = preprocess_text(candidate_question)

    user_words = set(user_text.split())
    candidate_words = set(candidate_text.split())

    # Remove generic question words.
    generic_words = {
        "what",
        "is",
        "are",
        "a",
        "an",
        "the",
        "how",
        "do",
        "does",
        "can",
        "i",
        "to",
        "in",
        "of",
        "for",
        "on",
        "and",
        "or",
        "it",
        "one",
    }

    meaningful_candidate_words = (
        candidate_words - generic_words
    )

    if not meaningful_candidate_words:
        return 0.0

    overlap = (
        user_words & meaningful_candidate_words
    )

    return len(overlap) / len(meaningful_candidate_words)


# ================================================================
# CONFIDENCE
# ================================================================

def get_confidence_level(similarity):
    if similarity >= HIGH_CONFIDENCE:
        return "High"

    if similarity >= MEDIUM_CONFIDENCE:
        return "Medium"

    return "Low"


# ================================================================
# CHATBOT
# ================================================================

class PythonChatbot:

    def __init__(self, knowledge_base_path=KB_PATH):

        self.knowledge_base_path = Path(
            knowledge_base_path
        )

        if not self.knowledge_base_path.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: "
                f"{self.knowledge_base_path}"
            )

        self.data = pd.read_csv(
            self.knowledge_base_path
        )

        required_columns = {
            "question",
            "answer",
            "category",
        }

        if not required_columns.issubset(
            self.data.columns
        ):
            raise ValueError(
                f"Knowledge base must contain: "
                f"{required_columns}"
            )

        self.data["question"] = (
            self.data["question"]
            .fillna("")
            .astype(str)
        )

        self.data["answer"] = (
            self.data["answer"]
            .fillna("")
            .astype(str)
        )

        self.data["category"] = (
            self.data["category"]
            .fillna("General")
            .astype(str)
        )

        self.questions = [
            preprocess_text(question)
            for question in self.data["question"]
        ]

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )

        self.question_vectors = (
            self.vectorizer.fit_transform(
                self.questions
            )
        )

        # Conversation memory.
        self.last_question = None
        self.last_answer = None
        self.last_category = None
        self.last_topic = None
        self.last_intent = None

    # ============================================================
    # MATCHING
    # ============================================================

    def find_matches(
        self,
        search_query,
        original_question=None,
        top_k=3,
        preferred_topic=None,
        preferred_intent=None,
    ):

        normalized_query = preprocess_text(
            search_query
        )

        query_vector = self.vectorizer.transform(
            [normalized_query]
        )

        similarities = cosine_similarity(
            query_vector,
            self.question_vectors
        )[0]

        candidates = []

        for index, similarity in enumerate(
            similarities
        ):

            candidate_question = (
                self.data.iloc[index]["question"]
            )

            candidate = {
                "index": index,
                "similarity": float(similarity),
                "question": candidate_question,
                "answer": self.data.iloc[index]["answer"],
                "category": self.data.iloc[index]["category"],
                "topic": detect_topic(
                    candidate_question
                ),
                "intent": detect_intent(
                    candidate_question
                ),
            }

            # Topic match.
            candidate["topic_match"] = (
                preferred_topic is not None
                and candidate["topic"] == preferred_topic
            )

            # Intent match.
            candidate["intent_match"] = (
                preferred_intent is not None
                and candidate["intent"] == preferred_intent
            )

            # Specificity is calculated against the original
            # user question, not the expanded context query.
            if original_question:
                candidate["specificity"] = (
                    get_specificity_score(
                        original_question,
                        candidate_question,
                    )
                )
            else:
                candidate["specificity"] = 0.0

            candidates.append(candidate)

        # --------------------------------------------------------
        # Ranking
        #
        # TF-IDF remains dominant.
        #
        # Topic + intent help resolve close candidates.
        #
        # Specificity breaks very close ties such as:
        #
        # What is a dictionary?
        # What is dictionary get()?
        # --------------------------------------------------------

        def ranking_score(candidate):

            score = candidate["similarity"]

            # Topic preference.
            if candidate["topic_match"]:
                score += 0.06

            # Intent preference.
            if candidate["intent_match"]:
                score += 0.06

            # Specificity is intentionally small.
            score += (
                candidate["specificity"] * 0.04
            )

            return score

        candidates.sort(
            key=ranking_score,
            reverse=True
        )

        return candidates[:top_k]

    # ============================================================
    # SEARCH QUERY
    # ============================================================

    def build_search_query(self, user_question):

        if (
            is_follow_up(user_question)
            and self.last_question
        ):
            return (
                f"{self.last_question} "
                f"{user_question}"
            )

        return user_question

    # ============================================================
    # RESPONSE
    # ============================================================

    def get_response(self, user_question):

        user_question = str(
            user_question
        ).strip()

        if not user_question:

            return {
                "answer": (
                    "Please enter a Python "
                    "programming question."
                ),
                "category": "General",
                "confidence": "Low",
                "similarity": 0.0,
                "matches": [],
            }

        search_query = self.build_search_query(
            user_question
        )

        user_topic = detect_topic(
            user_question
        )

        user_intent = detect_intent(
            user_question
        )

        # Follow-up questions inherit previous context.
        if is_follow_up(user_question):

            if user_topic is None:
                user_topic = self.last_topic

            if user_intent == "general":
                user_intent = self.last_intent

        matches = self.find_matches(
            search_query,
            original_question=user_question,
            top_k=3,
            preferred_topic=user_topic,
            preferred_intent=user_intent,
        )

        if not matches:

            return {
                "answer": "I couldn't find an answer.",
                "category": "General",
                "confidence": "Low",
                "similarity": 0.0,
                "matches": [],
            }

        best = matches[0]

        similarity = best["similarity"]

        # --------------------------------------------------------
        # OUT-OF-DOMAIN REJECTION
        # --------------------------------------------------------

        has_python_keyword = (
            contains_python_keyword(
                user_question
            )
        )

        if has_python_keyword:
            acceptance_threshold = (
                MEDIUM_CONFIDENCE
            )
        else:
            acceptance_threshold = (
                OUT_OF_DOMAIN_THRESHOLD
            )

        # Follow-ups can use inherited context.
        if (
            is_follow_up(user_question)
            and self.last_question
        ):
            acceptance_threshold = (
                MEDIUM_CONFIDENCE
            )

        if similarity < acceptance_threshold:

            return {
                "answer": (
                    "I'm sorry, I couldn't find a "
                    "sufficiently relevant answer in "
                    "my Python knowledge base. "
                    "Please ask a more specific "
                    "Python programming question."
                ),
                "category": "Out of Domain",
                "confidence": "Low",
                "similarity": similarity,
                "matches": matches,
            }

        # --------------------------------------------------------
        # SAVE CONTEXT
        # --------------------------------------------------------

        self.last_question = user_question
        self.last_answer = best["answer"]
        self.last_category = best["category"]

        self.last_topic = (
            user_topic
            or best["topic"]
        )

        self.last_intent = (
            user_intent
            or best["intent"]
        )

        return {
            "answer": best["answer"],
            "category": best["category"],
            "confidence": get_confidence_level(
                similarity
            ),
            "similarity": similarity,
            "matches": matches,
        }


# ================================================================
# CLI DISPLAY
# ================================================================

def print_response(result):

    print()
    print(f"Bot: {result['answer']}")

    print()
    print(
        f"[Category   : {result['category']}]"
    )

    print(
        f"[Confidence : {result['confidence']}]"
    )

    print(
        f"[Similarity : "
        f"{result['similarity']:.2%}]"
    )

    if result["matches"]:

        print()
        print("Related questions:")

        for position, match in enumerate(
            result["matches"],
            start=1
        ):

            print(
                f"{position}. "
                f"{match['question']} "
                f"({match['similarity']:.2%})"
            )

    print()


# ================================================================
# MAIN
# ================================================================

def main():

    print("=" * 65)
    print(
        "          PERSONAL PYTHON LEARNING ASSISTANT"
    )
    print("=" * 65)
    print(
        "Ask questions about Python programming."
    )
    print(
        "The chatbot retrieves answers from a "
        "predefined knowledge base."
    )
    print(
        "Type 'exit' or 'quit' to stop."
    )
    print("=" * 65)

    chatbot = PythonChatbot()

    while True:

        try:
            user_question = input(
                "\nYou: "
            ).strip()

        except (
            KeyboardInterrupt,
            EOFError,
        ):

            print(
                "\n\nChatbot: Goodbye! "
                "Keep coding in Python."
            )
            break

        if user_question.lower() in {
            "exit",
            "quit",
        }:

            print(
                "\nChatbot: Goodbye! "
                "Keep coding in Python."
            )
            break

        result = chatbot.get_response(
            user_question
        )

        print_response(result)


if __name__ == "__main__":
    main()