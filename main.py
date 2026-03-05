import tkinter as tk
from tkinter import ttk
from datetime import datetime


class ChatApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("namespace chat")
        self.geometry("1100x700")
        self.minsize(900, 560)
        self.configure(bg="#0d1117")

        self.contacts = [
            "General",
            "Product Team",
            "Design",
            "Dev Ops",
            "Support",
            "Random",
        ]
        self.active_contact = tk.StringVar(value=self.contacts[0])
        self.message_input = tk.StringVar()

        self._create_styles()
        self._build_layout()
        self._seed_messages()

        self.bind("<Return>", self._send_message_event)

    def _create_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Sidebar.TFrame", background="#111827")
        style.configure("Main.TFrame", background="#0b1220")
        style.configure("TopBar.TFrame", background="#111827")
        style.configure("Input.TFrame", background="#111827")

        style.configure(
            "Channel.TButton",
            background="#111827",
            foreground="#cbd5e1",
            borderwidth=0,
            focusthickness=0,
            padding=(14, 10),
            font=("Segoe UI", 10),
            anchor="w",
        )
        style.map(
            "Channel.TButton",
            background=[("active", "#1f2937"), ("pressed", "#334155")],
            foreground=[("active", "#ffffff")],
        )

        style.configure(
            "Send.TButton",
            background="#2563eb",
            foreground="#ffffff",
            borderwidth=0,
            focusthickness=0,
            padding=(16, 8),
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Send.TButton",
            background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
        )

    def _build_layout(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self, style="Sidebar.TFrame")
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        sidebar.configure(width=260)

        brand = tk.Label(
            sidebar,
            text="namespace",
            fg="#f8fafc",
            bg="#111827",
            font=("Segoe UI Semibold", 20),
            padx=20,
            pady=20,
            anchor="w",
        )
        brand.pack(fill="x")

        section = tk.Label(
            sidebar,
            text="Channels",
            fg="#94a3b8",
            bg="#111827",
            font=("Segoe UI", 9),
            padx=20,
            pady=2,
            anchor="w",
        )
        section.pack(fill="x")

        self.channel_buttons = {}
        for contact in self.contacts:
            btn = ttk.Button(
                sidebar,
                text=f"# {contact}",
                style="Channel.TButton",
                command=lambda c=contact: self._switch_channel(c),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self.channel_buttons[contact] = btn

        footer = tk.Label(
            sidebar,
            text="Built with Python + Tkinter",
            fg="#64748b",
            bg="#111827",
            font=("Segoe UI", 8),
            padx=20,
            pady=18,
            anchor="w",
        )
        footer.pack(side="bottom", fill="x")

        main = ttk.Frame(self, style="Main.TFrame")
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        top = ttk.Frame(main, style="TopBar.TFrame")
        top.grid(row=0, column=0, sticky="ew")

        self.header = tk.Label(
            top,
            text=f"# {self.active_contact.get()}",
            fg="#f8fafc",
            bg="#111827",
            font=("Segoe UI Semibold", 16),
            padx=20,
            pady=16,
            anchor="w",
        )
        self.header.pack(side="left", fill="x", expand=True)

        status = tk.Label(
            top,
            text="● Online",
            fg="#34d399",
            bg="#111827",
            font=("Segoe UI", 10),
            padx=20,
        )
        status.pack(side="right")

        chat_wrap = tk.Frame(main, bg="#0b1220")
        chat_wrap.grid(row=1, column=0, sticky="nsew")
        chat_wrap.grid_rowconfigure(0, weight=1)
        chat_wrap.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            chat_wrap,
            bg="#0b1220",
            highlightthickness=0,
            bd=0,
            relief="flat",
        )
        scrollbar = ttk.Scrollbar(chat_wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.messages_frame = tk.Frame(self.canvas, bg="#0b1220")
        self.messages_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw", width=1)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        input_bar = ttk.Frame(main, style="Input.TFrame")
        input_bar.grid(row=2, column=0, sticky="ew", padx=16, pady=16)
        input_bar.grid_columnconfigure(0, weight=1)

        self.entry = tk.Entry(
            input_bar,
            textvariable=self.message_input,
            bg="#1f2937",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat",
            font=("Segoe UI", 11),
            bd=0,
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 10), ipady=11, ipadx=12)

        send_btn = ttk.Button(input_bar, text="Send", style="Send.TButton", command=self._send_message)
        send_btn.grid(row=0, column=1)

        self._highlight_active_channel()

    def _on_canvas_resize(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(1, width=event.width)

    def _seed_messages(self) -> None:
        demos = [
            ("system", "Welcome to namespace 👋", "09:40"),
            ("other", "Team standup starts in 20 min.", "09:43"),
            ("self", "Got it. I will join from desktop app.", "09:44"),
            ("other", "Perfect! Also please review the build plan for the .exe.", "09:45"),
        ]
        for author, text, stamp in demos:
            self._add_message_bubble(author, text, stamp)

    def _switch_channel(self, channel: str) -> None:
        self.active_contact.set(channel)
        self.header.config(text=f"# {channel}")
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        now = datetime.now().strftime("%H:%M")
        self._add_message_bubble("system", f"Switched to #{channel}", now)
        self._highlight_active_channel()

    def _highlight_active_channel(self) -> None:
        active = self.active_contact.get()
        for name, btn in self.channel_buttons.items():
            if name == active:
                btn.state(["pressed"])
            else:
                btn.state(["!pressed"])

    def _send_message_event(self, _event: tk.Event) -> None:
        self._send_message()

    def _send_message(self) -> None:
        text = self.message_input.get().strip()
        if not text:
            return
        stamp = datetime.now().strftime("%H:%M")
        self._add_message_bubble("self", text, stamp)
        self.message_input.set("")
        self.after(350, lambda: self._bot_reply(text))

    def _bot_reply(self, text: str) -> None:
        msg = f"Echo from namespace bot: {text[:90]}"
        stamp = datetime.now().strftime("%H:%M")
        self._add_message_bubble("other", msg, stamp)

    def _add_message_bubble(self, author: str, message: str, stamp: str) -> None:
        row = tk.Frame(self.messages_frame, bg="#0b1220")
        row.pack(fill="x", pady=6, padx=14)

        is_self = author == "self"
        is_system = author == "system"

        bubble_bg = "#1d4ed8" if is_self else "#1f2937"
        text_color = "#ffffff" if is_self else "#e2e8f0"

        if is_system:
            line = tk.Label(
                row,
                text=message,
                bg="#0b1220",
                fg="#93c5fd",
                font=("Segoe UI", 9, "italic"),
                anchor="center",
                pady=4,
            )
            line.pack(fill="x")
        else:
            bubble = tk.Frame(row, bg=bubble_bg, padx=12, pady=8)
            bubble.pack(side="right" if is_self else "left", anchor="e" if is_self else "w")

            body = tk.Label(
                bubble,
                text=message,
                bg=bubble_bg,
                fg=text_color,
                font=("Segoe UI", 10),
                justify="left",
                wraplength=520,
            )
            body.pack(anchor="w")

            time_label = tk.Label(
                bubble,
                text=stamp,
                bg=bubble_bg,
                fg="#bfdbfe" if is_self else "#94a3b8",
                font=("Segoe UI", 8),
                pady=2,
            )
            time_label.pack(anchor="e")

        self.update_idletasks()
        self.canvas.yview_moveto(1.0)


def main() -> None:
    app = ChatApp()
    app.mainloop()


if __name__ == "__main__":
    main()
