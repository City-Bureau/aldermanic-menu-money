import csv
import re
import sys


def process_early():
    rows = []
    ward = ""
    dept = ""
    program = ""
    for idx, row in enumerate(csv.reader(sys.stdin)):
        paren_match = re.search(r"^\([\d\-]{1,3}\)$", row[0].strip())
        if (
            row[0].strip() == ""
            or paren_match
            or all(c.strip() == "" for c in row)
            or any(any(w in c for w in ["Page ", "Menu", "Full Address"]) for c in row)
        ):
            continue

        dept_match = re.search(r"[A-Z]{2,6}\s*:\s*[A-Z]{2,6}", row[0])
        if dept_match:
            dept = dept_match.group()
        elif row[0].startswith("Program"):
            program = row[0].split(":")[-1].strip()
        elif "Ward" in row[0]:
            ward = row[0].split(":")[-1].strip()
        elif all(c.strip() == "" for c in row[1:]):
            # Is address, append to last address row
            rows[-1]["location"] += " " + row[0].strip()
        else:
            rows.append(
                {
                    "ward": ward,
                    "dept": dept,
                    "program": program,
                    "location": row[0],
                    "desc": row[1],
                    "blocks": row[2],
                    "unit_count": row[3],
                    "est_cost": row[4],
                }
            )
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "ward",
            "dept",
            "program",
            "location",
            "desc",
            "blocks",
            "unit_count",
            "est_cost",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)


def process_recent():
    rows = []
    ward = ""
    for idx, row in enumerate(csv.reader(sys.stdin)):
        # TODO: Ignore totals
        if all(c.strip() == "" for c in row) or "MenuPackage" in row:
            continue
        if row[0].startswith("Ward:"):
            ward = row[0].split(":")[-1].strip()
        elif len(rows) > 0 and rows[-1]["est_cost"] == "":
            for idx, field in enumerate(["desc", "location", "est_cost"]):
                rows[-1][field] = " ".join([rows[-1][field], row[idx]]).strip()
        else:
            rows.append(
                {
                    "ward": ward,
                    "desc": row[0].strip(),
                    "location": row[1].strip(),
                    "est_cost": row[2].strip(),
                }
            )
    writer = csv.DictWriter(
        sys.stdout, fieldnames=["ward", "desc", "location", "est_cost"]
    )
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    if sys.argv[1] < "2016":
        process_early()
    else:
        process_recent()
