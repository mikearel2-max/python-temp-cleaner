from cleaner_engine import clean_temp

def show_menu():
    print("\n=== PC TOOLS ===")
    print("1) Temp Cleaner (Dry Run)")
    print("2) Temp Cleaner (Delete)")
    print("3) Exit")

def run_temp_dry():
    stats = clean_temp(dry_run=True)
    print(f"\nTemp: {stats['temp_path']}")
    print(f"Items found: {stats['files_seen']}")
    print("Dry run only (nothing deleted).")

def run_temp_delete():
    confirm = input("Type YES to confirm delete: ").strip()
    if confirm == "YES":
        stats = clean_temp(dry_run=False)
        print(f"\nDeleted: {stats['files_deleted']}")
        print(f"Failed: {len(stats['errors'])}")
    else:
        print("Cancelled.")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            run_temp_dry()
        elif choice == "2":
            run_temp_delete()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
