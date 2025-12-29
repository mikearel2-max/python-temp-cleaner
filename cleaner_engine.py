import os
import shutil
from datetime import datetime

def clean_temp(path=None, dry_run=True):

    if path is None:
        path = os.getenv("TEMP")

    if not path:
        raise RuntimeError("Could not find TEMP directory.")

    temp_path = path  # optional alias for readability

    files_seen = 0
    files_deleted = 0
    errors = []
    success_rate = 0.0

    for name in os.listdir(temp_path):
        full_path = os.path.join(temp_path, name)
        files_seen += 1

        if dry_run:
            continue

        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.unlink(full_path)
                files_deleted += 1
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
                files_deleted += 1
        except Exception as e:
            errors.append((full_path, str(e)))

        
    success_rate = 0.0
    if files_seen > 0:
        success_rate = (files_deleted / files_seen) * 100


    # --- simple log file ---
    log_file = None
    if not dry_run:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = f"temp_clean_log_{ts}.txt"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Temp path: {temp_path}\n")
            f.write(f"Files seen: {files_seen}\n")
            f.write(f"Files deleted: {files_deleted}\n")
            f.write(f"Errors: {len(errors)}\n\n")
            for path, err in errors:
                f.write(f"[ERROR] {path} -> {err}\n")

    return {
        "temp_path": temp_path,
        "files_seen": files_seen,
        "files_deleted": files_deleted,
        "errors": errors,
        "dry_run": dry_run,
        "log_file": log_file,
        "success_rate": success_rate,
    }


# This block only runs if you run this file directly:  python temp_cleaner.py
if __name__ == "__main__":
    stats = clean_temp(dry_run=True)  # change to False if you want CLI clean

    print(f"TEMP folder: {stats['temp_path']}")
    print(f"Items found: {stats['files_seen']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    if stats["dry_run"]:
        print("Dry run only, nothing deleted.")
    else:
        print(f"Items deleted: {stats['files_deleted']}")
        if stats["errors"]:
            print("Some items could not be deleted:")
            for path, err in stats["errors"]:
                print(f" - {path}: {err}")
