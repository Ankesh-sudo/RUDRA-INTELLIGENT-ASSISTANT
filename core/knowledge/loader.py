import csv
from typing import List
from core.knowledge.schema import DharmaRow
from core.knowledge.exceptions import KnowledgeValidationError


REQUIRED_COLUMNS = {"topic", "question", "answer", "citation"}


def load_dharma_csv(path: str) -> List[DharmaRow]:
    rows: List[DharmaRow] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
            raise KnowledgeValidationError("Invalid CSV schema")

        for i, r in enumerate(reader, start=1):
            try:
                row = DharmaRow(
                    topic=r["topic"].strip(),
                    question=r["question"].strip(),
                    answer=r["answer"].strip(),
                    citation=r["citation"].strip(),
                )
            except Exception as e:
                raise KnowledgeValidationError(f"Row {i} invalid: {e}")

            if not all([row.topic, row.question, row.answer, row.citation]):
                raise KnowledgeValidationError(f"Row {i} has empty fields")

            rows.append(row)

    if not rows:
        raise KnowledgeValidationError("CSV has no data")

    return rows
