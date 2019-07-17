import csv
import re
import sys


def process_early():
    rows = []
    ward = ""
    dept = ""
    program = ""
    csv_rows = [row for row in csv.reader(sys.stdin)]
    for idx, row in enumerate(csv_rows):
        paren_match = re.search(r"^\([\d\-]{1,3}\)$", row[0].strip())
        if (
            row[0].strip() == ""
            or paren_match
            or all(c.strip() == "" for c in row)
            or any(
                any(w in c for w in ["Page ", "Budget", "Full Address"]) for c in row
            )
        ):
            continue

        dept_match = re.search(r"[A-Z]{2,6}\s*:\s*[A-Z]{2,6}", row[0])
        if dept_match:
            dept = dept_match.group().replace(" :", ":")
        elif row[0].startswith("Program"):
            program = row[0].split(":")[-1].strip()
        elif idx > 0 and csv_rows[idx - 1][0].startswith("Program"):
            program = " ".join([program, row[0].strip()])
        elif "Ward" in row[0]:
            ward = row[0].split(":")[-1].strip()
        elif all(c.strip() == "" for c in row[1:]):
            # Is address, append to last address row
            rows[-1]["location"] += " " + row[0].strip()
        else:
            rows.append(
                {
                    "year": sys.argv[1],
                    "ward": ward,
                    "dept": dept,
                    "program": program,
                    "location": row[0].strip(),
                    "desc": row[1].strip(),
                    "blocks": row[2],
                    "unit_count": row[3],
                    "est_cost": row[4],
                }
            )
    for row in rows:
        row["desc"] = re.sub(r"\s+", " ", row["desc"]).strip()
        row["location"] = re.sub(r"\s+", " ", row["location"]).strip()
        row["location"] = re.sub(r"(?<=[A-Z])&(?=[A-Z])", " & ", row["location"])
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            "year",
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
        if all(c.strip() == "" for c in row) or any(
            w in row[0] for w in ["MenuPackage", "TOTAL", "MENU BUDGET", "BALANCE"]
        ):
            continue
        if row[0].startswith("Ward:"):
            ward = row[0].split(":")[-1].strip()
        elif len(rows) > 0 and rows[-1]["est_cost"] == "":
            for idx, field in enumerate(["desc", "location", "est_cost"]):
                rows[-1][field] = " ".join([rows[-1][field], row[idx].strip()]).strip()
        else:
            rows.append(
                {
                    "year": sys.argv[1],
                    "ward": ward,
                    "desc": row[0].strip(),
                    "location": row[1].strip(),
                    "est_cost": row[2].strip(),
                }
            )
    for row in rows:
        row["desc"] = re.sub(r"\s+", " ", row["desc"]).strip()
        row["location"] = re.sub(r"\s+", " ", row["location"]).strip()
        row["location"] = re.sub(r"(?<=[A-Z])&(?=[A-Z])", " & ", row["location"])
    writer = csv.DictWriter(
        sys.stdout, fieldnames=["year", "ward", "desc", "location", "est_cost"]
    )
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    if sys.argv[1] < "2016":
        process_early()
    else:
        process_recent()
