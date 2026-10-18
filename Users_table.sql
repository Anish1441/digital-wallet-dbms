DROP DATABASE IF EXISTS wallet;
CREATE DATABASE wallet;
use wallet;
CREATE TABLE USERS ( user_id INT PRIMARY KEY AUTO_INCREMENT, full_name VARCHAR(100) NOT NULL, email VARCHAR(150) NOT NULL UNIQUE, phone VARCHAR(20) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL, app_role ENUM('USER', 'ADMIN') NOT NULL DEFAULT 'USER', kyc_status ENUM('PENDING', 'VERIFIED', 'FAILED') NOT NULL DEFAULT 'PENDING', is_active BOOLEAN NOT NULL DEFAULT TRUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP );


INSERT INTO USERS
(user_id, full_name, email, phone, password_hash,
 app_role, kyc_status, is_active)
VALUES
(1,  'Aarav Sharma',  'aarav.sharma@example.com',  '9000000001', 'hash_demo_01', 'USER',  'VERIFIED', TRUE),
(2,  'Priya Patil',   'priya.patil@example.com',   '9000000002', 'hash_demo_02', 'USER',  'PENDING',  TRUE),
(3,  'Rohan Deshmukh','rohan.d@example.com',       '9000000003', 'hash_demo_03', 'USER',  'FAILED',   TRUE),
(4,  'Sneha Kulkarni','sneha.k@example.com',       '9000000004', 'hash_demo_04', 'USER',  'VERIFIED', TRUE),
(5,  'Aditya Joshi',  'aditya.j@example.com',      '9000000005', 'hash_demo_05', 'USER',  'PENDING',  FALSE),
(6,  'Neha Shah',     'neha.shah@example.com',     '9000000006', 'hash_demo_06', 'USER',  'VERIFIED', TRUE),
(7,  'Vikram Rao',    'vikram.rao@example.com',    '9000000007', 'hash_demo_07', 'USER',  'FAILED',   FALSE),
(8,  'Ananya Mehta',  'ananya.mehta@example.com',  '9000000008', 'hash_demo_08', 'USER',  'PENDING',  TRUE),
(9,  'Karan Verma',   'karan.verma@example.com',   '9000000009', 'hash_demo_09', 'ADMIN', 'VERIFIED', TRUE),
(10, 'Isha Nair',     'isha.nair@example.com',     '9000000010', 'hash_demo_10', 'USER',  'VERIFIED', TRUE);


use wallet;
CREATE TABLE WALLETS ( wallet_id INT PRIMARY KEY AUTO_INCREMENT, user_id INT NOT NULL UNIQUE, balance DECIMAL(12,2) NOT NULL DEFAULT 0.00, currency CHAR(3) NOT NULL DEFAULT 'INR', daily_limit DECIMAL(12,2) NOT NULL DEFAULT 10000.00, status ENUM('ACTIVE', 'FROZEN', 'CLOSED') NOT NULL DEFAULT 'ACTIVE', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, CONSTRAINT chk_wallet_balance CHECK (balance >= 0), CONSTRAINT chk_wallet_limit CHECK (daily_limit >= 0), CONSTRAINT fk_wallet_user FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE ON UPDATE CASCADE );


INSERT INTO WALLETS
(wallet_id, user_id, balance, currency, daily_limit, status)
VALUES
(1,  1,  5000.00,  'INR', 10000.00, 'ACTIVE'),
(2,  2,  1250.50,  'INR',  5000.00, 'ACTIVE'),
(3,  3,     0.00,  'INR',  5000.00, 'FROZEN'),
(4,  4, 15000.00,  'INR', 20000.00, 'ACTIVE'),
(5,  5,   350.75,  'INR',  3000.00, 'CLOSED'),
(6,  6,  8200.00,  'INR', 10000.00, 'ACTIVE'),
(7,  7,     0.00,  'INR',  2000.00, 'FROZEN'),
(8,  8,   999.99,  'INR',  5000.00, 'ACTIVE'),
(9,  9, 25000.00,  'INR', 50000.00, 'ACTIVE'),
(10, 10,  4750.25, 'INR', 10000.00, 'ACTIVE');


use wallet;
CREATE TABLE BANK_ACCOUNTS ( bank_account_id INT PRIMARY KEY AUTO_INCREMENT, user_id INT NOT NULL, bank_name VARCHAR(100) NOT NULL, account_no_masked VARCHAR(30) NOT NULL, ifsc_code VARCHAR(11) NOT NULL, account_type ENUM('SAVINGS', 'CURRENT') NOT NULL, is_verified BOOLEAN NOT NULL DEFAULT FALSE, is_active BOOLEAN NOT NULL DEFAULT TRUE, linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, CONSTRAINT fk_bank_user FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE ON UPDATE CASCADE );


INSERT INTO BANK_ACCOUNTS
(bank_account_id, user_id, bank_name, account_no_masked,
 ifsc_code, account_type, is_verified, is_active)
VALUES
(1,  1, 'State Bank of India',       'XXXXXX1234', 'SBIN0001234', 'SAVINGS', TRUE,  TRUE),
(2,  1, 'HDFC Bank',                 'XXXXXX5678', 'HDFC0001234', 'SAVINGS', TRUE,  TRUE),
(3,  2, 'ICICI Bank',                'XXXXXX2468', 'ICIC0001234', 'SAVINGS', FALSE, TRUE),
(4,  2, 'Axis Bank',                 'XXXXXX1357', 'UTIB0001234', 'CURRENT', TRUE,  TRUE),
(5,  3, 'Punjab National Bank',      'XXXXXX8642', 'PUNB0001234', 'SAVINGS', FALSE, TRUE),
(6,  4, 'Bank of Baroda',            'XXXXXX9753', 'BARB0001234', 'SAVINGS', TRUE,  TRUE),
(7,  4, 'Kotak Mahindra Bank',       'XXXXXX1122', 'KKBK0001234', 'CURRENT', TRUE,  FALSE),
(8,  5, 'Canara Bank',               'XXXXXX3344', 'CNRB0001234', 'SAVINGS', FALSE, FALSE),
(9,  6, 'Union Bank of India',       'XXXXXX5566', 'UBIN0001234', 'SAVINGS', TRUE,  TRUE),
(10, 6, 'IDFC FIRST Bank',           'XXXXXX7788', 'IDFB0001234', 'CURRENT', FALSE, TRUE),
(11, 7, 'Indian Bank',               'XXXXXX9900', 'IDIB0001234', 'SAVINGS', FALSE, FALSE),
(12, 8, 'IndusInd Bank',             'XXXXXX1020', 'INDB0001234', 'SAVINGS', TRUE,  TRUE),
(13, 9, 'Federal Bank',              'XXXXXX3040', 'FDRL0001234', 'CURRENT', TRUE,  TRUE),
(14, 10,'Yes Bank',                  'XXXXXX5060', 'YESB0001234', 'SAVINGS', TRUE,  TRUE);


use wallet;
CREATE TABLE MERCHANT_CATEGORIES ( category_id INT PRIMARY KEY AUTO_INCREMENT, category_name VARCHAR(100) NOT NULL UNIQUE, description VARCHAR(255) );

INSERT INTO MERCHANT_CATEGORIES
(category_id, category_name, description)
VALUES
(1, 'Food',       'Restaurants, cafes and food delivery services'),
(2, 'Shopping',   'Online stores, retail shops and supermarkets'),
(3, 'Travel',     'Transport, hotels, flights and travel bookings'),
(4, 'Utilities',  'Electricity, water, gas and other utility services'),
(5, 'Healthcare', 'Hospitals, clinics, pharmacies and medical services'),
(6, 'Other',      'Merchants that do not fit into other categories');


use wallet;
CREATE TABLE MERCHANTS (
   merchant_id INT PRIMARY KEY AUTO_INCREMENT,
   category_id INT NOT NULL,
   business_name VARCHAR(150) NOT NULL,
   merchant_code VARCHAR(20) NOT NULL UNIQUE,
   contact_phone VARCHAR(20) NOT NULL,
   status ENUM('ACTIVE', 'SUSPENDED', 'CLOSED') NOT NULL DEFAULT 'ACTIVE',
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
   CONSTRAINT fk_merchant_category
       FOREIGN KEY (category_id)
       REFERENCES MERCHANT_CATEGORIES(category_id)
       ON DELETE RESTRICT
       ON UPDATE CASCADE
);

INSERT INTO MERCHANTS
(merchant_id, category_id, business_name, merchant_code, contact_phone, status)
VALUES
(1,  1, 'Spice Route Kitchen',     'MRC001', '9100000001', 'ACTIVE'),
(2,  1, 'Chai Point Cafe',         'MRC002', '9100000002', 'SUSPENDED'),
(3,  2, 'Metro Mart Supermarket',  'MRC003', '9100000003', 'ACTIVE'),
(4,  2, 'UrbanCart Online',        'MRC004', '9100000004', 'ACTIVE'),
(5,  3, 'QuickRide Cabs',          'MRC005', '9100000005', 'ACTIVE'),
(6,  3, 'Sahyadri Travels',        'MRC006', '9100000006', 'CLOSED'),
(7,  4, 'City Power Services',     'MRC007', '9100000007', 'ACTIVE'),
(8,  5, 'HealthPlus Pharmacy',     'MRC008', '9100000008', 'ACTIVE'),
(9,  5, 'CareWell Clinic',         'MRC009', '9100000009', 'SUSPENDED'),
(10, 6, 'Everyday Services Hub',   'MRC010', '9100000010', 'CLOSED');


use wallet;
CREATE TABLE BILLERS (
   biller_id INT PRIMARY KEY AUTO_INCREMENT,
   biller_name VARCHAR(100) NOT NULL UNIQUE,
   biller_type ENUM('ELECTRICITY', 'MOBILE', 'INTERNET', 'GAS', 'WATER', 'DTH') NOT NULL,
   status ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO BILLERS
(biller_id, biller_name, biller_type, status)
VALUES
(1, 'MSEDCL Electricity',   'ELECTRICITY', 'ACTIVE'),
(2, 'Jio Prepaid/Postpaid', 'MOBILE',      'ACTIVE'),
(3, 'Airtel Broadband',     'INTERNET',    'ACTIVE'),
(4, 'Mahanagar Gas',        'GAS',         'ACTIVE'),
(5, 'PMC Water Supply',     'WATER',       'ACTIVE'),
(6, 'Tata Play DTH',        'DTH',         'INACTIVE');


use wallet;
CREATE TABLE USER_BILLERS (
   user_biller_id INT PRIMARY KEY AUTO_INCREMENT,
   user_id INT NOT NULL,
   biller_id INT NOT NULL,
   consumer_number VARCHAR(30) NOT NULL,
   nickname VARCHAR(50),
   is_active BOOLEAN NOT NULL DEFAULT TRUE,
   created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
   CONSTRAINT uq_biller_consumer
       UNIQUE (biller_id, consumer_number),
 
   CONSTRAINT fk_ub_user
       FOREIGN KEY (user_id)
       REFERENCES USERS(user_id)
       ON DELETE RESTRICT
       ON UPDATE CASCADE,
 
   CONSTRAINT fk_ub_biller
       FOREIGN KEY (biller_id)
       REFERENCES BILLERS(biller_id)
       ON DELETE RESTRICT
       ON UPDATE CASCADE
);

INSERT INTO USER_BILLERS
(user_biller_id, user_id, biller_id, consumer_number, nickname, is_active)
VALUES
(1,  1,  1, '170012345601', 'Home Light Bill',  TRUE),
(2,  1,  2, '9000000001',   'My Mobile',        TRUE),
(3,  1,  3, 'AIR1000301',   'Home WiFi',        TRUE),
(4,  2,  1, '170012345602', 'Flat Electricity', TRUE),
(5,  2,  4, 'MGL5500002',   'Kitchen Gas',      TRUE),
(6,  3,  2, '9000000003',   'My Mobile',        TRUE),
(7,  4,  1, '170012345603', 'Home Electricity', TRUE),
(8,  4,  3, 'AIR1000304',   'Broadband',        TRUE),
(9,  6,  2, '9000000006',   'Phone Recharge',   TRUE),
(10, 6,  5, 'PMC7700006',   'Water Bill',       TRUE),
(11, 8,  6, 'TP8800008',    'TV Subscription',  FALSE),
(12, 10, 3, 'AIR1000310',   'Office WiFi',      TRUE);


use wallet;
CREATE TABLE BILLS (
   bill_id INT PRIMARY KEY AUTO_INCREMENT,
   user_biller_id INT NOT NULL,
   billing_period VARCHAR(20) NOT NULL,
   amount_due DECIMAL(12,2) NOT NULL,
   due_date DATE NOT NULL,
   status ENUM('UNPAID', 'PAID', 'OVERDUE', 'CANCELLED') NOT NULL DEFAULT 'UNPAID',
   generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
   CONSTRAINT chk_bill_amount
       CHECK (amount_due > 0),
 
   CONSTRAINT uq_bill_period
       UNIQUE (user_biller_id, billing_period),
 
   CONSTRAINT fk_bill_user_biller
       FOREIGN KEY (user_biller_id)
       REFERENCES USER_BILLERS(user_biller_id)
       ON DELETE RESTRICT
       ON UPDATE CASCADE
);

INSERT INTO BILLS
(bill_id, user_biller_id, billing_period, amount_due, due_date, status, generated_at)
VALUES
(1,  1,  '2026-08', 1450.00, '2026-09-05', 'PAID',      '2026-08-25 09:00:00'),
(2,  1,  '2026-09', 1620.50, '2026-10-05', 'UNPAID',    '2026-09-25 09:00:00'),
(3,  2,  '2026-09',  299.00, '2026-09-25', 'PAID',      '2026-09-10 09:00:00'),
(4,  3,  '2026-09',  799.00, '2026-09-28', 'PAID',      '2026-09-13 09:00:00'),
(5,  4,  '2026-08',  980.75, '2026-09-05', 'PAID',      '2026-08-25 09:00:00'),
(6,  4,  '2026-09', 1105.00, '2026-10-05', 'UNPAID',    '2026-09-25 09:00:00'),
(7,  5,  '2026-09',  540.00, '2026-09-30', 'OVERDUE',   '2026-09-15 09:00:00'),
(8,  6,  '2026-08',  399.00, '2026-09-01', 'OVERDUE',   '2026-08-17 09:00:00'),
(9,  7,  '2026-09', 2210.25, '2026-10-06', 'UNPAID',    '2026-09-26 09:00:00'),
(10, 8,  '2026-09',  999.00, '2026-09-28', 'PAID',      '2026-09-13 09:00:00'),
(11, 9,  '2026-09',  719.00, '2026-09-26', 'PAID',      '2026-09-11 09:00:00'),
(12, 10, '2026-09',  185.00, '2026-10-10', 'UNPAID',    '2026-09-28 09:00:00'),
(13, 11, '2026-09',  350.00, '2026-09-20', 'PAID',      '2026-09-05 09:00:00'),
(14, 12, '2026-09', 1199.00, '2026-09-29', 'PAID',      '2026-09-14 09:00:00'),
(15, 12, '2026-08', 1199.00, '2026-09-01', 'OVERDUE',   '2026-08-17 09:00:00'),
(16, 7,  '2026-08', 1875.00, '2026-09-05', 'PAID',      '2026-08-26 09:00:00'),
(17, 6,  '2026-09',  399.00, '2026-10-08', 'UNPAID',    '2026-09-23 09:00:00'),
(18, 9,  '2026-08',  719.00, '2026-08-26', 'CANCELLED', '2026-08-11 09:00:00'),
(19, 11, '2026-08',  350.00, '2026-08-20', 'CANCELLED', '2026-08-05 09:00:00'),
(20, 2,  '2026-08',  299.00, '2026-08-25', 'PAID',      '2026-08-10 09:00:00');
 

use  wallet;
CREATE TABLE TRANSACTIONS (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    reference_no VARCHAR(40) NOT NULL UNIQUE,
    sender_wallet_id INT NULL,
    receiver_wallet_id INT NULL,
    merchant_id INT NULL,
    bank_account_id INT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_type ENUM(
        'P2P',
        'BANK_TO_WALLET',
        'WALLET_TO_BANK',
        'MERCHANT',
        'BILL_PAYMENT',
        'CASHBACK',
        'ADJUSTMENT'
    ) NOT NULL,
    status ENUM(
        'PENDING',
        'SUCCESS',
        'FAILED',
        'REVERSED'
    ) NOT NULL DEFAULT 'PENDING',
    description VARCHAR(255),
    initiated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,

    CONSTRAINT chk_txn_amount
        CHECK (amount > 0),

    CONSTRAINT fk_txn_sender
        FOREIGN KEY (sender_wallet_id)
        REFERENCES WALLETS(wallet_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_txn_receiver
        FOREIGN KEY (receiver_wallet_id)
        REFERENCES WALLETS(wallet_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_txn_merchant
        FOREIGN KEY (merchant_id)
        REFERENCES MERCHANTS(merchant_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_txn_bank
        FOREIGN KEY (bank_account_id)
        REFERENCES BANK_ACCOUNTS(bank_account_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

INSERT INTO TRANSACTIONS
(
    transaction_id,
    reference_no,
    sender_wallet_id,
    receiver_wallet_id,
    merchant_id,
    bank_account_id,
    amount,
    transaction_type,
    status,
    description,
    initiated_at,
    completed_at
)
VALUES

(1, 'TXN-MER-0001', 1, NULL, 1, NULL, 650.00,
 'MERCHANT', 'SUCCESS', 'Payment to Spice Route Kitchen',
 '2026-09-10 12:10:00', '2026-09-10 12:10:05'),

(2, 'TXN-MER-0002', 2, NULL, 1, NULL, 900.00,
 'MERCHANT', 'SUCCESS', 'Payment to Spice Route Kitchen',
 '2026-09-12 13:20:00', '2026-09-12 13:20:04'),

(3, 'TXN-MER-0003', 4, NULL, 3, NULL, 2000.00,
 'MERCHANT', 'SUCCESS', 'Shopping at Metro Mart Supermarket',
 '2026-09-14 17:30:00', '2026-09-14 17:30:06'),

(4, 'TXN-MER-0004', 6, NULL, 3, NULL, 1250.00,
 'MERCHANT', 'SUCCESS', 'Shopping at Metro Mart Supermarket',
 '2026-09-16 18:15:00', '2026-09-16 18:15:05'),

(5, 'TXN-MER-0005', 8, NULL, 5, NULL, 750.00,
 'MERCHANT', 'SUCCESS', 'Payment to QuickRide Cabs',
 '2026-09-18 10:30:00', '2026-09-18 10:30:03'),

(6, 'TXN-MER-0006', 10, NULL, 5, NULL, 1200.00,
 'MERCHANT', 'SUCCESS', 'Payment to QuickRide Cabs',
 '2026-09-20 15:10:00', '2026-09-20 15:10:05'),

(7, 'TXN-MER-0007', 1, NULL, 8, NULL, 500.00,
 'MERCHANT', 'SUCCESS', 'Purchase from HealthPlus Pharmacy',
 '2026-09-21 11:00:00', '2026-09-21 11:00:05'),

(8, 'TXN-MER-0008', 2, NULL, 8, NULL, 1000.00,
 'MERCHANT', 'SUCCESS', 'Purchase from HealthPlus Pharmacy',
 '2026-09-22 16:20:00', '2026-09-22 16:20:04'),

(9, 'TXN-MER-0009', 4, NULL, 4, NULL, 1200.00,
 'MERCHANT', 'SUCCESS', 'Purchase from UrbanCart Online',
 '2026-09-24 19:00:00', '2026-09-24 19:00:06'),

(10, 'TXN-MER-0010', 6, NULL, 7, NULL, 600.00,
 'MERCHANT', 'SUCCESS', 'Payment to City Power Services',
 '2026-09-25 10:15:00', '2026-09-25 10:15:04'),

(11, 'TXN-MER-0011', 8, NULL, 4, NULL, 500.00,
 'MERCHANT', 'SUCCESS', 'August purchase at UrbanCart Online',
 '2026-08-15 14:00:00', '2026-08-15 14:00:05'),

(12, 'TXN-MER-0012', 10, NULL, 4, NULL, 1000.00,
 'MERCHANT', 'SUCCESS', 'Purchase from UrbanCart Online',
 '2026-09-27 20:10:00', '2026-09-27 20:10:05'),

(13, 'TXN-MER-0013', 1, NULL, 2, NULL, 450.00,
 'MERCHANT', 'FAILED', 'Merchant payment failed',
 '2026-10-01 09:45:00', '2026-10-01 09:45:03'),

(14, 'TXN-MER-0014', 4, NULL, 3, NULL, 1800.00,
 'MERCHANT', 'PENDING', 'Merchant payment awaiting completion',
 '2026-10-04 10:30:00', NULL),

(15, 'TXN-MER-0015', 6, NULL, 9, NULL, 700.00,
 'MERCHANT', 'REVERSED', 'Merchant payment reversed',
 '2026-09-29 14:25:00', '2026-09-29 15:10:00'),

(16, 'TXN-MER-0016', 4, NULL, 6, NULL, 300.00,
 'MERCHANT', 'SUCCESS', 'Historical travel payment',
 '2026-08-12 11:20:00', '2026-08-12 11:20:04'),

(17, 'TXN-BILL-0001', 1, NULL, NULL, NULL, 299.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 20',
 '2026-08-20 09:30:00', '2026-08-20 09:30:05'),

(18, 'TXN-BILL-0002', 1, NULL, NULL, NULL, 1450.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 1',
 '2026-09-01 10:15:00', '2026-09-01 10:15:04'),

(19, 'TXN-BILL-0003', 2, NULL, NULL, NULL, 980.75,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 5',
 '2026-09-02 11:00:00', '2026-09-02 11:00:05'),

(20, 'TXN-BILL-0004', 4, NULL, NULL, NULL, 1875.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 16',
 '2026-09-03 13:30:00', '2026-09-03 13:30:05'),

(21, 'TXN-BILL-0005', 1, NULL, NULL, NULL, 299.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 3',
 '2026-09-20 09:00:00', '2026-09-20 09:00:04'),

(22, 'TXN-BILL-0006', 1, NULL, NULL, NULL, 799.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 4',
 '2026-09-22 09:40:00', '2026-09-22 09:40:04'),

(23, 'TXN-BILL-0007', 4, NULL, NULL, NULL, 999.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 10',
 '2026-09-25 08:50:00', '2026-09-25 08:50:04'),

(24, 'TXN-BILL-0008', 6, NULL, NULL, NULL, 719.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 11',
 '2026-09-24 12:10:00', '2026-09-24 12:10:03'),

(25, 'TXN-BILL-0009', 8, NULL, NULL, NULL, 350.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 13',
 '2026-09-18 17:30:00', '2026-09-18 17:30:03'),

(26, 'TXN-BILL-0010', 10, NULL, NULL, NULL, 1199.00,
 'BILL_PAYMENT', 'SUCCESS', 'Payment for Bill 14',
 '2026-09-27 18:00:00', '2026-09-27 18:00:05'),

(27, 'TXN-P2P-0001', 1, 2, NULL, NULL, 750.00,
 'P2P', 'SUCCESS', 'Money sent from Aarav to Priya',
 '2026-09-05 10:00:00', '2026-09-05 10:00:03'),

(28, 'TXN-P2P-0002', 4, 6, NULL, NULL, 1000.00,
 'P2P', 'SUCCESS', 'Money sent from Sneha to Neha',
 '2026-09-07 11:15:00', '2026-09-07 11:15:04'),

(29, 'TXN-P2P-0003', 6, 10, NULL, NULL, 500.00,
 'P2P', 'SUCCESS', 'Money sent from Neha to Isha',
 '2026-09-09 16:30:00', '2026-09-09 16:30:03'),

(30, 'TXN-P2P-0004', 8, 1, NULL, NULL, 250.00,
 'P2P', 'SUCCESS', 'Money sent from Ananya to Aarav',
 '2026-09-11 13:10:00', '2026-09-11 13:10:05'),

(31, 'TXN-P2P-0005', 2, 4, NULL, NULL, 3000.00,
 'P2P', 'FAILED', 'Transfer failed due to insufficient balance',
 '2026-09-15 09:20:00', '2026-09-15 09:20:02'),

(32, 'TXN-P2P-0006', 3, 1, NULL, NULL, 400.00,
 'P2P', 'FAILED', 'Transfer failed because wallet was frozen',
 '2026-09-17 12:00:00', '2026-09-17 12:00:02'),

(33, 'TXN-P2P-0007', 10, 4, NULL, NULL, 600.00,
 'P2P', 'REVERSED', 'P2P transfer reversed',
 '2026-09-19 18:00:00', '2026-09-19 18:20:00'),

(34, 'TXN-P2P-0008', 1, 6, NULL, NULL, 350.00,
 'P2P', 'PENDING', 'P2P transfer pending',
 '2026-10-04 11:15:00', NULL),

(35, 'TXN-BTW-0001', NULL, 1, NULL, 1, 2000.00,
 'BANK_TO_WALLET', 'SUCCESS', 'Added money from SBI account',
 '2026-09-06 09:30:00', '2026-09-06 09:30:05'),

(36, 'TXN-BTW-0002', NULL, 2, NULL, 3, 1000.00,
 'BANK_TO_WALLET', 'FAILED', 'Bank account verification failed',
 '2026-09-08 11:30:00', '2026-09-08 11:30:03'),

(37, 'TXN-BTW-0003', NULL, 4, NULL, 6, 5000.00,
 'BANK_TO_WALLET', 'SUCCESS', 'Added money from Bank of Baroda',
 '2026-09-10 14:00:00', '2026-09-10 14:00:05'),

(38, 'TXN-BTW-0004', NULL, 6, NULL, 9, 1500.00,
 'BANK_TO_WALLET', 'SUCCESS', 'Added money from Union Bank',
 '2026-09-12 10:30:00', '2026-09-12 10:30:04'),

(39, 'TXN-BTW-0005', NULL, 8, NULL, 12, 800.00,
 'BANK_TO_WALLET', 'PENDING', 'Bank to wallet transfer pending',
 '2026-10-04 12:00:00', NULL),

(40, 'TXN-BTW-0006', NULL, 10, NULL, 14, 2500.00,
 'BANK_TO_WALLET', 'SUCCESS', 'Added money from Yes Bank',
 '2026-09-28 15:15:00', '2026-09-28 15:15:05'),

(41, 'TXN-WTB-0001', 1, NULL, NULL, 2, 1000.00,
 'WALLET_TO_BANK', 'SUCCESS', 'Wallet withdrawal to HDFC Bank',
 '2026-09-13 10:10:00', '2026-09-13 10:10:04'),

(42, 'TXN-WTB-0002', 2, NULL, NULL, 4, 500.00,
 'WALLET_TO_BANK', 'SUCCESS', 'Wallet withdrawal to Axis Bank',
 '2026-09-14 11:20:00', '2026-09-14 11:20:04'),

(43, 'TXN-WTB-0003', 4, NULL, NULL, 7, 1200.00,
 'WALLET_TO_BANK', 'REVERSED', 'Withdrawal reversed to wallet',
 '2026-09-16 15:00:00', '2026-09-16 15:30:00'),

(44, 'TXN-WTB-0004', 6, NULL, NULL, 10, 700.00,
 'WALLET_TO_BANK', 'FAILED', 'Withdrawal failed due to bank verification',
 '2026-09-18 13:45:00', '2026-09-18 13:45:03'),

(45, 'TXN-WTB-0005', 10, NULL, NULL, 14, 900.00,
 'WALLET_TO_BANK', 'SUCCESS', 'Wallet withdrawal to Yes Bank',
 '2026-09-30 17:10:00', '2026-09-30 17:10:05'),

(46, 'TXN-CB-0001', NULL, 1, NULL, NULL, 65.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0001',
 '2026-09-10 12:11:00', '2026-09-10 12:11:02'),

(47, 'TXN-CB-0002', NULL, 2, NULL, NULL, 75.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0002',
 '2026-09-12 13:21:00', '2026-09-12 13:21:02'),

(48, 'TXN-CB-0003', NULL, 4, NULL, NULL, 100.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0003',
 '2026-09-14 17:31:00', '2026-09-14 17:31:02'),

(49, 'TXN-CB-0004', NULL, 6, NULL, NULL, 62.50,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0004',
 '2026-09-16 18:16:00', '2026-09-16 18:16:02'),

(50, 'TXN-CB-0005', NULL, 8, NULL, NULL, 60.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0005',
 '2026-09-18 10:31:00', '2026-09-18 10:31:02'),

(51, 'TXN-CB-0006', NULL, 10, NULL, NULL, 80.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0006',
 '2026-09-20 15:11:00', '2026-09-20 15:11:02'),

(52, 'TXN-CB-0007', NULL, 1, NULL, NULL, 30.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0007',
 '2026-09-21 11:01:00', '2026-09-21 11:01:02'),

(53, 'TXN-CB-0008', NULL, 2, NULL, NULL, 60.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0008',
 '2026-09-22 16:21:00', '2026-09-22 16:21:02'),

(54, 'TXN-CB-0009', NULL, 4, NULL, NULL, 24.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0009',
 '2026-09-24 19:01:00', '2026-09-24 19:01:02'),

(55, 'TXN-CB-0010', NULL, 6, NULL, NULL, 12.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0010',
 '2026-09-25 10:16:00', '2026-09-25 10:16:02'),

(56, 'TXN-CB-0011', NULL, 8, NULL, NULL, 15.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0011',
 '2026-08-15 14:01:00', '2026-08-15 14:01:02'),

(57, 'TXN-CB-0012', NULL, 10, NULL, NULL, 20.00,
 'CASHBACK', 'SUCCESS', 'Cashback for TXN-MER-0012',
 '2026-09-27 20:11:00', '2026-09-27 20:11:02'),

(58, 'TXN-ADJ-0001', NULL, 3, NULL, NULL, 100.00,
 'ADJUSTMENT', 'SUCCESS', 'Administrative balance correction',
 '2026-09-02 12:00:00', '2026-09-02 12:00:03'),

(59, 'TXN-ADJ-0002', NULL, 5, NULL, NULL, 50.00,
 'ADJUSTMENT', 'SUCCESS', 'Promotional balance adjustment',
 '2026-09-04 13:00:00', '2026-09-04 13:00:03'),

(60, 'TXN-ADJ-0003', NULL, 7, NULL, NULL, 25.00,
 'ADJUSTMENT', 'FAILED', 'Administrative adjustment failed',
 '2026-09-06 14:00:00', '2026-09-06 14:00:02');


use wallet;
CREATE TABLE BILL_PAYMENTS (
    bill_payment_id INT PRIMARY KEY AUTO_INCREMENT,
    bill_id INT NOT NULL UNIQUE,
    transaction_id INT NOT NULL UNIQUE,
    amount_paid DECIMAL(12,2) NOT NULL,
    paid_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_bill_payment_amount
        CHECK (amount_paid > 0),

    CONSTRAINT fk_bill_payment_bill
        FOREIGN KEY (bill_id)
        REFERENCES BILLS(bill_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_bill_payment_txn
        FOREIGN KEY (transaction_id)
        REFERENCES TRANSACTIONS(transaction_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);



INSERT INTO BILL_PAYMENTS
(bill_payment_id, bill_id, transaction_id, amount_paid, paid_at)
VALUES
(1,  20, 17,  299.00,  '2026-08-20 09:30:05'),
(2,   1, 18, 1450.00,  '2026-09-01 10:15:04'),
(3,   5, 19,  980.75,  '2026-09-02 11:00:05'),
(4,  16, 20, 1875.00,  '2026-09-03 13:30:05'),
(5,   3, 21,  299.00,  '2026-09-20 09:00:04'),
(6,   4, 22,  799.00,  '2026-09-22 09:40:04'),
(7,  10, 23,  999.00,  '2026-09-25 08:50:04'),
(8,  11, 24,  719.00,  '2026-09-24 12:10:03'),
(9,  13, 25,  350.00,  '2026-09-18 17:30:03'),
(10, 14, 26, 1199.00,  '2026-09-27 18:00:05');


use wallet;
CREATE TABLE CASHBACK_OFFERS (
    offer_id INT PRIMARY KEY AUTO_INCREMENT,
    merchant_id INT NULL,
    offer_name VARCHAR(120) NOT NULL,
    promo_code VARCHAR(30) UNIQUE,
    minimum_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    cashback_percentage DECIMAL(5,2) NOT NULL,
    max_cashback DECIMAL(12,2) NOT NULL,
    start_at DATETIME NOT NULL,
    end_at DATETIME NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_offer_minimum
        CHECK (minimum_amount >= 0),

    CONSTRAINT chk_offer_percent
        CHECK (
            cashback_percentage >= 0
            AND cashback_percentage <= 100
        ),

    CONSTRAINT chk_offer_cap
        CHECK (max_cashback >= 0),

    CONSTRAINT chk_offer_dates
        CHECK (end_at > start_at),

    CONSTRAINT fk_offer_merchant
        FOREIGN KEY (merchant_id)
        REFERENCES MERCHANTS(merchant_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


INSERT INTO CASHBACK_OFFERS
(
    offer_id,
    merchant_id,
    offer_name,
    promo_code,
    minimum_amount,
    cashback_percentage,
    max_cashback,
    start_at,
    end_at,
    is_active
)
VALUES

(1, 1,
 'Spice Route 10% Cashback',
 'SPICE10',
 300.00, 10.00, 75.00,
 '2026-09-01 00:00:00',
 '2026-10-31 23:59:59',
 TRUE),

(2, NULL,
 'General Wallet 2% Cashback',
 'WALLET2',
 500.00, 2.00, 50.00,
 '2026-09-01 00:00:00',
 '2026-12-31 23:59:59',
 TRUE),

(3, 3,
 'Metro Mart 5% Cashback',
 'METRO5',
 1000.00, 5.00, 100.00,
 '2026-09-01 00:00:00',
 '2026-10-31 23:59:59',
 TRUE),

(4, 5,
 'QuickRide 8% Cashback',
 'RIDE8',
 500.00, 8.00, 80.00,
 '2026-09-01 00:00:00',
 '2026-10-31 23:59:59',
 TRUE),

(5, 8,
 'HealthPlus 6% Cashback',
 'HEALTH6',
 250.00, 6.00, 60.00,
 '2026-09-01 00:00:00',
 '2026-10-31 23:59:59',
 TRUE),

(6, NULL,
 'August Bonus 3% Cashback',
 'AUGUST3',
 400.00, 3.00, 30.00,
 '2026-08-01 00:00:00',
 '2026-08-31 23:59:59',
 FALSE);


use wallet;
CREATE TABLE CASHBACK_HISTORY (
    cashback_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    source_transaction_id INT NOT NULL UNIQUE,
    offer_id INT NULL,
    amount DECIMAL(12,2) NOT NULL,
    credited_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_cashback_amount
        CHECK (amount > 0),

    CONSTRAINT fk_cashback_user
        FOREIGN KEY (user_id)
        REFERENCES USERS(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_cashback_source
        FOREIGN KEY (source_transaction_id)
        REFERENCES TRANSACTIONS(transaction_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_cashback_offer
        FOREIGN KEY (offer_id)
        REFERENCES CASHBACK_OFFERS(offer_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);




INSERT INTO CASHBACK_HISTORY
(
    cashback_id,
    user_id,
    source_transaction_id,
    offer_id,
    amount,
    credited_at
)
VALUES

(1,  1,  1, 1,  65.00,  '2026-09-10 12:11:00'),

(2,  2,  2, 1,  75.00,  '2026-09-12 13:21:00'),

(3,  4,  3, 3, 100.00,  '2026-09-14 17:31:00'),

(4,  6,  4, 3,  62.50,  '2026-09-16 18:16:00'),

(5,  8,  5, 4,  60.00,  '2026-09-18 10:31:00'),

(6, 10,  6, 4,  80.00,  '2026-09-20 15:11:00'),

(7,  1,  7, 5,  30.00,  '2026-09-21 11:01:00'),

(8,  2,  8, 5,  60.00,  '2026-09-22 16:21:00'),

(9,  4,  9, 2,  24.00,  '2026-09-24 19:01:00'),

(10, 6, 10, 2,  12.00,  '2026-09-25 10:16:00'),

(11, 8, 11, 6,  15.00,  '2026-08-15 14:01:00'),

(12, 10, 12, 2, 20.00,  '2026-09-27 20:11:00');


use wallet;
CREATE TABLE AUDIT_LOGS (
    audit_id INT PRIMARY KEY AUTO_INCREMENT,
    actor_user_id INT NULL,
    action_type VARCHAR(60) NOT NULL,
    entity_type VARCHAR(60) NOT NULL,
    entity_id INT NULL,
    details JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_actor
        FOREIGN KEY (actor_user_id)
        REFERENCES USERS(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


INSERT INTO AUDIT_LOGS
(
    audit_id,
    actor_user_id,
    action_type,
    entity_type,
    entity_id,
    details,
    created_at
)
VALUES

(1, 1,
 'USER_LOGIN',
 'USER',
 1,
 JSON_OBJECT('result', 'SUCCESS'),
 '2026-09-05 09:50:00'),

(2, 1,
 'P2P_TRANSFER',
 'TRANSACTION',
 27,
 JSON_OBJECT('receiver_wallet_id', 2, 'amount', 750.00, 'status', 'SUCCESS'),
 '2026-09-05 10:00:03'),

(3, 4,
 'P2P_TRANSFER',
 'TRANSACTION',
 28,
 JSON_OBJECT('receiver_wallet_id', 6, 'amount', 1000.00, 'status', 'SUCCESS'),
 '2026-09-07 11:15:04'),

(4, 2,
 'TRANSFER_FAILED',
 'TRANSACTION',
 31,
 JSON_OBJECT('reason', 'INSUFFICIENT_BALANCE', 'amount', 3000.00),
 '2026-09-15 09:20:02'),

(5, 3,
 'TRANSFER_FAILED',
 'TRANSACTION',
 32,
 JSON_OBJECT('reason', 'WALLET_FROZEN', 'amount', 400.00),
 '2026-09-17 12:00:02'),

(6, 9,
 'WALLET_FREEZE',
 'WALLET',
 3,
 JSON_OBJECT('new_status', 'FROZEN'),
 '2026-09-17 12:05:00'),

(7, 9,
 'WALLET_FREEZE',
 'WALLET',
 7,
 JSON_OBJECT('new_status', 'FROZEN'),
 '2026-09-18 10:00:00'),

(8, 9,
 'WALLET_CLOSE',
 'WALLET',
 5,
 JSON_OBJECT('new_status', 'CLOSED'),
 '2026-09-19 10:00:00'),

(9, 1,
 'BANK_ACCOUNT_LINK',
 'BANK_ACCOUNT',
 2,
 JSON_OBJECT('bank_name', 'HDFC Bank'),
 '2026-09-01 08:30:00'),

(10, 2,
 'BANK_ACCOUNT_LINK',
 'BANK_ACCOUNT',
 4,
 JSON_OBJECT('bank_name', 'Axis Bank'),
 '2026-09-02 08:45:00'),

(11, 1,
 'MERCHANT_PAYMENT',
 'TRANSACTION',
 1,
 JSON_OBJECT('merchant_id', 1, 'amount', 650.00, 'status', 'SUCCESS'),
 '2026-09-10 12:10:05'),

(12, 2,
 'MERCHANT_PAYMENT',
 'TRANSACTION',
 2,
 JSON_OBJECT('merchant_id', 1, 'amount', 900.00, 'status', 'SUCCESS'),
 '2026-09-12 13:20:04'),

(13, 1,
 'BILL_PAYMENT',
 'BILL',
 1,
 JSON_OBJECT('transaction_id', 18, 'amount', 1450.00),
 '2026-09-01 10:15:04'),

(14, 4,
 'BILL_PAYMENT',
 'BILL',
 10,
 JSON_OBJECT('transaction_id', 23, 'amount', 999.00),
 '2026-09-25 08:50:04'),

(15, 6,
 'BILL_PAYMENT',
 'BILL',
 11,
 JSON_OBJECT('transaction_id', 24, 'amount', 719.00),
 '2026-09-24 12:10:03'),

(16, 1,
 'CASHBACK_CREDIT',
 'CASHBACK',
 1,
 JSON_OBJECT('source_transaction_id', 1, 'amount', 65.00),
 '2026-09-10 12:11:00'),

(17, 2,
 'CASHBACK_CREDIT',
 'CASHBACK',
 2,
 JSON_OBJECT('source_transaction_id', 2, 'amount', 75.00),
 '2026-09-12 13:21:00'),

(18, 4,
 'CASHBACK_CREDIT',
 'CASHBACK',
 3,
 JSON_OBJECT('source_transaction_id', 3, 'amount', 100.00),
 '2026-09-14 17:31:00'),

(19, 9,
 'MERCHANT_SUSPEND',
 'MERCHANT',
 2,
 JSON_OBJECT('merchant_name', 'Chai Point Cafe', 'new_status', 'SUSPENDED'),
 '2026-09-26 10:00:00'),

(20, 9,
 'MERCHANT_SUSPEND',
 'MERCHANT',
 9,
 JSON_OBJECT('merchant_name', 'CareWell Clinic', 'new_status', 'SUSPENDED'),
 '2026-09-27 10:00:00'),

(21, 9,
 'MERCHANT_CLOSE',
 'MERCHANT',
 6,
 JSON_OBJECT('merchant_name', 'Sahyadri Travels', 'new_status', 'CLOSED'),
 '2026-09-28 10:00:00'),

(22, 9,
 'CASHBACK_OFFER_CREATED',
 'CASHBACK_OFFER',
 1,
 JSON_OBJECT('promo_code', 'SPICE10', 'percentage', 10.00),
 '2026-09-01 09:00:00'),

(23, 9,
 'CASHBACK_OFFER_CREATED',
 'CASHBACK_OFFER',
 2,
 JSON_OBJECT('promo_code', 'WALLET2', 'percentage', 2.00),
 '2026-09-01 09:05:00'),

(24, 9,
 'TRANSACTION_REVERSED',
 'TRANSACTION',
 15,
 JSON_OBJECT('original_status', 'SUCCESS', 'new_status', 'REVERSED'),
 '2026-09-29 15:10:00'),

(25, 9,
 'ADMIN_ADJUSTMENT',
 'TRANSACTION',
 58,
 JSON_OBJECT('wallet_id', 3, 'amount', 100.00, 'status', 'SUCCESS'),
 '2026-09-02 12:00:03');


