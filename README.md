# 🧮 Inventory (M, N) Policy Simulator  
### A probabilistic inventory simulation model built with Python + Streamlit

This project implements the **probabilistic inventory system** from a Prescriptive Analytics graduate-level assignment.  
The system follows a **periodic review (M, N) policy**, with **stochastic daily demand** and **stochastic supplier lead time**, using a full **Monte Carlo simulation**.

The app allows you to:

- ✔ Simulate the **four preset policies** (A–D) from the assignment  
- ✔ Define **custom values** for M, N and cost parameters  
- ✔ Visualize **daily inventory behavior**, costs, and review events  
- ✔ Compare policies using **summary tables** and **interactive charts**  
- ✔ Run everything through a clean **Streamlit web interface**  

The project is fully modular, production-style, and uses a clean architecture separating simulation logic and UI.

Project link on Streamlit: https://inventory-simulator.streamlit.app

---

## 📁 Project Structure


```text
inventory_sim/
│
├── app.py                        # Main landing page for Streamlit
├── simulation.py                 # Core Monte Carlo simulation engine
├── config.py                     # Default distributions, costs, preset policies
├── pages/
│     ├── 01_preset_policies.py   # Page: Simulation of Policies A–D
│     ├── 02_custom_policy.py     # Page: Custom (M, N) policy
│     └── 03_summary.py           # Page: Summary + charts comparing all policies
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation                
