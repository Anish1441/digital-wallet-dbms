"""
Database Connector Module for Digital Wallet & Payment Management System
Dual-Engine Hybrid Architecture:
1. Primary Engine: Live MySQL 8.0 (localhost:3306 or cloud MySQL via env/secrets)
2. Cloud Fallback Engine: Automatic SQLite Mirror (wallet_cloud.db) for Streamlit Community Cloud
   so the deployed web app works 100% seamlessly when shared with friends without requiring
   access to your local laptop's localhost:3306 MySQL server.
"""

import os
import re
import json
import sqlite3
import tempfile
import datetime
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    HAS_MYSQL_DRIVER = True
except ImportError:
    HAS_MYSQL_DRIVER = False
    MySQLError = Exception


def _adapt_mysql_to_sqlite_sql(query: str) -> str:
    """Adapts MySQL query syntax to SQLite."""
    q = query.replace("%s", "?")
    q = re.sub(r"\bNOW\(\)", "datetime('now', 'localtime')", q, flags=re.IGNORECASE)
    q = re.sub(r"\bTRUE\b", "1", q, flags=re.IGNORECASE)
    q = re.sub(r"\bFALSE\b", "0", q, flags=re.IGNORECASE)
    return q


def _adapt_mysql_params(params: Optional[Tuple]) -> Tuple:
    if not params:
        return ()
    adapted = []
    for p in params:
        if isinstance(p, Decimal):
            adapted.append(float(p))
        elif isinstance(p, bool):
            adapted.append(1 if p else 0)
        else:
            adapted.append(p)
    return tuple(adapted)


class CompatSQLiteCursor(sqlite3.Cursor):
    """SQLite Cursor subclass that transparently accepts MySQL %s syntax and Decimal params."""

    def execute(self, sql: str, parameters: Any = ()):
        adapted_sql = _adapt_mysql_to_sqlite_sql(sql)
        adapted_params = _adapt_mysql_params(tuple(parameters) if parameters else ())
        return super().execute(adapted_sql, adapted_params)


class CompatSQLiteConnection(sqlite3.Connection):
    """SQLite Connection subclass that returns CompatSQLiteCursor by default."""

    def cursor(self, factory=CompatSQLiteCursor, **kwargs):
        return super().cursor(CompatSQLiteCursor)


class WalletDBConnector:
    """
    Hybrid connector class to manage MySQL 8.0 operations locally and automatically
    fall back to a full-featured SQLite mirror when deployed on Streamlit Community Cloud.
    """

    _sqlite_initialized = False

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ):
        self.host = host or os.environ.get("MYSQL_HOST", "localhost")
        self.port = int(port or os.environ.get("MYSQL_PORT", 3306))
        self.user = user or os.environ.get("MYSQL_USER", "root")
        self.password = password or self._read_local_password()
        self.database = database or os.environ.get("MYSQL_DATABASE", "wallet")
        self.conn = None
        self.engine = "mysql"  # "mysql" or "sqlite"
        self.sqlite_path = os.path.join(tempfile.gettempdir(), "wallet_cloud_mirror.db")

    @staticmethod
    def _read_local_password() -> str:
        """Password comes from env var or .streamlit/secrets.toml ([mysql] password) - never hardcoded."""
        pw = os.environ.get("MYSQL_PASSWORD")
        if pw:
            return pw
        try:
            import streamlit as st
            return str(st.secrets["mysql"]["password"])
        except Exception:
            return ""

    def connect(self):
        """Attempts connection to MySQL first; falls back to SQLite mirror on Cloud."""
        if HAS_MYSQL_DRIVER:
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    autocommit=False,
                    connection_timeout=2,
                )
                self.engine = "mysql"
                return self.conn
            except Exception:
                pass

        # Fallback to Cloud SQLite Engine
        self.engine = "sqlite"
        self._ensure_sqlite_initialized()
        self.conn = sqlite3.connect(
            self.sqlite_path,
            check_same_thread=False,
            factory=CompatSQLiteConnection,
        )
        self.conn.row_factory = sqlite3.Row
        self._register_sqlite_functions(self.conn)
        return self.conn

    def _register_sqlite_functions(self, conn: sqlite3.Connection):
        """Registers MySQL-compatible scalar functions inside SQLite."""
        conn.create_function("NOW", 0, lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        def _json_object(*args):
            d = {}
            for i in range(0, len(args) - 1, 2):
                val = float(args[i + 1]) if isinstance(args[i + 1], Decimal) else args[i + 1]
                d[str(args[i])] = val
            return json.dumps(d)

        conn.create_function("JSON_OBJECT", -1, _json_object)
        conn.create_function("fn_get_wallet_balance", 1, lambda uid: float(self._sqlite_fn_get_wallet_balance(uid)))
        conn.create_function("fn_total_successful_spend", 1, lambda wid: float(self._sqlite_fn_total_successful_spend(wid)))
        conn.create_function("fn_total_due_bills", 1, lambda uid: float(self._sqlite_fn_total_due_bills(uid)))
        conn.create_function("fn_calculate_cashback", 2, lambda amt, oid: float(self._sqlite_fn_calculate_cashback(amt, oid)))

    def _ensure_sqlite_initialized(self):
        """Seeds the cloud SQLite database from Users_table.sql if not yet created."""
        if WalletDBConnector._sqlite_initialized and os.path.exists(self.sqlite_path):
            return

        conn = sqlite3.connect(self.sqlite_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USERS';")
        if cur.fetchone() is not None:
            conn.close()
            WalletDBConnector._sqlite_initialized = True
            return

        # Create all 13 tables in SQLite compatible syntax
        schema_sql = """
        CREATE TABLE IF NOT EXISTS USERS (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            app_role TEXT NOT NULL DEFAULT 'USER',
            kyc_status TEXT NOT NULL DEFAULT 'PENDING',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS WALLETS (
            wallet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            balance NUMERIC NOT NULL DEFAULT 0.00,
            currency TEXT NOT NULL DEFAULT 'INR',
            daily_limit NUMERIC NOT NULL DEFAULT 10000.00,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS BANK_ACCOUNTS (
            bank_account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            bank_name TEXT NOT NULL,
            account_no_masked TEXT NOT NULL,
            ifsc_code TEXT NOT NULL,
            account_type TEXT NOT NULL,
            is_verified INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS MERCHANT_CATEGORIES (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS MERCHANTS (
            merchant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            business_name TEXT NOT NULL,
            merchant_code TEXT NOT NULL UNIQUE,
            contact_phone TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES MERCHANT_CATEGORIES(category_id)
        );

        CREATE TABLE IF NOT EXISTS BILLERS (
            biller_id INTEGER PRIMARY KEY AUTOINCREMENT,
            biller_name TEXT NOT NULL UNIQUE,
            biller_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS USER_BILLERS (
            user_biller_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            biller_id INTEGER NOT NULL,
            consumer_number TEXT NOT NULL,
            nickname TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (biller_id, consumer_number),
            FOREIGN KEY (user_id) REFERENCES USERS(user_id),
            FOREIGN KEY (biller_id) REFERENCES BILLERS(biller_id)
        );

        CREATE TABLE IF NOT EXISTS BILLS (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_biller_id INTEGER NOT NULL,
            billing_period TEXT NOT NULL,
            amount_due NUMERIC NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'UNPAID',
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (user_biller_id, billing_period),
            FOREIGN KEY (user_biller_id) REFERENCES USER_BILLERS(user_biller_id)
        );

        CREATE TABLE IF NOT EXISTS TRANSACTIONS (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference_no TEXT NOT NULL UNIQUE,
            sender_wallet_id INTEGER NULL,
            receiver_wallet_id INTEGER NULL,
            merchant_id INTEGER NULL,
            bank_account_id INTEGER NULL,
            amount NUMERIC NOT NULL,
            transaction_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            description TEXT,
            initiated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL
        );

        CREATE TABLE IF NOT EXISTS BILL_PAYMENTS (
            bill_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER NOT NULL UNIQUE,
            transaction_id INTEGER NOT NULL UNIQUE,
            amount_paid NUMERIC NOT NULL,
            paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS CASHBACK_OFFERS (
            offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchant_id INTEGER NULL,
            offer_name TEXT NOT NULL,
            promo_code TEXT UNIQUE,
            minimum_amount NUMERIC NOT NULL DEFAULT 0.00,
            cashback_percentage NUMERIC NOT NULL,
            max_cashback NUMERIC NOT NULL,
            start_at TEXT NOT NULL,
            end_at TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS CASHBACK_HISTORY (
            cashback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source_transaction_id INTEGER NOT NULL UNIQUE,
            offer_id INTEGER NULL,
            amount NUMERIC NOT NULL,
            credited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS AUDIT_LOGS (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_user_id INTEGER NULL,
            action_type TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id INTEGER NULL,
            details TEXT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.executescript(schema_sql)

        def _json_obj(*args):
            d = {}
            for i in range(0, len(args) - 1, 2):
                d[str(args[i])] = args[i + 1]
            return json.dumps(d)

        conn.create_function("JSON_OBJECT", -1, _json_obj)

        # Parse INSERT statements from Users_table.sql
        sql_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Users_table.sql")
        if os.path.exists(sql_file):
            with open(sql_file, "r", encoding="utf-8") as f:
                raw_sql = f.read()
            inserts = re.findall(r"(INSERT\s+INTO\s+\w+.*?;)", raw_sql, flags=re.DOTALL | re.IGNORECASE)
            for ins in inserts:
                clean_ins = re.sub(r"\bTRUE\b", "1", ins, flags=re.IGNORECASE)
                clean_ins = re.sub(r"\bFALSE\b", "0", clean_ins, flags=re.IGNORECASE)
                try:
                    cur.execute(clean_ins)
                except Exception:
                    pass

        # Create Views & Triggers in SQLite
        views_and_triggers = """
        CREATE VIEW IF NOT EXISTS vw_user_wallet_summary AS
        SELECT u.user_id, u.full_name, u.email, u.phone, u.kyc_status, u.is_active AS user_active,
               w.wallet_id, w.balance, w.currency, w.daily_limit, w.status AS wallet_status
        FROM USERS u LEFT JOIN WALLETS w ON u.user_id = w.user_id;

        CREATE VIEW IF NOT EXISTS vw_transaction_details AS
        SELECT t.transaction_id, t.reference_no, t.transaction_type, t.amount, t.status,
               t.sender_wallet_id, su.full_name AS sender_name,
               t.receiver_wallet_id, ru.full_name AS receiver_name,
               t.merchant_id, m.business_name AS merchant_name,
               t.bank_account_id, ba.bank_name, ba.account_no_masked,
               t.description, t.initiated_at, t.completed_at
        FROM TRANSACTIONS t
        LEFT JOIN WALLETS sw ON t.sender_wallet_id = sw.wallet_id
        LEFT JOIN USERS su ON sw.user_id = su.user_id
        LEFT JOIN WALLETS rw ON t.receiver_wallet_id = rw.wallet_id
        LEFT JOIN USERS ru ON rw.user_id = ru.user_id
        LEFT JOIN MERCHANTS m ON t.merchant_id = m.merchant_id
        LEFT JOIN BANK_ACCOUNTS ba ON t.bank_account_id = ba.bank_account_id;

        CREATE VIEW IF NOT EXISTS vw_due_bills AS
        SELECT b.bill_id, u.user_id, u.full_name, bl.biller_name, bl.biller_type,
               ub.consumer_number, ub.nickname, b.billing_period, b.amount_due, b.due_date, b.status
        FROM BILLS b
        INNER JOIN USER_BILLERS ub ON b.user_biller_id = ub.user_biller_id
        INNER JOIN USERS u ON ub.user_id = u.user_id
        INNER JOIN BILLERS bl ON ub.biller_id = bl.biller_id
        WHERE b.status IN ('UNPAID', 'OVERDUE');

        CREATE TRIGGER IF NOT EXISTS trg_after_user_insert
        AFTER INSERT ON USERS
        FOR EACH ROW
        BEGIN
            INSERT INTO WALLETS (user_id, balance, currency, daily_limit, status)
            VALUES (NEW.user_id, 0.00, 'INR', 5000.00, 'ACTIVE');
        END;

        CREATE TRIGGER IF NOT EXISTS trg_after_wallet_update
        AFTER UPDATE ON WALLETS
        FOR EACH ROW
        WHEN OLD.status <> NEW.status
        BEGIN
            INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details)
            VALUES (
                NULL,
                'WALLET_STATUS_CHANGE',
                'WALLET',
                NEW.wallet_id,
                '{"old_status": "' || OLD.status || '", "new_status": "' || NEW.status || '"}'
            );
        END;

        CREATE TRIGGER IF NOT EXISTS trg_after_bank_delete
        AFTER DELETE ON BANK_ACCOUNTS
        FOR EACH ROW
        BEGIN
            INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details)
            VALUES (
                OLD.user_id,
                'BANK_ACCOUNT_DELETED',
                'BANK_ACCOUNT',
                OLD.bank_account_id,
                '{"bank_name": "' || OLD.bank_name || '", "account_no_masked": "' || OLD.account_no_masked || '"}'
            );
        END;
        """
        cur.executescript(views_and_triggers)
        conn.commit()
        conn.close()
        WalletDBConnector._sqlite_initialized = True

    def close(self):
        """Closes the active database connection."""
        if self.conn:
            try:
                if self.engine == "mysql":
                    if self.conn.is_connected():
                        self.conn.close()
                else:
                    self.conn.close()
            except Exception:
                pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        self.close()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    # =========================================================================
    # 1. READ OPERATIONS (SELECT, VIEWS, JOINS, SUBQUERIES, METADATA)
    # =========================================================================

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        if self.engine == "mysql":
            cursor = self.conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                return cursor.fetchall()
            finally:
                cursor.close()
        else:
            q_strip = query.strip().rstrip(";")
            # Handle DESCRIBE <table> in SQLite
            m_desc = re.match(r"^DESCRIBE\s+(\w+)$", q_strip, flags=re.IGNORECASE)
            if m_desc:
                tbl = m_desc.group(1)
                cur = self.conn.cursor()
                cur.execute(f"PRAGMA table_info({tbl});")
                rows = cur.fetchall()
                cur.close()
                return [
                    {
                        "Field": r["name"],
                        "Type": r["type"],
                        "Null": "NO" if r["notnull"] else "YES",
                        "Key": "PRI" if r["pk"] else "",
                        "Default": r["dflt_value"],
                        "Extra": "auto_increment" if r["pk"] else "",
                    }
                    for r in rows
                ]

            # Handle SHOW INDEX FROM <table> in SQLite
            m_idx = re.match(r"^SHOW\s+INDEX\s+FROM\s+(\w+)$", q_strip, flags=re.IGNORECASE)
            if m_idx:
                tbl = m_idx.group(1)
                cur = self.conn.cursor()
                cur.execute(f"PRAGMA table_info({tbl});")
                cols = cur.fetchall()
                results = []
                for c in cols:
                    if c["pk"]:
                        results.append({"Key_name": "PRIMARY", "Column_name": c["name"], "Non_unique": 0, "Index_type": "BTREE"})
                cur.execute(f"PRAGMA index_list({tbl});")
                idxs = cur.fetchall()
                for idx in idxs:
                    cur.execute(f"PRAGMA index_info({idx['name']});")
                    ic = cur.fetchall()
                    col_name = ic[0]["name"] if ic else ""
                    results.append({
                        "Key_name": idx["name"],
                        "Column_name": col_name,
                        "Non_unique": 0 if idx["unique"] else 1,
                        "Index_type": "BTREE",
                    })
                cur.close()
                return results

            cur = self.conn.cursor()
            try:
                cur.execute(query, params or ())
                rows = cur.fetchall()
                return [dict(r) for r in rows]
            finally:
                cur.close()

    def execute_query_df(self, query: str, params: Optional[Tuple] = None) -> pd.DataFrame:
        data = self.execute_query(query, params)
        return pd.DataFrame(data)

    # =========================================================================
    # 2. WRITE & DML OPERATIONS (INSERT, UPDATE, DELETE)
    # =========================================================================

    def execute_dml(self, query: str, params: Optional[Tuple] = None, auto_commit: bool = True) -> int:
        cur = self.conn.cursor()
        try:
            cur.execute(query, params or ())
            affected_rows = cur.rowcount
            last_id = cur.lastrowid
            if auto_commit:
                self.conn.commit()
            return last_id if last_id else affected_rows
        except Exception as e:
            if auto_commit:
                self.conn.rollback()
            raise e
        finally:
            cur.close()

    # =========================================================================
    # 3. DDL & SCHEMA OPERATIONS
    # =========================================================================

    def execute_ddl(self, statement: str) -> None:
        if self.engine == "mysql":
            cur = self.conn.cursor()
            try:
                cur.execute(statement)
                self.conn.commit()
            finally:
                cur.close()
        else:
            if re.search(r"\b(PROCEDURE|FUNCTION)\b", statement, flags=re.IGNORECASE):
                return
            cur = self.conn.cursor()
            try:
                cur.execute(statement)
                self.conn.commit()
            finally:
                cur.close()

    def execute_script(self, sql_script: str) -> None:
        if self.engine == "mysql":
            cur = self.conn.cursor()
            try:
                for result in cur.execute(sql_script, multi=True):
                    if result.with_rows:
                        result.fetchall()
                self.conn.commit()
            finally:
                cur.close()
        else:
            self.conn.executescript(_adapt_mysql_to_sqlite_sql(sql_script))
            self.conn.commit()

    # =========================================================================
    # 4. STORED PROCEDURES (CURSORS) & FUNCTIONS
    # =========================================================================

    def call_procedure(self, proc_name: str, args: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        if self.engine == "mysql":
            cursor = self.conn.cursor(dictionary=True)
            results = []
            try:
                cursor.callproc(proc_name, args or [])
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                self.conn.commit()
                return results
            except Exception as e:
                self.conn.rollback()
                raise e
            finally:
                cursor.close()
        else:
            pname = proc_name.strip().lower()
            if pname == "sp_total_balance":
                rows = self.execute_query("SELECT COALESCE(SUM(balance), 0.00) AS total_wallet_balance FROM WALLETS;")
                return [{"total_wallet_balance": Decimal(str(rows[0]["total_wallet_balance"])).quantize(Decimal("0.01"))}]
            elif pname == "sp_bonus_active_wallets":
                self.execute_dml("UPDATE WALLETS SET balance = balance + 50 WHERE status = 'ACTIVE';")
                return [{"status": "SUCCESS"}]
            return []

    def _sqlite_fn_get_wallet_balance(self, user_id: int) -> Decimal:
        rows = self.execute_query("SELECT COALESCE(SUM(balance), 0.00) AS val FROM WALLETS WHERE user_id = %s;", (user_id,))
        return Decimal(str(rows[0]["val"])) if rows else Decimal("0.00")

    def _sqlite_fn_total_successful_spend(self, wallet_id: int) -> Decimal:
        rows = self.execute_query(
            "SELECT COALESCE(SUM(amount), 0.00) AS val FROM TRANSACTIONS WHERE sender_wallet_id = %s AND status = 'SUCCESS';",
            (wallet_id,),
        )
        return Decimal(str(rows[0]["val"])) if rows else Decimal("0.00")

    def _sqlite_fn_total_due_bills(self, user_id: int) -> Decimal:
        rows = self.execute_query(
            """
            SELECT COALESCE(SUM(b.amount_due), 0.00) AS val
            FROM BILLS b
            INNER JOIN USER_BILLERS ub ON b.user_biller_id = ub.user_biller_id
            WHERE ub.user_id = %s AND b.status IN ('UNPAID', 'OVERDUE');
            """,
            (user_id,),
        )
        return Decimal(str(rows[0]["val"])) if rows else Decimal("0.00")

    def _sqlite_fn_calculate_cashback(self, amount: float, offer_id: int) -> Decimal:
        rows = self.execute_query("SELECT * FROM CASHBACK_OFFERS WHERE offer_id = %s;", (offer_id,))
        if not rows:
            return Decimal("0.00")
        offer = rows[0]
        if not offer.get("is_active"):
            return Decimal("0.00")
        amt = Decimal(str(amount))
        min_amt = Decimal(str(offer.get("minimum_amount", 0)))
        if amt < min_amt:
            return Decimal("0.00")
        pct = Decimal(str(offer.get("cashback_percentage", 0)))
        max_cb = Decimal(str(offer.get("max_cashback", 0)))
        cb = (amt * pct) / Decimal("100.00")
        if cb > max_cb:
            cb = max_cb
        return cb.quantize(Decimal("0.01"))

    def call_function(self, func_name: str, args: List[Any]) -> Any:
        if self.engine == "mysql":
            placeholders = ", ".join(["%s"] * len(args))
            query = f"SELECT {func_name}({placeholders}) AS result;"
            rows = self.execute_query(query, tuple(args))
            if rows and "result" in rows[0]:
                return rows[0]["result"]
            return None
        else:
            fname = func_name.strip().lower()
            if fname == "fn_get_wallet_balance":
                return self._sqlite_fn_get_wallet_balance(int(args[0]))
            elif fname == "fn_total_successful_spend":
                return self._sqlite_fn_total_successful_spend(int(args[0]))
            elif fname == "fn_total_due_bills":
                return self._sqlite_fn_total_due_bills(int(args[0]))
            elif fname == "fn_calculate_cashback":
                return self._sqlite_fn_calculate_cashback(float(args[0]), int(args[1]))
            return Decimal("0.00")


if __name__ == "__main__":
    print("--- Digital Wallet Hybrid DB Connector Test ---")
    with WalletDBConnector() as db:
        print(f"[+] Connected using engine: {db.engine.upper()}")
        users_df = db.execute_query_df("SELECT user_id, full_name, balance, wallet_status FROM vw_user_wallet_summary LIMIT 3;")
        print(users_df)
        bal = db.call_function("fn_get_wallet_balance", [1])
        print(f"User 1 Wallet Balance: Rs. {bal}")
        cb = db.call_function("fn_calculate_cashback", [650.00, 1])
        print(f"Cashback on Rs. 650 using Offer 1: Rs. {cb}")
        proc_res = db.call_procedure("sp_total_balance")
        print(f"Procedure Output: {proc_res}")
