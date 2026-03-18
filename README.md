# Django Invoice Dashboard

A full-stack invoice management system built with Django that allows users to create, manage, and send invoices efficiently. The application streamlines the invoicing process by automating PDF generation and email delivery.

## 🚀 Features

- Create and manage clients  
- Generate and manage invoices  
- Add line items dynamically (services, quantities, pricing)  
- Automatically calculate totals  
- Generate professional PDF invoices  
- Preview invoices directly in the browser  
- Download invoices as PDF  
- Send invoices via email  
- Admin authentication system  
- Clean dashboard interface  

## 🛠 Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** SQLite (development)  
- **PDF Generation:** WeasyPrint  
- **Email Integration:** SMTP  

## 📦 Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the repository

    git clone https://github.com/danieljcave/invoice-dashboard.git
    cd invoice-dashboard

### 2. Create a virtual environment

    python3 -m venv env
    source env/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Create environment variables

Create a `.env` file in the root directory and add:

    DEBUG=1
    ENVIRONMENT=dev
    SECRET_KEY=your-secret-key

### 5. Apply migrations

    python manage.py migrate

### 6. Create a superuser

    python manage.py createsuperuser

### 7. Run the development server

    python manage.py runserver

Then open:

    http://127.0.0.1:8000

## 📄 Usage

- Log in with your superuser account  
- Add clients and associated details  
- Create invoices with line items  
- View invoice details in the dashboard  
- Preview invoices as PDFs in-browser  
- Download or email invoices directly  

## 📸 Screenshots

<details>
        <summary>Click to Open to view Screenshots</summary>
        <br></br>
        <p><b>Welcome Page</b></p>
        <img src="/screenshots/welcome_page.png">
        <br></br>
        <p><b>Invoice Dashboard</b></p>
        <img src="/screenshots/invoice_dashboard.png">
        <br></br>
        <p><b>Invoice Detail</b></p>
        <img src="/screenshots/invoice_detail.png">
        <br></br>
        <p><b>Invoice Edit</b></p>
        <img src="/screenshots/invoice_edit.png">
        <br></br>
        <p><b>Invoice Delete</b></p>
        <img src="/screenshots/invoice_delete.png">
        <br></br>
        <p><b>Client Dashboard</b></p>
        <img src="/screenshots/client_dashboard.png">
        <br></br>
        <p><b>Client Edit</b></p>
        <img src="/screenshots/client_edit.png">
        <br></br>
        <p><b>Client Delete</b></p>
        <img src="/screenshots/client_delete.png">
        <br></br>
        <p><b>Dog Dashboard</b></p>
        <img src="/screenshots/dog_dashboard.png">
        <br></br>
        <p><b>Dog Edit</b></p>
        <img src="/screenshots/dog_edit.png">
        <br></br>
        <p><b>Dog Delete</b></p>
        <img src="/screenshots/dog_delete.png">
        <br></br>
        <p><b>Dog Walks Counter</b></p>
        <img src="/screenshots/dog_walk_counter.png">
        <br></br>
        <p><b>Invoice PDF</b></p>
        <img src="/screenshots/pdf_view.png">
    </details>

## 💡 Project Purpose

This project was built to demonstrate full-stack development skills using Django, focusing on solving a real-world problem by automating manual invoicing workflows. It highlights backend logic, database design, PDF generation, and user interface development.

## 🔮 Future Improvements

- User roles and permissions  
- Payment tracking  
- Invoice status (paid/unpaid)  
- Search and filtering  
- REST API integration  
- Deployment to a cloud platform  

## 📌 Notes

- This project is configured for local development using SQLite  
- Sensitive data and environment variables are excluded from version control  