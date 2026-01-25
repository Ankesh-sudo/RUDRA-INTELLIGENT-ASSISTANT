import csv
from typing import List
from core.knowledge.upanishad_schema import UpanishadRow
from core.knowledge.exceptions import KnowledgeValidationError

REQUIRED = {"topic","question","answer","text","verse","citation"}

def load_upanishad_csv(path: str) -> List[UpanishadRow]:
    rows: List[UpanishadRow] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise KnowledgeValidationError("Invalid Upanishad CSV schema")

        for i, r in enumerate(reader, start=1):
            text = r["text"].strip()
            verse = r["verse"].strip()
            citation = r["citation"].strip()
            expected = f"{text} {verse}"
            if citation != expected:
                raise KnowledgeValidationError(
                    f"Row {i}: citation mismatch (expected '{expected}')"
                )

            row = UpanishadRow(
                topic=r["topic"].strip(),
                question=r["question"].strip(),
                answer=r["answer"].strip(),
                text=text,
                verse=verse,
                citation=citation,
            )
            if not all([row.topic, row.question, row.answer, row.text, row.verse, row.citation]):
                raise KnowledgeValidationError(f"Row {i}: empty fields")

            rows.append(row)

    if not rows:
        raise KnowledgeValidationError("Upanishad CSV has no data")
    return rows
