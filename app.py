import customtkinter as ctk
import matplotlib.pyplot as plt

from gui.sidebar import Sidebar
from gui.dashboard import DashboardPage
from gui.prediction import PredictionPage
from gui.model_info import ModelInfoPage
from gui.eda import EDAPage

# ---------------- Theme ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#070B1A"

# ---------------- Main Window ----------------
root = ctk.CTk()
root.title("ChurnSight - Customer Churn Analytics")
root.geometry("1440x900")
root.minsize(1200, 700)
root.configure(fg_color=BG)

# ---------------- Content Container ----------------
content = ctk.CTkFrame(root, fg_color=BG)
content.pack(side="right", fill="both", expand=True)

# ---------------- Create Pages ----------------
dashboard_page = DashboardPage(content)
prediction_page = PredictionPage(content)
model_info_page = ModelInfoPage(content)
eda_page = EDAPage(content)

pages = {
    "Dashboard": dashboard_page,
    "Churn Prediction": prediction_page,
    "EDA Explorer": eda_page,
    "model": model_info_page
}

# Stack all pages
for page in pages.values():
    page.place(relx=0, rely=0, relwidth=1, relheight=1)

# ---------------- Navigation ----------------
def show_page(page_name):
    pages[page_name].lift()
    sidebar.set_active(page_name)

# ---------------- Sidebar ----------------
sidebar = Sidebar(root, show_page)
sidebar.pack(side="left", fill="y")

# ---------------- Close App ----------------
def close_app():
    plt.close("all")
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)
sidebar.logout.configure(command=close_app)

# ---------------- Default Page ----------------
show_page("Dashboard")

root.mainloop()