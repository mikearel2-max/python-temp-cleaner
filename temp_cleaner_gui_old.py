import tkinter as tk
from tkinter import messagebox
from cleaner_engine import clean_temp   # import the engine you just wrote


def run_dry_run():
    try:
        stats = clean_temp(dry_run=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error running dry run:\n{e}")
        return

    msg = (
        f"TEMP folder:\n{stats['temp_path']}\n\n"
        f"Items found: {stats['files_seen']}\n"
        f"Dry run only – nothing was deleted."
    )
    messagebox.showinfo("Dry Run Complete", msg)


def run_cleanup():
    # Confirm with the user first
    confirm = messagebox.askyesno(
        "Confirm Cleanup",
        "This will permanently delete temporary files.\n\n"
        "Are you sure you want to continue?"
    )
    if not confirm:
        return

    try:
        stats = clean_temp(dry_run=False)
    except Exception as e:
        messagebox.showerror("Error", f"Error during cleanup:\n{e}")
        return

    msg = (
        f"TEMP folder:\n{stats['temp_path']}\n\n"
        f"Items found: {stats['files_seen']}\n"
        f"Items deleted: {stats['files_deleted']}\n"
    )
    if stats["errors"]:
        msg += f"\nSome items could not be deleted ({len(stats['errors'])})."
    if stats.get("log_file"):
        msg += f"\n\nDetails saved to:\n{stats['log_file']}"



def build_gui():
    root = tk.Tk()
    root.title("Temp Cleaner")

    # Basic window size
    root.geometry("350x180")

    title_label = tk.Label(
        root,
        text="Windows Temp Cleaner",
        font=("Segoe UI", 14, "bold")
    )
    title_label.pack(pady=(15, 10))

    info_label = tk.Label(
        root,
        text="Run a dry run first to see how many\n"
             "items are in your TEMP folder.\n"
             "Then run Cleanup to delete them.",
        justify="center"
    )
    info_label.pack(pady=(0, 15))

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    dry_run_button = tk.Button(
        button_frame,
        text="Dry Run",
        width=12,
        command=run_dry_run
    )
    dry_run_button.grid(row=0, column=0, padx=5)

    clean_button = tk.Button(
        button_frame,
        text="Clean Now",
        width=12,
        command=run_cleanup
    )
    clean_button.grid(row=0, column=1, padx=5)

    root.mainloop()


if __name__ == "__main__":
    build_gui()
