import customtkinter as ctk

BG = "#070B1A"
CARD = "#0F1B3D"
BORDER = "#22315A"
PURPLE = "#7C5CFF"
TEXT = "#FFFFFF"
SUBTEXT = "#9AA4C7"

class ModelInfoPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color=BG)
        self.build_ui()

    def build_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20,15))

        ctk.CTkLabel(
            header,
            text="Model Information",
            font=("Segoe UI",30,"bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Machine Learning model details used for customer churn prediction",
            font=("Segoe UI",13),
            text_color=SUBTEXT
        ).pack(anchor="w")

        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=(0,20))

        self.card(content, "Model Used", [
            "Algorithm: XGBoost Classifier",
            "Problem Type: Binary Classification",
            "Target Variable: Churn (Yes/No)",
            "Model File: final_churn_model.pkl"
        ])

        self.card(content, "Model Performance", [
            "Accuracy: 82%",
            "Cross Validation Score: 84%",
            "Precision: Good",
            "Recall: Optimized for churn detection"
        ])

        self.card(content, "Dataset Information", [
            "Dataset: IBM Telco Customer Churn",
            "Records: 7,032 customers",
            "Original Features: 20",
            "Final Model Features: 30"
        ])

        self.card(content, "Feature Engineering", [
            "Scaled Features:",
            "• Tenure",
            "• MonthlyCharges",
            "• TotalCharges",
            "",
            "One-Hot Encoded Features:",
            "• Gender",
            "• Contract",
            "• Internet Service",
            "• Payment Method",
            "• Multiple Lines",
            "• Security & Streaming Services"
        ])

        self.card(content, "Preprocessing Pipeline", [
            "1. Data Cleaning",
            "2. Missing Value Handling",
            "3. Binary Encoding",
            "4. One-Hot Encoding",
            "5. Feature Scaling",
            "6. XGBoost Prediction"
        ])

        self.card(content, "Why XGBoost?", [
            "• Highest cross-validation score",
            "• Excellent performance on tabular data",
            "• Handles feature interactions effectively",
            "• Reduces overfitting through regularization",
            "• Fast and reliable predictions"
        ])

    def card(self, parent, title, lines):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )
        card.pack(fill="x", pady=12)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI",20,"bold")
        ).pack(anchor="w", padx=20, pady=(18,10))

        for line in lines:
            ctk.CTkLabel(
                card,
                text=line,
                font=("Segoe UI",13),
                text_color=SUBTEXT,
                anchor="w",
                justify="left"
            ).pack(anchor="w", padx=25, pady=2)

        ctk.CTkFrame(card, fg_color="transparent", height=10).pack()