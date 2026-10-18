USE wallet;

-- =========================================================
-- 1. JOINS (5 JOINS)
-- =========================================================

-- 1. INNER JOIN — Users with their Wallets
SELECT
    u.user_id,
    u.full_name,
    u.app_role,
    w.wallet_id,
    w.balance,
    w.currency,
    w.status AS wallet_status
FROM USERS u
INNER JOIN WALLETS w
    ON u.user_id = w.user_id
ORDER BY u.user_id;

-- 2. NATURAL JOIN — Merchant Categories with Merchants
SELECT
    category_id,
    category_name,
    merchant_id,
    business_name,
    merchant_code,
    status
FROM MERCHANT_CATEGORIES
NATURAL JOIN MERCHANTS
ORDER BY category_id, merchant_id;

-- 3. LEFT OUTER JOIN — All Merchants and their Merchant Transactions
SELECT
    m.merchant_id,
    m.business_name,
    m.status AS merchant_status,
    t.transaction_id,
    t.reference_no,
    t.amount,
    t.status AS transaction_status
FROM MERCHANTS m
LEFT OUTER JOIN TRANSACTIONS t
    ON m.merchant_id = t.merchant_id
    AND t.transaction_type = 'MERCHANT'
ORDER BY m.merchant_id, t.transaction_id;

-- 4. RIGHT OUTER JOIN — All Bills with Payment Information
SELECT
    b.bill_id,
    b.billing_period,
    b.amount_due,
    b.due_date,
    b.status AS bill_status,
    bp.bill_payment_id,
    bp.amount_paid,
    bp.paid_at
FROM BILL_PAYMENTS bp
RIGHT OUTER JOIN BILLS b
    ON bp.bill_id = b.bill_id
ORDER BY b.bill_id;

-- 5. SELF JOIN — Find Users Having the Same KYC Status
SELECT
    u1.full_name AS user_1,
    u2.full_name AS user_2,
    u1.kyc_status
FROM USERS u1
INNER JOIN USERS u2
    ON u1.kyc_status = u2.kyc_status
    AND u1.user_id < u2.user_id
ORDER BY u1.kyc_status, u1.full_name;


-- =========================================================
-- 2. SUBQUERIES (Q1 - Q5)
-- =========================================================

-- Q1: Users whose wallet balance is above the average balance (AVG, nested subquery + IN)
-- Expected: users 4, 6, 9
SELECT user_id, full_name
FROM USERS
WHERE user_id IN (
   SELECT user_id
   FROM WALLETS
   WHERE balance > (SELECT AVG(balance) FROM WALLETS)
);

-- Q2: Bills with the highest amount among all PAID bills (MAX, scalar subquery)
-- Expected: bill 16 (1875.00)
SELECT bill_id, user_biller_id, billing_period, amount_due
FROM BILLS
WHERE amount_due = (
   SELECT MAX(amount_due)
   FROM BILLS
   WHERE status = 'PAID'
);

-- Q3: Users who have at least one OVERDUE bill (EXISTS, correlated subquery)
-- Expected: users 2, 3, 10
SELECT u.user_id, u.full_name
FROM USERS u
WHERE EXISTS (
   SELECT 1
   FROM USER_BILLERS ub
   JOIN BILLS b ON b.user_biller_id = ub.user_biller_id
   WHERE ub.user_id = u.user_id
     AND b.status = 'OVERDUE'
);

-- Q4: Billers subscriptions whose total billed amount exceeds 2000 (SUM + GROUP BY + HAVING)
-- Expected: user_billers 1, 4, 7, 12
SELECT user_biller_id, user_id, nickname
FROM USER_BILLERS
WHERE user_biller_id IN (
   SELECT user_biller_id
   FROM BILLS
   GROUP BY user_biller_id
   HAVING SUM(amount_due) > 2000
);

-- Q5: Users with more than one bank account (COUNT, correlated scalar subquery)
-- Expected: users 1, 2, 4, 6
SELECT u.user_id, u.full_name
FROM USERS u
WHERE (
   SELECT COUNT(*)
   FROM BANK_ACCOUNTS ba
   WHERE ba.user_id = u.user_id
) > 1;


-- =========================================================
-- 3. DML QUERIES (INSERT, UPDATE, DELETE)
-- =========================================================

-- A. INSERT Queries (1-4)
INSERT INTO USERS
(full_name, email, phone, password_hash, app_role, kyc_status, is_active)
VALUES
('Rahul More', 'rahul.more@example.com', '9000000011',
 'hash_demo_11', 'USER', 'PENDING', TRUE);

INSERT INTO WALLETS
(user_id, balance, currency, daily_limit, status)
VALUES
(11, 2000.00, 'INR', 10000.00, 'ACTIVE');

INSERT INTO BANK_ACCOUNTS
(user_id, bank_name, account_no_masked, ifsc_code,
 account_type, is_verified, is_active)
VALUES
(11, 'HDFC Bank', 'XXXXXX8899', 'HDFC0005678',
 'SAVINGS', FALSE, TRUE);

INSERT INTO MERCHANTS
(category_id, business_name, merchant_code, contact_phone, status)
VALUES
(2, 'Campus Book Store', 'MRC011', '9100000011', 'ACTIVE');

-- B. UPDATE Queries (5-10)
UPDATE USERS
SET kyc_status = 'VERIFIED'
WHERE user_id = 11;

UPDATE USERS
SET
    full_name = 'Rahul S. More',
    phone = '9000000091'
WHERE user_id = 11;

UPDATE BANK_ACCOUNTS
SET is_verified = TRUE
WHERE user_id = 11
  AND account_no_masked = 'XXXXXX8899';

UPDATE WALLETS
SET status = 'FROZEN'
WHERE wallet_id = 8;

UPDATE WALLETS
SET daily_limit = 15000.00
WHERE wallet_id = 1;

UPDATE MERCHANTS
SET status = 'SUSPENDED'
WHERE merchant_code = 'MRC011';

-- C. DELETE Queries (11-12)
DELETE FROM MERCHANTS
WHERE merchant_code = 'MRC011';


-- =========================================================
-- 4. TRIGGERS (1 - 3)
-- =========================================================

DROP TRIGGER IF EXISTS trg_after_user_insert;
DELIMITER $$
CREATE TRIGGER trg_after_user_insert
AFTER INSERT ON USERS
FOR EACH ROW
BEGIN
    INSERT INTO WALLETS (user_id, balance, currency, daily_limit, status)
    VALUES (NEW.user_id, 0.00, 'INR', 5000.00, 'ACTIVE');
END$$
DELIMITER ;

INSERT INTO USERS (full_name, email, phone, password_hash, app_role, kyc_status, is_active)
VALUES ('Rahul Pawar', 'rahul.p@example.com', '9000000011', 'hash_demo_11', 'USER', 'PENDING', TRUE);

DROP TRIGGER IF EXISTS trg_after_wallet_update;
DELIMITER $$
CREATE TRIGGER trg_after_wallet_update
AFTER UPDATE ON WALLETS
FOR EACH ROW
BEGIN
    IF OLD.status <> NEW.status THEN
        INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details)
        VALUES (
            NULL,
            'WALLET_STATUS_CHANGE',
            'WALLET',
            NEW.wallet_id,
            JSON_OBJECT('old_status', OLD.status, 'new_status', NEW.status)
        );
    END IF;
END$$
DELIMITER ;

UPDATE WALLETS SET status = 'FROZEN' WHERE wallet_id = 2; 
SELECT * FROM AUDIT_LOGS WHERE action_type = 'WALLET_STATUS_CHANGE'; 

DROP TRIGGER IF EXISTS trg_after_bank_delete;
DELIMITER $$
CREATE TRIGGER trg_after_bank_delete
AFTER DELETE ON BANK_ACCOUNTS
FOR EACH ROW
BEGIN
    INSERT INTO AUDIT_LOGS (actor_user_id, action_type, entity_type, entity_id, details)
    VALUES (
        OLD.user_id,
        'BANK_ACCOUNT_DELETED',
        'BANK_ACCOUNT',
        OLD.bank_account_id,
        JSON_OBJECT('bank_name', OLD.bank_name, 'account_no_masked', OLD.account_no_masked)
    );
END$$
DELIMITER ;

DELETE FROM BANK_ACCOUNTS WHERE bank_account_id = 8 AND is_active = FALSE; 
SELECT * FROM AUDIT_LOGS WHERE action_type = 'BANK_ACCOUNT_DELETED'; 


-- =========================================================
-- 5. CURSORS (STORED PROCEDURES)
-- =========================================================

DROP PROCEDURE IF EXISTS sp_total_balance;
DELIMITER $$
CREATE PROCEDURE sp_total_balance()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_bal DECIMAL(12,2);
    DECLARE v_total DECIMAL(12,2) DEFAULT 0;

    DECLARE cur_wallet CURSOR FOR SELECT balance FROM WALLETS;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur_wallet;

    read_loop: LOOP
        FETCH cur_wallet INTO v_bal;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;
        SET v_total = v_total + v_bal;
    END LOOP;

    CLOSE cur_wallet;

    SELECT v_total AS total_wallet_balance;
END$$
DELIMITER ;

CALL sp_total_balance();

DROP PROCEDURE IF EXISTS sp_bonus_active_wallets;
DELIMITER $$
CREATE PROCEDURE sp_bonus_active_wallets()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_wid INT;

    DECLARE cur_active CURSOR FOR
        SELECT wallet_id FROM WALLETS WHERE status = 'ACTIVE';
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur_active;

    read_loop: LOOP
        FETCH cur_active INTO v_wid;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;
        UPDATE WALLETS SET balance = balance + 50 WHERE wallet_id = v_wid;
    END LOOP;

    CLOSE cur_active;
END$$
DELIMITER ;

CALL sp_bonus_active_wallets();
SELECT wallet_id, balance FROM WALLETS;


-- =========================================================
-- 6. 3 VIEWS + 4 FUNCTIONS
-- =========================================================

DROP VIEW IF EXISTS vw_user_wallet_summary;
CREATE VIEW vw_user_wallet_summary AS
SELECT
    u.user_id,
    u.full_name,
    u.email,
    u.phone,
    u.kyc_status,
    u.is_active AS user_active,
    w.wallet_id,
    w.balance,
    w.currency,
    w.daily_limit,
    w.status AS wallet_status
FROM USERS u
LEFT JOIN WALLETS w
    ON u.user_id = w.user_id;

DROP VIEW IF EXISTS vw_transaction_details;
CREATE VIEW vw_transaction_details AS
SELECT
    t.transaction_id,
    t.reference_no,
    t.transaction_type,
    t.amount,
    t.status,
    t.sender_wallet_id,
    su.full_name AS sender_name,
    t.receiver_wallet_id,
    ru.full_name AS receiver_name,
    t.merchant_id,
    m.business_name AS merchant_name,
    t.bank_account_id,
    ba.bank_name,
    ba.account_no_masked,
    t.description,
    t.initiated_at,
    t.completed_at
FROM TRANSACTIONS t
LEFT JOIN WALLETS sw
    ON t.sender_wallet_id = sw.wallet_id
LEFT JOIN USERS su
    ON sw.user_id = su.user_id
LEFT JOIN WALLETS rw
    ON t.receiver_wallet_id = rw.wallet_id
LEFT JOIN USERS ru
    ON rw.user_id = ru.user_id
LEFT JOIN MERCHANTS m
    ON t.merchant_id = m.merchant_id
LEFT JOIN BANK_ACCOUNTS ba
    ON t.bank_account_id = ba.bank_account_id;

DROP VIEW IF EXISTS vw_due_bills;
CREATE VIEW vw_due_bills AS
SELECT
    b.bill_id,
    u.user_id,
    u.full_name,
    bl.biller_name,
    bl.biller_type,
    ub.consumer_number,
    ub.nickname,
    b.billing_period,
    b.amount_due,
    b.due_date,
    b.status
FROM BILLS b
INNER JOIN USER_BILLERS ub
    ON b.user_biller_id = ub.user_biller_id
INNER JOIN USERS u
    ON ub.user_id = u.user_id
INNER JOIN BILLERS bl
    ON ub.biller_id = bl.biller_id
WHERE b.status IN ('UNPAID', 'OVERDUE');

DROP FUNCTION IF EXISTS fn_get_wallet_balance;
DROP FUNCTION IF EXISTS fn_total_successful_spend;
DROP FUNCTION IF EXISTS fn_total_due_bills;
DROP FUNCTION IF EXISTS fn_calculate_cashback;

DELIMITER $$

CREATE FUNCTION fn_get_wallet_balance
(
    p_user_id INT
)
RETURNS DECIMAL(15,2)
NOT DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_balance DECIMAL(15,2) DEFAULT 0.00;
    SELECT COALESCE(SUM(balance), 0.00)
    INTO v_balance
    FROM WALLETS
    WHERE user_id = p_user_id;
    RETURN v_balance;
END$$

CREATE FUNCTION fn_total_successful_spend
(
    p_wallet_id INT
)
RETURNS DECIMAL(15,2)
NOT DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total DECIMAL(15,2) DEFAULT 0.00;
    SELECT COALESCE(SUM(amount), 0.00)
    INTO v_total
    FROM TRANSACTIONS
    WHERE sender_wallet_id = p_wallet_id
      AND status = 'SUCCESS';
    RETURN v_total;
END$$

CREATE FUNCTION fn_total_due_bills
(
    p_user_id INT
)
RETURNS DECIMAL(15,2)
NOT DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total DECIMAL(15,2) DEFAULT 0.00;
    SELECT COALESCE(SUM(b.amount_due), 0.00)
    INTO v_total
    FROM BILLS b
    INNER JOIN USER_BILLERS ub
        ON b.user_biller_id = ub.user_biller_id
    WHERE ub.user_id = p_user_id
      AND b.status IN ('UNPAID', 'OVERDUE');
    RETURN v_total;
END$$

CREATE FUNCTION fn_calculate_cashback
(
    p_amount DECIMAL(12,2),
    p_offer_id INT
)
RETURNS DECIMAL(12,2)
NOT DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_exists INT DEFAULT 0;
    DECLARE v_minimum DECIMAL(12,2) DEFAULT 0.00;
    DECLARE v_percentage DECIMAL(5,2) DEFAULT 0.00;
    DECLARE v_max_cashback DECIMAL(12,2) DEFAULT 0.00;
    DECLARE v_is_active INT DEFAULT 0;
    DECLARE v_start DATETIME;
    DECLARE v_end DATETIME;
    DECLARE v_cashback DECIMAL(12,2) DEFAULT 0.00;

    SELECT
        COUNT(*),
        COALESCE(MAX(minimum_amount), 0.00),
        COALESCE(MAX(cashback_percentage), 0.00),
        COALESCE(MAX(max_cashback), 0.00),
        COALESCE(MAX(is_active), 0),
        MAX(start_at),
        MAX(end_at)
    INTO
        v_exists,
        v_minimum,
        v_percentage,
        v_max_cashback,
        v_is_active,
        v_start,
        v_end
    FROM CASHBACK_OFFERS
    WHERE offer_id = p_offer_id;

    IF v_exists = 0 THEN
        RETURN 0.00;
    END IF;

    IF v_is_active = 0 THEN
        RETURN 0.00;
    END IF;

    IF NOW() < v_start OR NOW() > v_end THEN
        RETURN 0.00;
    END IF;

    IF p_amount < v_minimum THEN
        RETURN 0.00;
    END IF;

    SET v_cashback = (p_amount * v_percentage) / 100;

    IF v_cashback > v_max_cashback THEN
        SET v_cashback = v_max_cashback;
    END IF;

    RETURN v_cashback;
END$$

DELIMITER ;

-- =========================================================
-- TEST VIEWS & FUNCTIONS
-- =========================================================

SELECT * FROM vw_user_wallet_summary;
SELECT * FROM vw_transaction_details;
SELECT * FROM vw_due_bills ORDER BY due_date;

SELECT fn_get_wallet_balance(1) AS wallet_balance;
SELECT fn_total_successful_spend(1) AS total_successful_spend;
SELECT fn_total_due_bills(1) AS total_due_bill_amount;

SELECT fn_calculate_cashback(650.00, 1) AS cashback_on_650;
SELECT fn_calculate_cashback(900.00, 1) AS cashback_on_900;
SELECT fn_calculate_cashback(200.00, 1) AS cashback_on_200;

SELECT
    u.user_id,
    u.full_name,
    fn_get_wallet_balance(u.user_id) AS wallet_balance,
    fn_total_due_bills(u.user_id) AS total_due_bills
FROM USERS u
ORDER BY u.user_id;

SELECT
    w.wallet_id,
    u.full_name,
    fn_total_successful_spend(w.wallet_id) AS successful_spend
FROM WALLETS w
INNER JOIN USERS u
    ON w.user_id = u.user_id
ORDER BY w.wallet_id;
