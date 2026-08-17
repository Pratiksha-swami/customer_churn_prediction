import customtkinter as ctk

# ---------------- Colors ----------------
BG = "#070B1A"
SIDEBAR = "#090F23"
CARD = "#0F1B3D"
BORDER = "#22315A"
PURPLE = "#7C5CFF"
TEXT = "#FFFFFF"
SUBTEXT = "#9AA4C7"


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, callback):

        super().__init__(
            parent,
            width=240,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.pack_propagate(False)
        self.callback = callback
        self.buttons = {}

        self.build_sidebar()

    def build_sidebar(self):

        # ---------------- Logo ----------------
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(25, 10))

        ctk.CTkLabel(
            logo_frame,
            text="◉",
            font=("Segoe UI", 30, "bold"),
            text_color=PURPLE
        ).pack(side="left")

        text_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_frame.pack(side="left", padx=8)

        ctk.CTkLabel(
            text_frame,
            text="ChurnSight",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text="Customer Churn Analytics",
            font=("Segoe UI", 11),
            text_color=SUBTEXT
        ).pack(anchor="w")

        # Divider
        ctk.CTkFrame(self, height=1, fg_color=BORDER).pack(fill="x", padx=20, pady=15)

        # ---------------- Navigation ----------------
        nav_items = [
            ("📊", "Dashboard"),
            ("🎯", "Churn Prediction"),
            ("📈", "EDA Explorer"),
            ("🤖", "model")
            
        ]

        for icon, name in nav_items:

            btn = ctk.CTkButton(
                self,
                text=f"{icon}   {name}",
                height=48,
                corner_radius=12,
                fg_color="transparent",
                hover_color="#1B2A52",
                anchor="w",
                font=("Segoe UI", 14),
                command=lambda n=name: self.callback(n)
            )

            btn.pack(fill="x", padx=15, pady=4)

            self.buttons[name] = btn

        # ---------------- Quick Insight ----------------
        quick = ctk.CTkFrame(
            self,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )

        quick.pack(fill="x", padx=18, pady=(25, 18))

        ctk.CTkLabel(
            quick,
            text="💡  Quick Insight",
            font=("Segoe UI", 16, "bold"),
            text_color=PURPLE
        ).pack(anchor="w", padx=15, pady=(15, 8))

        ctk.CTkLabel(
            quick,
            text=(
                "Month-to-month contracts\n"
                "have the highest churn.\n\n"
                "Long-term contracts\n"
                "improve retention."
            ),
            justify="left",
            text_color=SUBTEXT,
            font=("Segoe UI", 12)
        ).pack(anchor="w", padx=15, pady=(0, 15))

        # Spacer
        # ctk.CTkFrame(self, fg_color="transparent").pack(expand=True, fill="both")

        # ---------------- Admin Card ----------------
        profile = ctk.CTkFrame(
            self,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=14
        )

        profile.pack(fill="x", padx=15, pady=10)

        avatar = ctk.CTkFrame(
            profile,
            width=42,
            height=42,
            corner_radius=21,
            fg_color=PURPLE
        )

        avatar.pack(side="left", padx=12, pady=12)
        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text="👤",
            font=("Segoe UI", 18)
        ).place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(profile, fg_color="transparent")
        info.pack(side="left", padx=5)

        ctk.CTkLabel(
            info,
            text="Admin",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text="Data Analyst",
            font=("Segoe UI", 11),
            text_color=SUBTEXT
        ).pack(anchor="w")

        # ---------------- Logout ----------------
        self.logout = ctk.CTkButton(
            self,
            text="↩  Log Out",
            height=42,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#1B2A52",
            anchor="w"
        )

        self.logout.pack(fill="x", padx=18, pady=(10, 20))

    # Highlight active page
    def set_active(self, name):

        for page, btn in self.buttons.items():

            if page == name:
                btn.configure(
                    fg_color=PURPLE,
                    text_color="white"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT
                )