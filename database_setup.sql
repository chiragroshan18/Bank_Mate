-- Create database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS pybank;
USE pybank;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    account_number VARCHAR(20) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20),
    type ENUM('Deposit', 'Withdrawal') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES users(account_number)
);

-- Create admins table
CREATE TABLE IF NOT EXISTS admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);