# 🏋️ Gym Class Auto Booker (Trust but Verify)

Automate your gym class bookings using **Selenium** and verify that your bookings were actually successful on the “My Bookings” page.  
No more manual clicking — this script books all your favorite slots, handles waitlists, and confirms your success with automatic verification.

---

## 🚀 Features

✅ Automatically logs into your gym portal  
✅ Detects all available class cards on the **Schedule** page  
✅ Books or waitlists classes based on availability  
✅ Handles popups and dynamic elements safely  
✅ Navigates to **My Bookings** and verifies successful bookings  
✅ Provides a complete booking summary and verification report  

---

## 🧠 “Trust but Verify” Concept

This project follows the principle of *Trust but Verify*:
> Don’t just assume your Selenium clicks worked — confirm that your bookings actually appear in your account.

After booking, the script automatically checks the “My Bookings” page and matches your intended bookings against verified results.

---

## ⚙️ Tech Stack

- 🐍 **Python 3.9+**
- 🌐 **Selenium WebDriver**
- 💻 **Google Chrome + ChromeDriver**
- ⏱️ **WebDriverWait** for synchronization
- 📦 `time`, `os`, and `sys` for support utilities

---

## 📋 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/gym-class-auto-booker.git
cd gym-class-auto-booker
