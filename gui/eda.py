import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#-----------colors-------

BG = "#070B1A"
CARD = "#0F1B3D"
BORDER = "#22315A"
PURPLE = "#7C5CFF"
BLUE = "#4F8CFF"
GREEN = "#3CCB5A"
RED = "#FF4D6D"
ORANGE = "#FF9F1C"
SUBTEXT = "#9AA4C7"

class EDAPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,fg_color=BG)

        self.df=pd.read_csv("dataset/churn_clean.csv")
        

        self.build_ui()
        self.update_chart()

    def build_ui(self):

        header=ctk.CTkFrame(self,fg_color="transparent")
        header.pack(fill="x",padx=25,pady=(20,15))

        left=ctk.CTkFrame(header,fg_color="transparent")
        left.pack(side="left")

        ctk.CTkLabel(left,text="EDA Explorer",
                     font=("Segoe UI",30,"bold")).pack(anchor="w")

        ctk.CTkLabel(left,text="Explore customer churn interactively",
                     text_color=SUBTEXT).pack(anchor="w")

        
        control=ctk.CTkFrame(self,fg_color=CARD,border_width=1,border_color=BORDER,corner_radius=16)
        control.pack(fill="x",padx=20)

        ctk.CTkLabel(
            control,
            text="Select Feature",
            font=("Segoe UI",14,"bold")
        ).grid(row=0,column=0,padx=20,pady=15)

        features=[c for c in self.df.columns if c!="customerID"]

        self.feature_box=ctk.CTkComboBox(control,values=features,width=220,command=lambda _:self.update_chart())

        self.feature_box.set("Contract")
        self.feature_box.grid(row=0,column=1,padx=10)

        # ---------- Main Body ----------
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=15)

        body.grid_columnconfigure(0,weight=3)
        body.grid_columnconfigure(1,weight=1)

        # chart 
        chart_card=ctk.CTkFrame(body,fg_color=CARD,border_color=BORDER,border_width=1,corner_radius=16)
        chart_card.grid(row=0,column=0,sticky="nsew",padx=(0,10))

        ctk.CTkLabel(
                    chart_card,
                    text="Visualization",
                    font=("Segoe UI",18,"bold")
                ).pack(anchor="w", padx=15, pady=(12,5))

        self.chart_frame = ctk.CTkFrame(chart_card, fg_color="transparent")
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Right Panel
        right = ctk.CTkFrame(body, fg_color="transparent")
        right.grid(row=0,column=1,sticky="nsew")

        self.stats_card(right)
        self.insight_card(right)
        # ================= Right Panel =================

    def stats_card(self,parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )

        card.pack(fill="x")

        ctk.CTkLabel(
            card,
            text="Statistics",
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w", padx=15, pady=(12,10))

        self.stat1 = ctk.CTkLabel(card,text="—")
        self.stat1.pack(anchor="w", padx=15)

        self.stat2 = ctk.CTkLabel(card,text="—")
        self.stat2.pack(anchor="w", padx=15, pady=(5,0))

        self.stat3 = ctk.CTkLabel(card,text="—")
        self.stat3.pack(anchor="w", padx=15, pady=(5,15))

    def insight_card(self,parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=16
        )
        card.pack(fill="x", pady=15)

        ctk.CTkLabel(
            card,
            text="Business Insight",
            font=("Segoe UI",18,"bold")
        ).pack(anchor="w", padx=15, pady=(12,10))

        self.insight = ctk.CTkLabel(
            card,
            text="Select a feature.",
            justify="left",
            wraplength=220,
            text_color=SUBTEXT
        )

        self.insight.pack(anchor="w", padx=15, pady=(0,15))

    def update_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        feature = self.feature_box.get()

        fig, ax = plt.subplots(figsize=(6,5), facecolor=BG)

        # ---------- Numerical ----------
        if feature in ["tenure","MonthlyCharges","TotalCharges"]:

            if feature == "tenure":
                bp = ax.boxplot(
                    [
                        self.df[self.df["Churn"]==0][feature],
                        self.df[self.df["Churn"]==1][feature]
                    ],
                    patch_artist=True
                )

                bp["boxes"][0].set_facecolor(GREEN)
                bp["boxes"][1].set_facecolor(RED)

                ax.set_xticklabels(["No Churn","Churn"])

            else:

                ax.hist(
                    self.df[self.df["Churn"]==0][feature],
                    bins=25,
                    alpha=.6,
                    color=GREEN,
                    label="No Churn"
                )

                ax.hist(
                    self.df[self.df["Churn"]==1][feature],
                    bins=25,
                    alpha=.6,
                    color=RED,
                    label="Churn"
                )

                ax.legend()
            self.stat1.configure(text=f"Mean : {self.df[feature].mean():.2f}")
            self.stat2.configure(text=f"Median : {self.df[feature].median():.2f}")
            self.stat3.configure(text=f"Max : {self.df[feature].max():.2f}")

            self.insight.configure(
                text=f"Average {feature} is {self.df[feature].mean():.2f}."
            )

        # ---------- Categorical ----------
        else:

            values = self.df.groupby(feature)["Churn"].mean()*100

            if len(values) <= 3:

                ax.pie(
                    values.values,
                    labels=values.index.astype(str),
                    colors=[BLUE,GREEN,ORANGE][:len(values)],
                    autopct="%1.1f%%",
                    startangle=90,
                    wedgeprops=dict(width=.40),
                    textprops={"color":"white"}
                )

                ax.text(
                    0,0,
                    feature,
                    ha="center",
                    color="white",
                    fontsize=16
                )

            else:

                bars = ax.barh(
                    values.index.astype(str),
                    values.values,
                    color=PURPLE
                )

                for b in bars:

                    ax.text(
                        b.get_width()+1,
                        b.get_y()+b.get_height()/2,
                        f"{b.get_width():.1f}%",
                        va="center",
                        color="white"
                    )

            self.stat1.configure(text=f"Categories : {len(values)}")
            self.stat2.configure(
                text=f"Highest : {values.idxmax()} ({values.max():.1f}%)"
            )
            self.stat3.configure(
                text=f"Lowest : {values.idxmin()} ({values.min():.1f}%)"
            )

            self.insight.configure(
                text=f"{values.idxmax()} has the highest churn ({values.max():.1f}%)."
            )

        # ---------- Style ----------
        ax.set_facecolor(BG)

        for spine in ax.spines.values():
            spine.set_color(BORDER)

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")

        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)
