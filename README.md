# 💳 Digital Wallet & Payment Management System (`digital-wallet-dbms`)

Enterprise-grade **Database Management System (DBMS)** web application built with **Python, Streamlit, Plotly, and MySQL 8.0** (with automatic **Cloud SQLite Mirror** fallback for **Streamlit Community Cloud** deployment).

## ✨ Key Features
- **Dual-Engine Hybrid Architecture (`db_connector.py`)**:
  - **Local Mode**: Connects directly to live **MySQL 8.0** (`localhost:3306`, `wallet` database) so all changes synchronize in real time with **MySQL Workbench**.
  - **Streamlit Community Cloud Mode**: Automatically initializes a complete cloud SQL mirror seeded with all **13 tables, 60+ transactions, 3 Views, 3 Triggers, 4 Stored Functions, and 2 Cursor Stored Procedures** so anyone visiting your public Streamlit Cloud link can test every User and Admin feature live!
- **Dual-Theme High-Contrast UI**: Instant toggle between **Dark Mode (Obsidian)** and **Light Mode (Crisp Alabaster)**.
- **Role-Based Portals**:
  - **User Portal (`aarav.sharma@example.com` / `hash_demo_01`)**: Live wallet balance, instant P2P transfers, bank account linking & deposits, utility bill payments with automated cashback (`fn_calculate_cashback`), and interactive Plotly charts.
  - **Admin Console (`karan.verma@example.com` / `hash_demo_09`)**: Master Data Grid CRUD for all 13 tables, live Schema & Index Inspector, Stored Procedures (`sp_total_balance`, `sp_bonus_active_wallets`) & Triggers testing hub, Interactive SQL Console, and Audit Trail viewer.

## 🚀 Quick Start (Local MySQL + Streamlit)
```bash
pip install -r requirements.txt
streamlit run app.py
```
