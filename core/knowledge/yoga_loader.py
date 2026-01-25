import csv
from typing import List
from core.knowledge.yoga_schema import YogaSutraRow
from core.knowledge.exceptions import KnowledgeValidationError

REQUIRED = {"topic","question","answer","chapter","sutra","citation"}

def load_yoga_csv(path: str) -> List[YogaSutraRow]:
    rows: List[YogaSutraRow] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise KnowledgeValidationError("Invalid Yoga CSV schema")

        for i, r in enumerate(reader, start=1):
            chapter = int(r["chapter"])
            sutra = int(r["sutra"])
            citation = r["citation"].strip()
            expected = f"Yoga Sutra {chapter}.{sutra}"

            if citation != expected:
                raise KnowledgeValidationError(
                    f"Row {i}: citation mismatch (expected '{expected}')"
                )
            if not (1 <= chapter <= 4 and sutra >= 1):
                raise KnowledgeValidationError(f"Row {i}: invalid chapter/sutra")

            row = YogaSutraRow(
                topic=r["topic"].strip(),
                question=r["question"].strip(),
                answer=r["answer"].strip(),
                chapter=chapter,
                sutra=sutra,
                citation=citation,
            )
            if not all([row.topic, row.question, row.answer, row.citation]):
                raise KnowledgeValidationError(f"Row {i}: empty fields")

            rows.append(row)

    if not rows:
        raise KnowledgeValidationError("Yoga CSV has no data")
    return rows
