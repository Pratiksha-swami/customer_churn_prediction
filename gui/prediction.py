import customtkinter as ctk
from utils.predictor import predict_customer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Wedge

# ---------- Colors ----------
BG = "#070B1A"
CARD = "#0F1B3D"
BORDER = "#22315A"

PURPLE = "#7C5CFF"
RED = "#FF4D6D"
GREEN = "#3CCB5A"

TEXT = "#FFFFFF"
SUBTEXT = "#9AA4C7"


class PredictionPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=BG)

        self.build_ui()

    def build_ui(self):

        # ================= Header =================
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20,15))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Churn Prediction",
            font=("Segoe UI",30,"bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Enter customer details and predict churn risk",
            font=("Segoe UI",13),
            text_color=SUBTEXT
        ).pack(anchor="w")

        right = ctk.CTkFrame(header, fg_color="transparent")
        right.pack(side="right")

        ctk.CTkButton(
            right,
            text="📅 01 Jan 2022 - 31 Dec 2022",
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            width=220,
            height=42
        ).pack(side="left")

        # ================= Main Layout =================
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=(0,20))

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        left_panel = ctk.CTkFrame(
            body,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )
        left_panel.grid(row=0,column=0,padx=(0,10),sticky="nsew")

        right_panel = ctk.CTkFrame(
            body,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )
        right_panel.grid(row=0,column=1,padx=(10,0),sticky="nsew")

        self.build_form(left_panel)
        self.build_result(right_panel)

    # ================= Left Form =================

    def build_form(self, parent):

        ctk.CTkLabel(
            parent,
            text="👤 Customer Information",
            font=("Segoe UI",22,"bold")
        ).pack(anchor="w", padx=20, pady=(20,5))

        ctk.CTkLabel(
            parent,
            text="Provide customer details below",
            text_color=SUBTEXT
        ).pack(anchor="w", padx=20)

        self.form = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.form.pack(fill="both", expand=True, padx=20, pady=15)

        self.form.grid_columnconfigure(0, weight=1)
        self.form.grid_columnconfigure(1, weight=1)

        self.fields = {}

        self.combo("gender",["Male","Female"],0,0)
        self.combo("SeniorCitizen", ["0", "1"], 0, 1)
        self.combo("DeviceProtection",["Yes","No","No internet service"],1,0)
        
        self.combo("Partner",["Yes","No"],1,1)
        self.combo("TechSupport",["Yes","No","No internet service"],2,0)

        self.combo("Dependents",["Yes","No"],2,1)
        self.combo("StreamingTV",["Yes","No","No internet service"],3,0)

        self.entry("tenure",3,1)
        self.combo("StreamingMovies",["Yes","No","No internet service"],4,0)

        self.combo("PhoneService",["Yes","No"],4,1)
        self.combo("Contract",["Month-to-month","One year","Two year"],5,0)

        self.combo("MultipleLines",["Yes","No","No phone service"],5,1)
        self.combo("PaperlessBilling",["Yes","No"],6,0)

        self.combo("InternetService",["DSL","Fiber optic","No"],6,1)
        self.combo(
            "PaymentMethod",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ],
            7,0
        )

        self.combo("OnlineSecurity",["Yes","No","No internet service"],7,1)
        self.entry("MonthlyCharges",8,0)

        self.combo("OnlineBackup",["Yes","No","No internet service"],8,1)
        self.entry("TotalCharges",9,0)

        
        ctk.CTkButton(
            parent,
            text="🎯 Predict Churn",
            fg_color=PURPLE,
            hover_color="#6944F5",
            height=46,
            font=("Segoe UI",15,"bold"),
            command=self.predict
        ).pack(fill="x", padx=20, pady=(5,20))

    # ================= Right Panel =================

    def build_result(self, parent):

        top = ctk.CTkFrame(parent, fg_color="transparent")
        top.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            top,
            text="📈 Prediction Results",
            font=("Segoe UI",22,"bold")
        ).pack(side="left")

        ctk.CTkButton(
            top,
            text="↻ New Prediction",
            fg_color="transparent",
            border_width=1,
            border_color=PURPLE,
            text_color=PURPLE,command=self.reset_form
        ).pack(side="right")

        # ---------- Main Result Card ----------

        result = ctk.CTkFrame(
            parent,
            fg_color=BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=14
        )
        result.pack(fill="x", padx=20)

        left = ctk.CTkFrame(result, fg_color="transparent")
        left.pack(side="left", padx=20, pady=20)

        ctk.CTkLabel(
            left,
            text="PREDICTION",
            text_color=SUBTEXT
        ).pack(anchor="w")

        self.status = ctk.CTkLabel(
            left,
            text="Awaiting",
            text_color=TEXT,
            font=("Segoe UI",28,"bold")
        )
        self.status.pack(anchor="w")

        self.risk = ctk.CTkLabel(
            left,
            text="Risk Level: --",
            text_color=SUBTEXT
        )
        self.risk.pack(anchor="w", pady=10)

        right = ctk.CTkFrame(result, fg_color="transparent")
        right.pack(side="right", padx=25, pady=20)

        ctk.CTkLabel(
            right,
            text="CHURN PROBABILITY",
            text_color=SUBTEXT
        ).pack()

        self.prob = ctk.CTkLabel(
            right,
            text="0%",
            font=("Segoe UI",38,"bold"),
            text_color=TEXT
        )
        self.prob.pack()

        self.progress = ctk.CTkProgressBar(
            right,
            width=240,
            progress_color=RED
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

        # ---------- Gauge Placeholder ----------
        
        gauge = ctk.CTkFrame(
            parent,
            fg_color=BG,
            border_width=1,
            border_color=BORDER,
            corner_radius=14
        )
        gauge.pack(fill="x", padx=20, pady=15)

        self.gauge_frame = ctk.CTkFrame(gauge, fg_color="transparent")
        self.gauge_frame.pack(fill="both", expand=True, pady=10)

        self.draw_gauge(0)

        # ---------- Bottom Cards ----------

        bottom = ctk.CTkFrame(parent, fg_color="transparent")
        bottom.pack(fill="both", expand=True, padx=20, pady=(0,20))

        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)

        self.breakdown(bottom).grid(row=0,column=0,padx=(0,8),sticky="nsew")
        self.risk_factors(bottom).grid(row=0,column=1,padx=(8,0),sticky="nsew")

    # ================= Small Cards =================

    def breakdown(self,parent):

        card = ctk.CTkFrame(parent, fg_color=BG, corner_radius=14)

        ctk.CTkLabel(
            card,
            text="Probability Distribution",
            font=("Segoe UI",16,"bold")
        ).pack(anchor="w", padx=15, pady=(15,5))

        self.bar1 = ctk.CTkProgressBar(card, progress_color=RED)
        self.bar1.pack(fill="x", padx=15, pady=(15,8))
        self.bar1.set(0)

        self.bar2 = ctk.CTkProgressBar(card, progress_color=GREEN)
        self.bar2.pack(fill="x", padx=15, pady=(0,20))
        self.bar2.set(1)

        return card

    def risk_factors(self,parent):

        card = ctk.CTkFrame(parent, fg_color=BG, corner_radius=14)

        ctk.CTkLabel(
            card,
            text="Top Risk Factors",
            font=("Segoe UI",16,"bold")
        ).pack(anchor="w", padx=15, pady=(15,5))

        self.factor = ctk.CTkLabel(
            card,
            text="Waiting for prediction...",
            justify="left",
            wraplength=240,
            text_color=SUBTEXT
        )

        self.factor.pack(anchor="w", padx=15, pady=10)

        return card
    def draw_gauge(self, percent):

        # Remove previous gauge
        for widget in self.gauge_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(4.2,2.6), facecolor=BG)
        ax.set_facecolor(BG)

        ax.set_xlim(-1.2,1.2)
        ax.set_ylim(-0.2,1.2)
        ax.axis("off")

        # Background semicircle
        ax.add_patch(
            Wedge(
                (0,0),
                1,
                180,
                0,
                width=0.18,
                facecolor="#1C294A"
            )
        )

        # Churn arc
        angle = 180 * percent / 100

        ax.add_patch(
            Wedge(
                (0,0),
                1,
                180-angle,
                180,
                width=0.18,
                facecolor=RED
            )
        )

        # Remaining arc
        ax.add_patch(
            Wedge(
                (0,0),
                1,
                0,
                180-angle,
                width=0.18,
                facecolor=GREEN
            )
        )

        ax.text(
            0,
            0.15,
            f"{percent:.1f}%",
            ha="center",
            va="center",
            fontsize=24,
            color="white",
            fontweight="bold"
        )

        ax.text(
            0,
            -0.05,
            "Churn Probability",
            ha="center",
            fontsize=12,
            color=SUBTEXT
        )

        canvas = FigureCanvasTkAgg(fig, self.gauge_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)
    # ================= Helpers =================

    def combo(self,label,values,row,col):

        frame = ctk.CTkFrame(self.form, fg_color="transparent")
        frame.grid(row=row,column=col,padx=8,pady=6,sticky="ew")

        ctk.CTkLabel(frame,text=label).pack(anchor="w")

        box = ctk.CTkComboBox(frame, values=values)
        box.pack(fill="x")

        self.fields[label]=box

    def entry(self,label,row,col):

        frame = ctk.CTkFrame(self.form, fg_color="transparent")
        frame.grid(row=row,column=col,padx=8,pady=6,sticky="ew")

        ctk.CTkLabel(frame,text=label).pack(anchor="w")

        box = ctk.CTkEntry(frame)
        box.pack(fill="x")

        self.fields[label]=box

    def predict(self):
        try:
            customer = {}

            for key, widget in self.fields.items():
                customer[key] = widget.get()

            # Convert numeric values
            customer["SeniorCitizen"] = int(customer["SeniorCitizen"])
            customer["tenure"] = float(customer["tenure"])
            customer["MonthlyCharges"] = float(customer["MonthlyCharges"])
            customer["TotalCharges"] = float(customer["TotalCharges"])

            prediction, probability = predict_customer(customer)

            percent = probability * 100

            # Risk Level
            if percent >= 70:
                risk = "HIGH"
                color = RED
            elif percent >= 40:
                risk = "MEDIUM"
                color = "#FF9F1C"
            else:
                risk = "LOW"
                color = GREEN

            # Update UI
            self.status.configure(
                text="CHURN" if prediction else "NO CHURN",
                text_color=color
            )

            self.risk.configure(
                text=f"Risk Level: {risk}",
                text_color=color
            )

            self.prob.configure(
                text=f"{percent:.1f}%",
                text_color=color
            )

            self.progress.set(probability)
            self.bar1.set(probability)
            self.bar2.set(1 - probability)
            self.draw_gauge(percent)

            # Simple business insights
            reasons = []

            if customer["Contract"] == "Month-to-month":
                reasons.append("• Month-to-month contract")

            if customer["tenure"] < 12:
                reasons.append("• Low customer tenure")

            if customer["MonthlyCharges"] > 70:
                reasons.append("• High monthly charges")

            if customer["TechSupport"] == "No":
                reasons.append("• No tech support")

            if customer["InternetService"] == "Fiber optic":
                reasons.append("• Fiber optic users often churn more")

            if not reasons:
                reasons.append("• Customer profile looks stable")

            self.factor.configure(text="\n".join(reasons[:5]))

        except Exception as e:
            self.status.configure(text="ERROR", text_color=RED)
            self.risk.configure(text="Invalid Input")
            self.factor.configure(text=str(e))
    def reset_form(self):
        for widget in self.fields.values():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
            else:
                widget.set(widget.cget("values")[0])

        self.status.configure(text="Awaiting", text_color=TEXT)
        self.risk.configure(text="Risk Level: --", text_color=SUBTEXT)
        self.prob.configure(text="0%", text_color=TEXT)
        self.progress.set(0)
        self.bar1.set(0)
        self.bar2.set(1)
        self.factor.configure(text="Waiting for prediction...")