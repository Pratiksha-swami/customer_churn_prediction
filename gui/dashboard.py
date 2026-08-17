import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Colors ----------------
BG = "#070B1A"
CARD = "#0F1B3D"
BORDER = "#22315A"

PURPLE = "#7C5CFF"
BLUE = "#4F8CFF"
GREEN = "#3CCB5A"
RED = "#FF4D6D"
ORANGE = "#FF9F1C"

TEXT = "#FFFFFF"
SUBTEXT = "#9AA4C7"


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent, fg_color=BG)

        self.df = pd.read_csv("dataset/churn_clean.csv")
        # self.df["Churn"] = self.df["Churn"].replace({"Yes":1,"No":0})
        # self.df["Churn"] = (
        #         self.df["Churn"]
        #         .map({"Yes": 1, "No": 0})
        #         .astype(int)
        #     )
        self.build_ui()

    def load_charts(self):

        df = self.df

        # ---------------- Chart 1 ----------------
        fig, ax = plt.subplots(figsize=(3,3), facecolor="#070B1A")

        values = df["Churn"].value_counts().sort_index()

        def fmt(pct):
            total = values.sum()
            return f"{int(pct*total/100)}\n({pct:.1f}%)"

        ax.pie(
            values,
            labels=["No Churn","Churn"],
            colors=["#3CCB5A","#FF4D6D"],
            startangle=90,
            wedgeprops=dict(width=0.42),
            autopct=fmt,
            pctdistance=0.8,
            textprops={"color":"white","fontsize":9}
        )

        ax.text(
            0,0,
            f"{values[1]/values.sum()*100:.1f}%",
            ha="center",
            va="center",
            color="white",
            fontsize=18,
            fontweight="bold"
        )

        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[0])

        # ---------------- Chart 2 ----------------
        fig, ax = plt.subplots(figsize=(3.4,3), facecolor="#070B1A")

        contract = pd.crosstab(df["Contract"], df["Churn"])

        contract.plot(
            kind="bar",
            ax=ax,
            color=["#3CCB5A","#FF4D6D"]
        )

        for c in ax.containers:
            ax.bar_label(c, fontsize=8, color="white")

        ax.set_ylabel("Customers")
        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[1])

        # ---------------- Chart 3 ----------------
        fig, ax = plt.subplots(figsize=(3.2,3), facecolor="#070B1A")

        bp = ax.boxplot(
            [
                df[df["Churn"]==1]["tenure"],
                df[df["Churn"]==0]["tenure"]
            ],
            patch_artist=True
        )

        bp["boxes"][0].set_facecolor("#FF4D6D")
        bp["boxes"][1].set_facecolor("#3CCB5A")

        ax.set_xticklabels(["Churn","Not Churn"])
        ax.set_ylabel("Months")

        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[2])

        # ---------------- Chart 4 ----------------
        fig, ax = plt.subplots(figsize=(3.3,3), facecolor="#070B1A")

        ax.hist(
            df[df["Churn"]==1]["MonthlyCharges"],
            bins=25,
            density=True,
            alpha=.5,
            color="#FF4D6D",
            label="Churned"
        )

        ax.hist(
            df[df["Churn"]==0]["MonthlyCharges"],
            bins=25,
            density=True,
            alpha=.5,
            color="#3CCB5A",
            label="Not Churned"
        )

        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[3])

        # ---------------- Chart 5 ----------------
        fig, ax = plt.subplots(figsize=(3.3,3), facecolor="#070B1A")

        payment = pd.crosstab(
            df["PaymentMethod"],
            df["Churn"],
            normalize="index"
        )*100

        payment.plot(
            kind="barh",
            stacked=True,
            ax=ax,
            color=["#3CCB5A","#FF4D6D"]
        )

        for c in ax.containers:
            ax.bar_label(
                c,
                label_type="center",
                fmt="%.1f%%",
                fontsize=7,
                color="white"
            )

        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[4])

        # ---------------- Chart 6 ----------------
        fig, ax = plt.subplots(figsize=(3.2,3), facecolor="#070B1A")

        internet = df.groupby("InternetService")["Churn"].mean()*100

        bars = ax.bar(
            internet.index,
            internet.values,
            color=PURPLE
        )

        for b in bars:
            ax.text(
                b.get_x()+b.get_width()/2,
                b.get_height()+1,
                f"{b.get_height():.1f}%",
                ha="center",
                color="white"
            )

        ax.set_ylabel("Churn %")

        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[5])

        # ---------------- Chart 7 ----------------
        fig, ax = plt.subplots(figsize=(3,3), facecolor="#070B1A")

        gender = (
            df.groupby("gender")["Churn"]
            .mean()
            .astype(float) * 100
        )

        ax.pie(
            gender.to_numpy(dtype=float),
            labels=gender.index.tolist(),
            colors=["#4F8CFF", "#FF4D6D"],
            startangle=90,
            wedgeprops=dict(width=0.38),
            autopct="%1.1f%%",
            textprops={"color": "white", "fontsize": 9}
        )

        ax.text(
            0, 0,
            "Gender",
            ha="center",
            color="white",
            fontsize=16
        )

        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[6])

        # ---------------- Chart 8 ----------------
        fig, ax = plt.subplots(figsize=(3,3), facecolor="#070B1A")

        senior = (
            df.groupby("SeniorCitizen")["Churn"]
            .mean()
            .astype(float) * 100
        )
        ax.pie(
            senior.to_numpy(dtype=float),
            labels=["No", "Yes"],
            colors=["#3CCB5A", "#FF9F1C"],
            startangle=90,
            wedgeprops=dict(width=0.38),
            autopct="%1.1f%%",
            textprops={"color": "white", "fontsize": 9}
        )
        ax.text(
            0,0,
            "Senior",
            ha="center",
            color="white",
            fontsize=16
        )

        self.style_axes(ax)
        self.add_canvas(fig,self.chart_frames[7])
        
    def style_axes(self, ax):
        ax.set_facecolor("#0F1B3D")
        for spine in ax.spines.values():
            spine.set_color("#22315A")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        legend = ax.get_legend()
        if legend:
            legend.get_frame().set_facecolor("#0F1B3D")
            legend.get_frame().set_edgecolor("#22315A")
            for t in legend.get_texts():
                t.set_color("white")


    def add_canvas(self, fig, frame):
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
        
    def build_ui(self):

        # ================= Header =================

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20,15))

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(
            left,
            text="Dashboard",
            font=("Segoe UI",30,"bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Overview of customer churn analytics",
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
        ).pack(side="left", padx=10)

        

        # ================= KPI Cards =================

        total = len(self.df)
        churned = self.df["Churn"].sum()
        retained = total - churned
        rate = churned/total*100
        avg_monthly = self.df["MonthlyCharges"].mean()
        avg_tenure = self.df["tenure"].mean()

        kpi_frame = ctk.CTkFrame(self, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=20)

        for i in range(6):
            kpi_frame.grid_columnconfigure(i, weight=1)

        data = [
            ("👥","Total Customers",f"{total:,}","100%",BLUE),
            ("❌","Churned Customers",f"{churned:,}",f"{rate:.1f}%",RED),
            ("✔","Retained Customers",f"{retained:,}",f"{100-rate:.1f}%",GREEN),
            ("📈","Churn Rate",f"{rate:.1f}%","Overall",ORANGE),
            ("💲","Avg Monthly Charges",f"₹ {avg_monthly:.2f}","Per Customer",BLUE),
            ("📅","Avg Tenure",f"{avg_tenure:.1f}","Months",PURPLE)
        ]

        for i,item in enumerate(data):
            self.kpi_card(kpi_frame,*item).grid(
                row=0,column=i,padx=6,sticky="ew"
            )

        # ================= Charts =================

        charts = ctk.CTkFrame(self, fg_color="transparent")
        charts.pack(fill="both", expand=True, padx=20, pady=15)

        for i in range(4):
            charts.grid_columnconfigure(i, weight=1)

        for r in range(2):
            charts.grid_rowconfigure(r, weight=1)

        titles = [
            "Churn Distribution",
            "Contract Type vs Churn",
            "Tenure vs Churn",
            "Monthly Charges vs Churn",
            "Payment Method vs Churn",
            "Churn by Internet Service",
            "Churn by Gender",
            "Churn by Senior Citizen"
        ]

        self.chart_frames = []

        for i,title in enumerate(titles):

            card = ctk.CTkFrame(
                charts,
                fg_color=CARD,
                border_width=1,
                border_color=BORDER,
                corner_radius=16
            )

            card.grid(
                row=i//4,
                column=i%4,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=("Segoe UI",16,"bold")
            ).pack(anchor="w", padx=15, pady=(12,6))

            frame = ctk.CTkFrame(card, fg_color="transparent")
            frame.pack(fill="both", expand=True, padx=8, pady=(0,8))

            self.chart_frames.append(frame)

        # ================= Bottom =================

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x", padx=20, pady=(0,20))

        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)

        self.analysis_panel(bottom).grid(
            row=0,column=0,padx=(0,8),sticky="nsew"
        )

        self.activity_panel(bottom).grid(
            row=0,column=1,sticky="nsew"
        )
        self.load_charts()
    # ---------- KPI Card ----------

    def kpi_card(self,parent,icon,title,value,subtitle,color):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16,
            height=105
        )

        card.grid_propagate(False)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=12, pady=(10,0))

        circle = ctk.CTkFrame(
            top,
            width=42,
            height=42,
            corner_radius=21,
            fg_color=color
        )
        circle.pack(side="left")
        circle.pack_propagate(False)

        ctk.CTkLabel(
            circle,
            text=icon,
            font=("Segoe UI",18)
        ).place(relx=0.5,rely=0.5,anchor="center")

        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="both", padx=12)

        ctk.CTkLabel(
            body,
            text=title,
            font=("Segoe UI",12),
            text_color=SUBTEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            body,
            text=value,
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            body,
            text=subtitle,
            font=("Segoe UI",11),
            text_color=SUBTEXT
        ).pack(anchor="w")

        return card

    # ---------- Analysis ----------

    def analysis_panel(self,parent):

        panel = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )

        ctk.CTkLabel(
            panel,
            text="Analysis & Insights",
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w", padx=15, pady=(12,10))

        grid = ctk.CTkFrame(panel, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=10, pady=(0,10))

        for i in range(4):
            grid.grid_columnconfigure(i, weight=1)

        insights = [
            ("🔴","Top Risk","Month-to-month contracts"),
            ("🟠","High Risk","High charges + low tenure"),
            ("🟢","Opportunity","Long-term contracts"),
            ("💡","Key Insight","Fiber users churn more")
        ]

        for i,(icon,title,text) in enumerate(insights):

            box = ctk.CTkFrame(
                grid,
                fg_color=BG,
                corner_radius=12
            )

            box.grid(row=0,column=i,padx=5,sticky="nsew")

            ctk.CTkLabel(
                box,
                text=icon,
                font=("Segoe UI",24)
            ).pack(pady=(12,6))

            ctk.CTkLabel(
                box,
                text=title,
                font=("Segoe UI",13,"bold")
            ).pack()

            ctk.CTkLabel(
                box,
                text=text,
                wraplength=120,
                text_color=SUBTEXT,
                font=("Segoe UI",11)
            ).pack(pady=(4,12))

        return panel

    # ---------- Activities ----------

    def activity_panel(self,parent):

        panel = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )

        ctk.CTkLabel(
            panel,
            text="Recent Activities",
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w", padx=15, pady=(12,10))

        items = [
            ("🟢","New prediction made","10:32 AM"),
            ("🔵","EDA chart generated","10:15 AM"),
            ("🟣","Report exported","Yesterday")
        ]

        for icon,title,time in items:

            row = ctk.CTkFrame(panel, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=8)

            ctk.CTkLabel(
                row,
                text=icon,
                font=("Segoe UI",16)
            ).pack(side="left")

            txt = ctk.CTkFrame(row, fg_color="transparent")
            txt.pack(side="left", padx=8)

            ctk.CTkLabel(
                txt,
                text=title,
                font=("Segoe UI",12,"bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                txt,
                text=time,
                font=("Segoe UI",11),
                text_color=SUBTEXT
            ).pack(anchor="w")

            
        return panel