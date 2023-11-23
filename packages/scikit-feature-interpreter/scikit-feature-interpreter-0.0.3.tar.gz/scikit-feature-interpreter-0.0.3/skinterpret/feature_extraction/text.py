from __future__ import annotations

from collections.abc import Mapping
from typing import Tuple

import numpy as np
import numpy.typing as npt
from sklearn.feature_extraction.text import TfidfVectorizer

TOKEN = str
TFIDF = float
TOKEN_TFIDF_PAIR = Tuple[TOKEN, TFIDF]


class TfidfInterpreter:
    """
    >>> interpreter = TfidfInterpreter({0: "a", 1: "b", 2: "c", 3: "d"})
    >>> for item in interpreter.interpret(np.array([0.5, 0.8, 0.0, 0.3])):
    ...     print(item)
    ('b', 0.8)
    ('a', 0.5)
    ('d', 0.3)
    """

    def __init__(self, id_to_term: Mapping[int, str]) -> None:
        self.id_to_term = id_to_term

    def interpret(
        self, tfidf: npt.NDArray[np.float64]
    ) -> list[TOKEN_TFIDF_PAIR]:
        assert len(tfidf) == len(self.id_to_term)

        nonzero_index = np.nonzero(tfidf)[0]
        pairs = [(self.id_to_term[i], tfidf[i]) for i in nonzero_index]
        return sorted(pairs, key=lambda pair: (-pair[1], pair[0]))


class InterpretableTfidfVectorizer:
    """
    >>> corpus = [
    ...     "This is the first document.",
    ...     "This document is the second document.",
    ...     "And this is the third one.",
    ...     "Is this the first document?",
    ... ]
    >>> vectorizer = TfidfVectorizer().fit(corpus)
    >>> interpreter = InterpretableTfidfVectorizer(vectorizer)
    >>> tfidf = interpreter.interpret(corpus[0])
    >>> for item in tfidf:
    ...     print(item[0], item[1])
    first 0.5802858236844359
    document 0.46979138557992045
    is 0.38408524091481483
    the 0.38408524091481483
    this 0.38408524091481483
    """

    def __init__(self, vectorizer: TfidfVectorizer) -> None:
        self.vectorizer = vectorizer

    def interpret(self, document: str) -> list[TOKEN_TFIDF_PAIR]:
        interpreter = TfidfInterpreter(
            {id: term for term, id in self.vectorizer.vocabulary_.items()}
        )
        tfidf_vector = self.vectorizer.transform([document])[0]
        tfidf_array = tfidf_vector.toarray()[0]
        return interpreter.interpret(tfidf_array)
