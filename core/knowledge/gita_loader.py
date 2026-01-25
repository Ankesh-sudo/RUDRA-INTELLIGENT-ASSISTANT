import csv
from typing import List
from core.knowledge.gita_schema import GitaRow
from core.knowledge.exceptions import KnowledgeValidationError


REQUIRED_COLUMNS = {
    "topic", "question", "answer", "chapter", "verse", "citation"
}


def load_gita_csv(path: str) -> List[GitaRow]:
    rows: List[GitaRow] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
            raise KnowledgeValidationError("Invalid Gita CSV schema")

        for i, r in enumerate(reader, start=1):
            try:
                chapter = int(r["chapter"])
                verse = int(r["verse"])
                citation = r["citation"].strip()

                expected = f"Bhagavad Gita {chapter}.{verse}"
                if citation != expected:
                    raise KnowledgeValidationError(
                        f"Row {i}: citation mismatch (expected '{expected}')"
                    )

                if not (1 <= chapter <= 18 and verse >= 1):
                    raise KnowledgeValidationError(
                        f"Row {i}: invalid chapter/verse"
                    )

                row = GitaRow(
                    topic=r["topic"].strip(),
                    question=r["question"].strip(),
                    answer=r["answer"].strip(),
                    chapter=chapter,
                    verse=verse,
                    citation=citation,
                )

                if not all([row.topic, row.question, row.answer, row.citation]):
                    raise KnowledgeValidationError(f"Row {i}: empty fields")

                rows.append(row)

            except KnowledgeValidationError:
                raise
            except Exception as e:
                raise KnowledgeValidationError(f"Row {i} invalid: {e}")

    if not rows:
        raise KnowledgeValidationError("Gita CSV has no data")

    return rows
