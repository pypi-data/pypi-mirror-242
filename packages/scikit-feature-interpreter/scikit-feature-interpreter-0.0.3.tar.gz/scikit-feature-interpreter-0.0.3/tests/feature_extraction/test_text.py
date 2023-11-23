from sklearn.feature_extraction.text import TfidfVectorizer

from skinterpret.feature_extraction.text import InterpretableTfidfVectorizer

CORPUS = [
    "This is the first document.",
    "This document is the second document.",
    "And this is the third one.",
    "Is this the first document?",
]


def test_can_create_from_fitted_vectorizer():
    vectorizer = TfidfVectorizer()
    vectorizer.fit(CORPUS)

    interpreter = InterpretableTfidfVectorizer(vectorizer)

    assert interpreter.vectorizer is vectorizer


def test_interpret():
    vectorizer = TfidfVectorizer()
    vectorizer.fit(CORPUS)

    interpreter = InterpretableTfidfVectorizer(vectorizer)
    actual = interpreter.interpret(CORPUS[0])

    expected = [
        ("first", 0.5802858236844359),
        ("document", 0.46979138557992045),
        ("is", 0.38408524091481483),
        ("the", 0.38408524091481483),
        ("this", 0.38408524091481483),
    ]
    assert actual == expected
