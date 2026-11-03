import os
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date

# Pillow is optional. It enables previews for JPG, JPEG, PNG, GIF, BMP and WebP.
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# CampusFind: a beginner-friendly Tkinter lost-and-found demo.
# Data is kept in memory, so reports reset when the application closes.

BG = "#F3F6FB"
NAVY = "#17243A"
BLUE = "#356AE6"
TEXT = "#1F2937"
MUTED = "#6B7280"
WHITE = "#FFFFFF"
GREEN = "#16805D"
ORANGE = "#B96A16"
RED = "#B42318"


class CampusFindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CampusFind | College Lost & Found")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        self.items = [
            {
                "id": 1, "type": "Lost", "name": "Scientific Calculator",
                "category": "Electronics", "location": "Block 3 - Room 204",
                "date": str(date.today()), "description": "Black calculator with a small sticker on the back.",
                "status": "Open"
            },
            {
                "id": 2, "type": "Found", "name": "Blue Water Bottle",
                "category": "Accessories", "location": "Central Library",
                "date": str(date.today()), "description": "Blue reusable bottle found near the reading desks.",
                "status": "Open"
            },
            {
                "id": 3, "type": "Lost", "name": "Student Notebook",
                "category": "Books & Stationery", "location": "ECE Lab",
                "date": str(date.today()), "description": "A ruled notebook with electronics notes.",
                "status": "Open"
            },
            {
                "id": 4, "type": "Found", "name": "Black Umbrella",
                "category": "Accessories", "location": "Main Canteen",
                "date": str(date.today()), "description": "Foldable black umbrella left near the entrance.",
                "status": "Resolved"
            },
        ]
        self.next_id = 5
        self.search_var = tk.StringVar()
        self.type_filter = tk.StringVar(value="All")
        self.category_filter = tk.StringVar(value="All")
        # Browse Items opens on active reports. Resolved reports remain available
        # through the Resolved filter instead of cluttering the active list.
        self.status_filter = tk.StringVar(value="Open")

        self.setup_styles()
        self.build_layout()
        self.refresh_all()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=34, font=("Segoe UI", 10),
                        background=WHITE, fieldbackground=WHITE, foreground=TEXT)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#E8EDF6", foreground=NAVY, padding=8)
        style.map("Treeview", background=[("selected", "#DCE7FF")],
                  foreground=[("selected", NAVY)])
        style.configure("TCombobox", padding=6)
        style.configure("TEntry", padding=7)

    def build_layout(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg=NAVY, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="⌕  CampusFind", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", padx=20, pady=(28, 4))
        tk.Label(sidebar, text="COLLEGE LOST & FOUND", bg=NAVY, fg="#AAB8D0",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(0, 30))

        self.nav_button(sidebar, "▦   Dashboard", self.show_dashboard)
        self.nav_button(sidebar, "＋   Report an Item", self.show_report)
        self.nav_button(sidebar, "⌕   Browse Items", self.show_browse)

        tk.Frame(sidebar, bg="#35425A", height=1).pack(fill="x", padx=18, pady=22)
        tk.Label(sidebar, text="DEMO VERSION", bg=NAVY, fg="#AAB8D0",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22)
        tk.Label(sidebar, text="Sample data is stored only\nwhile this app is open.",
                 bg=NAVY, fg="#D6DEEA", justify="left",
                 font=("Segoe UI", 9)).pack(anchor="w", padx=22, pady=8)

        # Main area
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        header = tk.Frame(self.main, bg=WHITE, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="Campus item recovery, made simpler.",
                 bg=WHITE, fg=NAVY, font=("Segoe UI", 16, "bold")).pack(
                     side="left", padx=28, pady=20)
        tk.Label(header, text="FRONTEND DEMO", bg="#E8F7F0", fg=GREEN,
                 font=("Segoe UI", 9, "bold"), padx=10, pady=6).pack(
                     side="right", padx=24)

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=26, pady=22)

    def nav_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, anchor="w",
                        bg=NAVY, fg=WHITE, activebackground="#2D3E5A",
                        activeforeground=WHITE, relief="flat", bd=0,
                        font=("Segoe UI", 11), padx=20, pady=13, cursor="hand2")
        btn.pack(fill="x", padx=10, pady=2)

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def title_block(self, title, subtitle):
        tk.Label(self.content, text=title, bg=BG, fg=NAVY,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(self.content, text=subtitle, bg=BG, fg=MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 18))

    def card(self, parent, title, value, accent):
        frame = tk.Frame(parent, bg=WHITE, highlightbackground="#E1E7F0",
                         highlightthickness=1)
        tk.Frame(frame, bg=accent, width=5).pack(side="left", fill="y")
        inner = tk.Frame(frame, bg=WHITE)
        inner.pack(side="left", fill="both", expand=True, padx=15, pady=14)
        tk.Label(inner, text=title, bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w")
        value_label = tk.Label(inner, text=str(value), bg=WHITE, fg=NAVY,
                               font=("Segoe UI", 23, "bold"))
        value_label.pack(anchor="w", pady=(4, 0))
        frame.value_label = value_label
        return frame

    def refresh_all(self):
        # Refresh dashboard only if it is currently displayed.
        if getattr(self, "current_page", "") == "dashboard":
            self.show_dashboard()
        elif getattr(self, "current_page", "") == "browse":
            self.show_browse()

    def show_dashboard(self):
        self.current_page = "dashboard"
        self.clear_content()
        self.title_block("Dashboard", "A simple overview of reported campus belongings.")

        total_lost = sum(i["type"] == "Lost" for i in self.items)
        total_found = sum(i["type"] == "Found" for i in self.items)
        resolved = sum(i["status"] == "Resolved" for i in self.items)
        open_items = sum(i["status"] == "Open" for i in self.items)

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x", pady=(0, 20))
        for col, (label, value, color) in enumerate([
            ("Lost reports", total_lost, BLUE),
            ("Found reports", total_found, GREEN),
            ("Open reports", open_items, ORANGE),
            ("Resolved", resolved, "#7C5CE7"),
        ]):
            c = self.card(cards, label, value, color)
            c.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 10, 0))
            cards.grid_columnconfigure(col, weight=1, uniform="cards")

        action_frame = tk.Frame(self.content, bg=BG)
        action_frame.pack(fill="x", pady=(0, 18))
        tk.Label(action_frame, text="Quick actions", bg=BG, fg=NAVY,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))
        self.action_button(action_frame, "＋  Report lost item", lambda: self.show_report("Lost"), BLUE).pack(side="left", padx=(0, 10))
        self.action_button(action_frame, "＋  Report found item", lambda: self.show_report("Found"), GREEN).pack(side="left")

        panel = tk.Frame(self.content, bg=WHITE, highlightbackground="#E1E7F0",
                         highlightthickness=1)
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="Recent reports", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(15, 8))

        recent = sorted(self.items, key=lambda x: x["id"], reverse=True)[:5]
        for item in recent:
            row = tk.Frame(panel, bg=WHITE)
            row.pack(fill="x", padx=18, pady=7)
            colour = BLUE if item["type"] == "Lost" else GREEN
            tk.Label(row, text=item["type"].upper(), bg=WHITE, fg=colour,
                     font=("Segoe UI", 9, "bold"), width=8, anchor="w").pack(side="left")
            tk.Label(row, text=item["name"], bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).pack(side="left", padx=8)
            tk.Label(row, text=item["location"], bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 9)).pack(side="left", padx=8)
            status_colour = GREEN if item["status"] == "Resolved" else ORANGE
            tk.Label(row, text=item["status"], bg=WHITE, fg=status_colour,
                     font=("Segoe UI", 9, "bold")).pack(side="right")
            ttk.Separator(panel, orient="horizontal").pack(fill="x", padx=18, pady=2)

    def action_button(self, parent, text, command, color=BLUE):
        return tk.Button(parent, text=text, command=command, bg=color, fg=WHITE,
                         activebackground=color, activeforeground=WHITE,
                         relief="flat", bd=0, font=("Segoe UI", 10, "bold"),
                         padx=14, pady=10, cursor="hand2")

    def show_report(self, report_type=None):
        self.current_page = "report"
        self.clear_content()
        report_type = report_type or "Lost"
        self.title_block("Report an Item", "Add a lost or found item to the demo portal.")

        outer = tk.Frame(self.content, bg=WHITE, highlightbackground="#E1E7F0",
                         highlightthickness=1)
        outer.pack(fill="both", expand=True)
        form = tk.Frame(outer, bg=WHITE)
        form.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(form, text="What would you like to report?", bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))
        type_var = tk.StringVar(value=report_type)
        type_combo = ttk.Combobox(form, textvariable=type_var, values=["Lost", "Found"],
                                  state="readonly", width=35)
        type_combo.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 16))

        name_var = tk.StringVar()
        category_var = tk.StringVar(value="Electronics")
        location_var = tk.StringVar()
        date_var = tk.StringVar(value=str(date.today()))
        selected_image_var = tk.StringVar()

        def field_label(text, row):
            tk.Label(form, text=text, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 10, "bold")).grid(row=row, column=0, sticky="w", pady=(6, 5))

        field_label("Item name *", 2)
        name_entry = ttk.Entry(form, textvariable=name_var, width=48)
        name_entry.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        field_label("Category", 4)
        category_combo = ttk.Combobox(form, textvariable=category_var,
                                      values=["Electronics", "ID & Cards", "Books & Stationery",
                                              "Accessories", "Clothing", "Keys", "Other"],
                                      state="readonly", width=45)
        category_combo.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        field_label("Location *", 6)
        location_entry = ttk.Entry(form, textvariable=location_var, width=48)
        location_entry.grid(row=7, column=0, sticky="ew", pady=(0, 8))

        field_label("Date (YYYY-MM-DD)", 8)
        date_entry = ttk.Entry(form, textvariable=date_var, width=48)
        date_entry.grid(row=9, column=0, sticky="ew", pady=(0, 8))

        field_label("Description", 10)
        description_text = tk.Text(form, width=48, height=4, font=("Segoe UI", 10),
                                   relief="solid", bd=1, wrap="word")
        description_text.grid(row=11, column=0, sticky="ew", pady=(0, 14))

        # Optional item photo upload. The selected file path is saved with the report.
        field_label("Item photo (optional)", 12)
        image_controls = tk.Frame(form, bg=WHITE)
        image_controls.grid(row=13, column=0, sticky="ew", pady=(0, 12))
        image_name_label = tk.Label(
            image_controls, text="No image selected", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 9), anchor="w"
        )

        def choose_image():
            image_path = filedialog.askopenfilename(
                parent=self.root,
                title="Select an item photo",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                    ("All files", "*.*"),
                ],
            )
            if image_path:
                selected_image_var.set(image_path)
                image_name_label.config(text=os.path.basename(image_path))

        def remove_image():
            selected_image_var.set("")
            image_name_label.config(text="No image selected")

        self.action_button(image_controls, "Choose image", choose_image, BLUE).pack(side="left")
        tk.Button(
            image_controls, text="Remove", command=remove_image,
            bg="#E8EDF6", fg=NAVY, relief="flat", bd=0,
            font=("Segoe UI", 9, "bold"), padx=10, pady=8, cursor="hand2"
        ).pack(side="left", padx=(8, 0))
        image_name_label.pack(side="left", padx=(10, 0))

        help_panel = tk.Frame(form, bg="#F3F6FB")
        help_panel.grid(row=2, column=1, rowspan=12, sticky="nsew", padx=(28, 0), pady=(0, 8))
        tk.Label(help_panel, text="Helpful tip", bg="#F3F6FB", fg=NAVY,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=16, pady=(16, 8))
        tk.Label(help_panel,
                 text="Use a clear item name and a general campus location.\n\n"
                      "Attach a clear photo to help identify the item.\n\n"
                      "For safety, do not enter passwords, full student IDs, "
                      "or private identifying details.\n\n"
                      "This demonstration uses local sample data. It does not "
                      "send reports to other students.",
                 bg="#F3F6FB", fg=MUTED, justify="left", wraplength=230,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=16, pady=(0, 16))

        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        def submit():
            name = name_var.get().strip()
            location = location_var.get().strip()
            item_date = date_var.get().strip()
            description = description_text.get("1.0", "end").strip()

            if not name:
                messagebox.showerror("Missing information", "Please enter the item name.")
                name_entry.focus_set()
                return
            if not location:
                messagebox.showerror("Missing information", "Please enter the location.")
                location_entry.focus_set()
                return
            try:
                date.fromisoformat(item_date)
            except ValueError:
                messagebox.showerror("Invalid date", "Please use YYYY-MM-DD, for example 2026-10-12.")
                date_entry.focus_set()
                return

            self.items.append({
                "id": self.next_id,
                "type": type_var.get(),
                "name": name,
                "category": category_var.get(),
                "location": location,
                "date": item_date,
                "description": description,
                "image_path": selected_image_var.get().strip() or None,
                "status": "Open",
            })
            self.next_id += 1
            messagebox.showinfo("Report added", f"Your {type_var.get().lower()} report has been added to this demo.")
            self.show_dashboard()

        buttons = tk.Frame(form, bg=WHITE)
        buttons.grid(row=14, column=0, sticky="w", pady=(0, 4))
        self.action_button(buttons, "Submit report", submit, BLUE).pack(side="left", padx=(0, 8))
        tk.Button(buttons, text="Reset form",
                  command=lambda: (name_var.set(""), category_var.set("Electronics"),
                                   location_var.set(""), date_var.set(str(date.today())),
                                   description_text.delete("1.0", "end"),
                                   remove_image()),
                  bg="#E8EDF6", fg=NAVY, relief="flat", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=14, pady=10,
                  cursor="hand2").pack(side="left")

    def show_browse(self):
        self.current_page = "browse"
        self.clear_content()
        self.title_block(
            "Browse Items",
            "Active reports are shown by default. Use Status = Resolved to view completed cases."
        )

        filter_box = tk.Frame(self.content, bg=WHITE, highlightbackground="#E1E7F0",
                              highlightthickness=1)
        filter_box.pack(fill="x", pady=(0, 14))
        top = tk.Frame(filter_box, bg=WHITE)
        top.pack(fill="x", padx=14, pady=12)

        search_entry = ttk.Entry(top, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        search_entry.insert(0, "")
        search_entry.bind("<KeyRelease>", lambda event: self.populate_tree())

        type_combo = ttk.Combobox(top, textvariable=self.type_filter,
                                  values=["All", "Lost", "Found"], state="readonly", width=10)
        type_combo.pack(side="left", padx=5)
        type_combo.bind("<<ComboboxSelected>>", lambda event: self.populate_tree())

        category_combo = ttk.Combobox(top, textvariable=self.category_filter,
                                      values=["All", "Electronics", "ID & Cards",
                                              "Books & Stationery", "Accessories",
                                              "Clothing", "Keys", "Other"],
                                      state="readonly", width=19)
        category_combo.pack(side="left", padx=5)
        category_combo.bind("<<ComboboxSelected>>", lambda event: self.populate_tree())

        status_combo = ttk.Combobox(top, textvariable=self.status_filter,
                                    values=["All", "Open", "Resolved"],
                                    state="readonly", width=11)
        status_combo.pack(side="left", padx=5)
        status_combo.bind("<<ComboboxSelected>>", lambda event: self.populate_tree())

        tk.Button(top, text="Clear", command=self.clear_filters,
                  bg="#E8EDF6", fg=NAVY, relief="flat", padx=12, pady=7,
                  cursor="hand2").pack(side="left", padx=(5, 0))

        table_panel = tk.Frame(self.content, bg=WHITE, highlightbackground="#E1E7F0",
                               highlightthickness=1)
        table_panel.pack(fill="both", expand=True)

        columns = ("type", "name", "category", "location", "date", "status", "photo")
        self.tree = ttk.Treeview(table_panel, columns=columns, show="headings", selectmode="browse")
        headings = {
            "type": ("Type", 70), "name": ("Item name", 160),
            "category": ("Category", 130), "location": ("Location", 165),
            "date": ("Date", 100), "status": ("Status", 85),
            "photo": ("Photo", 55)
        }
        for col, (heading, width) in headings.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, minwidth=65, anchor="w")
        yscroll = ttk.Scrollbar(table_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        yscroll.pack(side="right", fill="y", padx=(0, 8), pady=8)

        self.tree.bind("<Double-1>", lambda event: self.view_selected())
        bottom = tk.Frame(self.content, bg=BG)
        bottom.pack(fill="x", pady=(12, 0))
        self.action_button(bottom, "View details", self.view_selected, BLUE).pack(side="left", padx=(0, 8))
        self.action_button(bottom, "Suggest possible matches", self.show_matches, GREEN).pack(side="left", padx=(0, 8))
        self.action_button(bottom, "Mark resolved", self.mark_resolved, ORANGE).pack(side="left")
        self.populate_tree()

    def filtered_items(self):
        query = self.search_var.get().strip().lower()
        result = []
        for item in self.items:
            searchable = " ".join([item["name"], item["category"], item["location"],
                                   item["description"], item["type"]]).lower()
            if query and query not in searchable:
                continue
            if self.type_filter.get() != "All" and item["type"] != self.type_filter.get():
                continue
            if self.category_filter.get() != "All" and item["category"] != self.category_filter.get():
                continue
            if self.status_filter.get() != "All" and item["status"] != self.status_filter.get():
                continue
            result.append(item)
        return result

    def populate_tree(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists():
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.filtered_items():
            self.tree.insert("", "end", iid=str(item["id"]),
                             values=(item["type"], item["name"], item["category"],
                                     item["location"], item["date"], item["status"],
                                     "Yes" if item.get("image_path") else "No"))

    def clear_filters(self):
        self.search_var.set("")
        self.type_filter.set("All")
        self.category_filter.set("All")
        self.status_filter.set("Open")
        self.populate_tree()

    def selected_item(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists():
            return None
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select an item", "Please select a report from the table first.")
            return None
        item_id = int(selected[0])
        return next((item for item in self.items if item["id"] == item_id), None)

    def view_selected(self):
        item = self.selected_item()
        if not item:
            return
        detail = tk.Toplevel(self.root)
        detail.title("Item details")
        detail.geometry("500x680")
        detail.configure(bg=WHITE)
        detail.transient(self.root)
        tk.Label(detail, text=item["name"], bg=WHITE, fg=NAVY,
                 font=("Segoe UI", 17, "bold"), wraplength=380).pack(anchor="w", padx=22, pady=(22, 6))
        tk.Label(detail, text=f'{item["type"]} report  •  {item["status"]}',
                 bg=WHITE, fg=GREEN if item["status"] == "Resolved" else BLUE,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=22, pady=(0, 14))
        details = [
            ("Category", item["category"]),
            ("Location", item["location"]),
            ("Date", item["date"]),
            ("Description", item["description"] or "No description provided."),
        ]
        for label, value in details:
            tk.Label(detail, text=label, bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(5, 0))
            tk.Label(detail, text=value, bg=WHITE, fg=TEXT, justify="left",
                     wraplength=440, font=("Segoe UI", 10)).pack(anchor="w", padx=22)

        image_path = item.get("image_path")
        if image_path:
            tk.Label(detail, text="Item photo", bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=22, pady=(12, 4))
            if os.path.isfile(image_path):
                preview = None
                try:
                    if Image is not None and ImageTk is not None:
                        with Image.open(image_path) as source_image:
                            preview_image = source_image.copy()
                        preview_image.thumbnail((420, 220))
                        preview = ImageTk.PhotoImage(preview_image)
                    else:
                        # Tkinter can preview some formats (such as PNG/GIF) without Pillow.
                        preview = tk.PhotoImage(file=image_path)
                        scale = max(1, (max(preview.width(), preview.height()) + 419) // 420)
                        if scale > 1:
                            preview = preview.subsample(scale, scale)
                except Exception:
                    preview = None

                if preview is not None:
                    preview_label = tk.Label(detail, image=preview, bg=WHITE)
                    preview_label.image = preview  # Keep a reference so Tkinter does not clear it.
                    preview_label.pack(anchor="w", padx=22, pady=(0, 8))
                else:
                    tk.Label(detail, text=os.path.basename(image_path), bg=WHITE, fg=TEXT,
                             font=("Segoe UI", 9)).pack(anchor="w", padx=22)
                    tk.Button(
                        detail, text="Open image", command=lambda p=image_path: self.open_image_file(p),
                        bg="#E8EDF6", fg=NAVY, relief="flat", padx=12, pady=6
                    ).pack(anchor="w", padx=22, pady=(4, 0))
            else:
                tk.Label(detail, text="The saved image file could not be found.",
                         bg=WHITE, fg=RED, font=("Segoe UI", 9)).pack(anchor="w", padx=22)
        else:
            tk.Label(detail, text="No image was uploaded for this report.",
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=22, pady=(8, 0))

        tk.Button(detail, text="Close", command=detail.destroy, bg=BLUE, fg=WHITE,
                  relief="flat", padx=18, pady=8).pack(anchor="w", padx=22, pady=20)

    def open_image_file(self, image_path):
        """Open the selected image with the computer's default image viewer."""
        try:
            if hasattr(os, "startfile"):
                os.startfile(image_path)
            else:
                webbrowser.open("file://" + os.path.abspath(image_path))
        except Exception as error:
            messagebox.showerror("Unable to open image", str(error))

    def mark_resolved(self):
        item = self.selected_item()
        if not item:
            return
        if item["status"] == "Resolved":
            messagebox.showinfo("Already resolved", "This report is already marked as resolved.")
            return
        if messagebox.askyesno("Mark as resolved", f'Mark "{item["name"]}" as resolved?'):
            item["status"] = "Resolved"
            # Return to the active-only view so the resolved case disappears immediately.
            # The report is retained and can still be viewed with Status = Resolved.
            self.status_filter.set("Open")
            self.populate_tree()
            messagebox.showinfo(
                "Updated",
                "The report has been resolved and removed from the active list. "
                "You can find it later by selecting Status = Resolved."
            )

    def show_matches(self):
        # A simple demo matcher: pair open Lost/Found reports sharing a category
        # and either a similar name or a similar location.
        open_items = [i for i in self.items if i["status"] == "Open"]
        matches = []
        for lost in open_items:
            if lost["type"] != "Lost":
                continue
            for found in open_items:
                if found["type"] != "Found":
                    continue
                same_category = lost["category"] == found["category"]
                name_words = set(lost["name"].lower().split()) & set(found["name"].lower().split())
                same_location = lost["location"].lower() == found["location"].lower()
                if same_category and (name_words or same_location):
                    matches.append((lost, found, "same category plus similar name or location"))

        win = tk.Toplevel(self.root)
        win.title("Possible matches")
        win.geometry("680x430")
        win.configure(bg=BG)
        tk.Label(win, text="Possible matches", bg=BG, fg=NAVY,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=(20, 4))
        tk.Label(win, text="These are suggestions only. Always verify the item before returning it.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(0, 14))
        panel = tk.Frame(win, bg=WHITE)
        panel.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        if not matches:
            tk.Label(panel, text="No possible matches found yet.\nTry adding more lost and found reports.",
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 12), justify="center").pack(expand=True)
        else:
            for lost, found, reason in matches:
                block = tk.Frame(panel, bg=WHITE, highlightbackground="#DCE3EE",
                                 highlightthickness=1)
                block.pack(fill="x", padx=12, pady=10)
                tk.Label(block, text=f'LOST: {lost["name"]}  •  {lost["location"]}',
                         bg=WHITE, fg=BLUE, font=("Segoe UI", 10, "bold"),
                         wraplength=590, justify="left").pack(anchor="w", padx=12, pady=(10, 4))
                tk.Label(block, text=f'FOUND: {found["name"]}  •  {found["location"]}',
                         bg=WHITE, fg=GREEN, font=("Segoe UI", 10, "bold"),
                         wraplength=590, justify="left").pack(anchor="w", padx=12, pady=4)
                tk.Label(block, text=f"Why suggested: {reason}",
                         bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(4, 10))


def main():
    root = tk.Tk()
    app = CampusFindApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
