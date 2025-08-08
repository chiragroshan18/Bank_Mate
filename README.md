#  🏦  BankMate

🚀 About the Project
Bank Mate 💳 is a sleek, user-friendly ATM Management System built using Python (PyQt5) and MySQL, designed to replicate the core features of real-world banking in a simple, educational environment.

Whether you're a beginner trying to understand the logic behind ATM systems, or a student working on a database-connected GUI project, Bank Mate provides a solid foundation to learn from — all wrapped in an intuitive graphical interface.

# Logo
<img width="1141" height="941" alt="logo" src="https://github.com/user-attachments/assets/eab5b883-306d-416c-8e24-2a2c210cabba" />


# 🎯 Who is This Project For?
    
    👨‍🎓 Students exploring Database + GUI integration

    🧑‍💻 Beginners in Python looking for hands-on project experience

    🧠 Anyone curious about how ATM systems work internally

## ✨ Features

### 👤 User Features
- 🔐 Account login with secure PIN authentication  
- 💰 Deposit money into accounts  
- 🏧 Withdraw money from accounts  
- 📜 View transaction history  
- 🆕 Create new bank accounts  

### 🛠️ Admin Features
- 🔐 Secure admin login  
- 👥 View all users and their balances  
- 🔎 Search for specific users  
- 📊 View all transactions  
- 🧑‍💼 Create new admin accounts  

## 🧱 Built With

### 🎨 Frontend
- 🐍 Python with **PyQt5** – for building the graphical user interface (GUI)
- 💡 Minimalistic and responsive UI design

### ⚙️ Backend
- 🧠 Python – handles the application logic and core functionality
- 🔐 bcrypt – used for password hashing and authentication

### 🗄️ Database
- 🛢️ MySQL – for storing users, transactions, and admin data
- 💾 SQL queries – includes `INSERT`, `SELECT`, `UPDATE`, `DELETE` operations




## 🌟 Acknowledgements


Every project is a journey — and Bank Mate 💳 was no exception. Here’s a heartfelt note of gratitude for all that helped shape it:

🙏 Grateful Moments & Inspirations
    > 🧠 The countless hours of self-learning and exploring new concepts gave this project its soul.

    > 💻 Experimenting with GUIs and SQL helped me understand the depth of user-focused programming.

    > 🛠️ Debugging struggles that turned into “aha!” moments — they taught me more than success ever could.

    > ✍️ The art of documenting — I discovered the power of clarity while explaining my work to others.

    > ⚙️ Building from scratch — from the first line of code to the final polish, it was all part of a beautiful challenge.


## 💡  Key Features

### User System
- Secure PIN-based authentication
- Real-time transaction processing
- Comprehensive account history

### Admin System
- User account management
- Transaction monitoring
- Advanced search capabilities

## 🛠️ Technical Stack
- **Frontend**: PyQt5
- **Backend**: Python 3.8+
- **Database**: MySQL 8.0+
- **Security**: bcrypt hashing

---



## 📂 Database Schema

The application uses the following database structure:

```sql
-- Users table
CREATE TABLE users (
    account_number VARCHAR(20) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00
);

-- Transactions table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20),
    type ENUM('Deposit', 'Withdrawal') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES users(account_number)
);

-- Admins table
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
```
## 🔧 Installation
1. **Clone the repository**
```bash
git clone https://github.com/chiragroshan18/bank-mate.git
cd bank-mate
```
2. **Install dependencies**
 ```bash
   pip install -r requirements.txt
```
3. **Set up the MySQL database**
 ```bash
mysql -u root -p < database_setup.sql
```
4. **Configure database connection in db_config.py**
   ```bash
   conn = mysql.connector.connect(
    host='localhost',
    database='pybank',
    user='your_username',
    password='your_password'
   ```
4. **Run the application**
```bash
python main.py
```
## 🧭 Usage Guide

### 👤 For Users:
1. From the main menu, select **"User Login"**  
2. Enter your **account number** and **PIN**  
3. Choose from the available options:
   - 💰 **Deposit Money**
   - 🏧 **Withdraw Money**
   - 📜 **View Transaction History**

### 🛡️ For Admins:
1. From the main menu, select **"Admin Login"**  
2. Enter your **admin credentials**  
3. Access the following features:
   - 👥 **View All Users**
   - 🔎 **Search Users**
   - 📊 **View All Transactions**
   - 🧑‍💼 **Create New Admin Accounts**
     

## 🖼️ Screenshots

---

### 🔐 Login Screen  
Initial screen with options for **User Login**.

<img width="727" height="907" alt="login_screen" src="https://github.com/user-attachments/assets/a317526e-29a1-4260-92e2-ba338216a444" />


---

### 🧑‍💼 User Dashboard  
User homepage after login. From here, the user can:
- 💵 Deposit Money  
- 🪙 Withdraw Money  
- 📜 View Transaction History

<img width="568" height="680" alt="user_dashboard" src="https://github.com/user-attachments/assets/958195b3-fe04-4e7b-8788-496912a81e74" />


---

### 💼 Transaction Window  
This screen allows users to:
- 💸 Perform Deposits  
- 💰 Make Withdrawals  
- 📑 View full Transaction History  
All combined into one easy-to-use interface.

![Transaction Window](https://github.com/user-attachments/assets/412977eb-c522-4f42-bf1c-48006e7534b4)


---

### 🛠️ Admin Dashboard  
Initial screen with options for **Admin Login**.
<img width="452" height="722" alt="Admin Dashboard" src="https://github.com/user-attachments/assets/fe26777d-fe38-443f-b6ca-0c46cec9dfe0" />











   

