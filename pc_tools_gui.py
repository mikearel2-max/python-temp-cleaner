import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading

# ✅ Option A: if your engine is in cleaner_engine.py
from cleaner_engine import clean_temp

# ✅ Option B: if your engine file is still named temp_cleaner.py, use this instead:
# from temp_cleaner import clean_temp


class PcToolsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PC Tools - Temp Cleaner")
        self.geometry("720x480")

        self.selected_path = tk.StringVar(value=os.getenv("TEMP") or "")
        self.dry_run = tk.BooleanVar(value=True)

        self._build_ui()

    def _build_ui(self):
        # --- Top frame: path selection ---
        top = ttk.Frame(self, padding=12)
        top.pack(fill="x")

        ttk.Label(top, text="Folder to clean:").grid(row=0, column=0, sticky="w")

        self.path_entry = ttk.Entry(top, textvariable=self.selected_path, width=70)
        self.path_entry.grid(row=1, column=0, sticky="we", padx=(0, 8), pady=(6, 0))

        browse_btn = ttk.Button(top, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=1, column=1, sticky="e", pady=(6, 0))

        top.columnconfigure(0, weight=1)

        # --- Options ---
        opts = ttk.Frame(self, padding=(12, 0, 12, 12))
        opts.pack(fill="x")

        ttk.Checkbutton(
            opts,
            text="Dry run (do NOT delete anything)",
            variable=self.dry_run
        ).grid(row=0, column=0, sticky="w")

        # --- Run button ---
        run_frame = ttk.Frame(self, padding=(12, 0, 12, 12))
        run_frame.pack(fill="x")

        self.run_btn = ttk.Button(run_frame, text="Run", command=self.on_run)
        self.run_btn.pack(side="left")

        self.status_label = ttk.Label(run_frame, text="")
        self.status_label.pack(side="left", padx=12)

        # --- Output box ---
        out_frame = ttk.Frame(self, padding=(12, 0, 12, 12))
        out_frame.pack(fill="both", expand=True)

        ttk.Label(out_frame, text="Results:").pack(anchor="w")

        self.output = tk.Text(out_frame, height=14, wrap="word")
        self.output.pack(fill="both", expand=True, pady=(6, 0))

        # Make it read-only-ish (we’ll toggle state when writing)
        self.output.configure(state="disabled")

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select a folder to clean")
        if folder:
            self.selected_path.set(folder)

    def on_run(self):
        path = self.selected_path.get().strip()
        if not path:
            messagebox.showerror("Missing folder", "Please choose a folder.")
            return

        if not os.path.exists(path):
            messagebox.showerror("Invalid folder", f"Folder does not exist:\n{path}")
            return

        # Safety: if not dry-run, require confirmation
        if not self.dry_run.get():
            ok = messagebox.askyesno(
                "Confirm delete",
                "Dry run is OFF.\n\nThis will DELETE files/folders in the selected directory.\n\nAre you sure?"
            )
            if not ok:
                return

        # Run in background thread so GUI doesn't freeze
        self.run_btn.configure(state="disabled")
        self.status_label.configure(text="Running...")

        t = threading.Thread(target=self._run_cleaner, daemon=True)
        t.start()

    def _run_cleaner(self):
        path = self.selected_path.get().strip()
        dry_run = self.dry_run.get()

        try:
            stats = clean_temp(path=path, dry_run=dry_run)
        except Exception as e:
            self._ui_error(str(e))
            return

        self._ui_output(stats)

    def _ui_error(self, msg: str):
        def _update():
            self.run_btn.configure(state="normal")
            self.status_label.configure(text="")
            messagebox.showerror("Error", msg)

        self.after(0, _update)

    def _ui_output(self, stats: dict):
        def _update():
            self.run_btn.configure(state="normal")
            self.status_label.configure(text="Done.")

            lines = []
            lines.append(f"Folder: {stats.get('temp_path')}")
            lines.append(f"Dry run: {stats.get('dry_run')}")
            lines.append(f"Items found: {stats.get('files_seen')}")
            lines.append(f"Items deleted: {stats.get('files_deleted')}")
            if "success_rate" in stats:
                lines.append(f"Success rate: {stats.get('success_rate'):.1f}%")
            lines.append(f"Errors: {len(stats.get('errors', []))}")

            log_file = stats.get("log_file")
            if log_file:
                lines.append(f"Log file: {log_file}")

            # Show up to first 20 errors
            errs = stats.get("errors", [])
            if errs:
                lines.append("\n--- First errors ---")
                for p, err in errs[:20]:
                    lines.append(f"- {p} -> {err}")

            self.output.configure(state="normal")
            self.output.delete("1.0", "end")
            self.output.insert("1.0", "\n".join(lines))
            self.output.configure(state="disabled")

        self.after(0, _update)


if __name__ == "__main__":
    app = PcToolsGUI()
    app.mainloop()
