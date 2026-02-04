from pathlib import Path

routers = [
    "app/routers/milk_collection.py",
    "app/routers/customer.py",
    "app/routers/billing.py",
]

for fpath in routers:
    p = Path(fpath)
    if p.exists():
        content = p.read_text()
        new_content = content.replace("public.", "")
        p.write_text(new_content)
        print(f"Fixed: {p.name}")
    else:
        print(f"Skipped (not found): {p.name}")
