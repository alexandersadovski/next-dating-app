# Next – A Modern Django Dating App

**Next** is a sleek, user-friendly dating application built with Django, designed to connect people through intuitive swiping, mutual matches, and meaningful conversations.

---

## 🧩 Key Features

### 👤 User Profile Management

- **Registration**: Users can sign up and create personalized profiles.  
- **Customization**: Edit or delete profiles as needed.  
- **Password Management**: Secure password change functionality.

### 💘 Matchmaking

- **Swiping Mechanism**: Swipe through profiles to express interest.  
- **Mutual Matches**: Users who like each other are matched and can connect.  
- **Messaging**: Engage in conversations with your matches.

### 💬 Chat Features

- **Conversations List**: View all ongoing conversations in one place.  
- **Real-Time Messaging**: Seamless, real-time chat with matches.  
- **Conversation Management**: Option to delete conversations when needed.

### 🚩 Reporting System

- **User Reporting**: Report inappropriate behavior or concerns.  
- **Report Tracking**: Monitor the status of reports — **Pending**, **Resolved**, or **Dismissed**.

### 🔧 Admin Panel

- **Report Review**: Admins can review and manage user reports.  
- **Status Management**: Update and track the status of reports.

---

## 🛠️ Technology Stack

- **Backend**: Django  
- **Frontend**: HTML, CSS, Django Template Language (DTL), JavaScript (AJAX)  
- **Database**: PostgreSQL

---

## 🔄 How It Works

1. **Sign Up**: Create a user profile.  
2. **Swipe**: Like or pass on other users' profiles.  
3. **Match**: If both users like each other, a match is created.  
4. **Chat**: Start a conversation with your match.  
5. **Report**: Flag inappropriate behavior and track its resolution.

---

## 🟢 Getting Started

Follow these steps to set up the project locally:

```bash
# 1️⃣ Clone the repository
git clone https://github.com/alexandersadovski/next-dating-app.git
```

```bash
# 2️⃣ Navigate to the project directory
cd next-dating-app
```

```bash
# 3️⃣ Set up and activate a virtual environment
python -m venv venv              # Create a virtual environment
source venv/bin/activate         # On macOS/Linux
venv\Scripts\activate            # On Windows
```

```bash
# 4️⃣ Install dependencies
pip install -r requirements.txt
```

```bash
# 5️⃣ Apply database migrations
python manage.py migrate
```

```bash
# 6️⃣ (Optional) Create an admin superuser
python manage.py createsuperuser
```

```bash
# 7️⃣ (Optional) Create a report reviewer (staff) account
python manage.py createreportreviewer
```

```bash
# 8️⃣ (Optional) Populate the database with mock users
python manage.py populate_users
```

```bash
# 9️⃣ Start the development server
python manage.py runserver
# ✅ You're all set! Access the project at: http://127.0.0.1:8000/
```
