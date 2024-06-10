# Invoice Processing Application

This application processes invoice data, calculates totals, and sends email reminders to customers. It uses Django for the backend, Celery for task processing, and Redis as the message broker.

## Prerequisites

- Python 3.9
- Django 4.2.13
- Celery
- Redis
- Pandas
- Node.js and npm (for React)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/invoice-processing.git
    cd invoice-processing
    ```

2. Create and activate a virtual environment:

    ```sh
    python3.9 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the project root with the following content:

    ```sh
    REMITTENT_EMAIL=your-email@gmail.com
    REMITTENT_PASSWORD=your-email-password
    ```

5. Install Node.js and npm:

    - **For Windows and macOS**: Download and install Node.js from the [official website](https://nodejs.org/).
    - **For macOS with brew**:

        ```sh
        brew install node
        ```
    - **For Ubuntu**:

        ```sh
        curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
        sudo apt-get install -y nodejs
        ```

6. Install the required Node.js packages for the React frontend:

    ```sh
    cd revving-app
    npm install
    npm run build
    cd ..
    ```

    This will install the necessary packages, including React and Axios, and build the frontend.


## Running the Unit Tests

To run the unit tests, use the following command:

```sh
python manage.py test app.tests
```

This will execute the tests defined in the app/tests/ directory.

## Starting the Server
To start the Django development server, use the following command:

```sh
python manage.py runserver
```
The server will be available at http://127.0.0.1:8000/.

## Importing the Data
To import invoice data, follow these steps:

### Run Redis
```sh
redis-server
```

### Start the Celery worker:

```sh
celery -A your_project_name worker --loglevel=info
```
Open the web application in your browser and navigate to the upload page (e.g., http://127.0.0.1:8000/).

### Upload the Excel file containing the invoice data. The file should have the following columns:

- date
- invoice number
- value
- haircut percent
- Daily fee percent
- currency
- Revenue source
- customer
- Expected payment duration

## Displaying the Results
After uploading the data, you can view the results as follows:

### Invoice Totals:
Navigate to http://127.0.0.1:8000/ to see the total values for each revenue source.

### All Invoices:
Click the "View All Invoices" button on the home page to see the list of all invoices. This page supports pagination to display 20 invoices per page.

### API Endpoints

- Upload Invoices: POST http://127.0.0.1:8000/api/upload-invoice/
- Get Invoice Totals: GET http://127.0.0.1:8000/api/invoice-totals/
- Get All Invoices: GET http://127.0.0.1:8000/api/invoices/
- Send Reminder Emails: GET http://127.0.0.1:8000/api/send-emails/

### Sending Reminder Emails (On testing phase)
To send reminder emails to all customers, use the following endpoint, would be nice to do it periodically with redis-beat:

```sh
http://127.0.0.1:8000/api/send-emails/
```
This will queue a Celery task to send reminder emails to all customers.