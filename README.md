# Student Event Report Generator

Welcome to the **Student Event Report Generator**! This project automates the process of generating detailed reports (HTML and PDF) for student event data, sorting and analyzing event sequences, and efficiently storing the results. The application leverages asynchronous task processing with Celery to ensure smooth operations without burdening the server.

---

## **Core Features**

1. **Input Data Handling**

   - Accepts a JSON file containing students and the events they completed.
   - Sorts events by the `unit number` and assigns sequential identifiers (`Q1`, `Q2`, etc.) to each event based on its sorted position.

2. **Sequence Generation**

   - Generates a sorted array for each student based on event timestamps.
   - Output format:  
     `[ Q1, Q1, Q2, Q1, Q3, Q1, ... ]`

3. **Report Generation**

   - Asynchronously generates HTML and PDF reports from the sorted data using Celery tasks.
   - Stores the reports in PostgreSQL in binary format for efficient retrieval.

4. **API Endpoints**

   - Submit JSON data for report generation.
   - Retrieve the task status and download generated reports.

5. **Deployment**
   - Fully containerized using Docker Compose for quick and consistent deployment.

---

## **Simplified Workflow**

### **Step 1: JSON Input**

- **Input:** JSON file containing student IDs and events with timestamps and unit numbers.
- **Process:**
  1. Events are sorted by unit number in ascending order.
  2. Sequential identifiers (`Q1`, `Q2`, etc.) are assigned to events.
  3. A function `sequence_generator` generates an output like:
     ```json
     {
       "student_1": ["Q1", "Q2", "Q3"],
       "student_2": ["Q1", "Q1", "Q3"]
     }
     ```

### **Step 2: Asynchronous Task Processing**

- Tasks like HTML and PDF generation are queued using **Celery** to ensure smooth server operations.
- **Redis** acts as the message broker.

### **Step 3: Report Generation**

- HTML reports are generated by the `html_generator` function.
- PDF reports are created using **ReportLab** in the `pdf_generator` function.
- Both reports are stored in PostgreSQL in binary format.

### **Step 4: API Endpoints**

- Submit JSON files, track task status, and retrieve reports via the following endpoints:

  | Endpoint                     | Functionality                                   |
  | ---------------------------- | ----------------------------------------------- |
  | `/assignment/html`           | Accepts JSON data and queues HTML generation.   |
  | `/assignment/html/<task_id>` | Fetches task status or retrieves the HTML file. |
  | `/assignment/pdf`            | Queues PDF generation for JSON input.           |
  | `/assignment/pdf/<task_id>`  | Fetches task status or retrieves the PDF file.  |

---

## **Key Tools and Technologies**

| Tool/Technology                 | Purpose                               |
| ------------------------------- | ------------------------------------- |
| **Django**                      | Backend framework for APIs and logic. |
| **Django REST Framework (DRF)** | Building RESTful APIs.                |
| **PostgreSQL**                  | Storing student data, HTML, and PDFs. |
| **Celery + Redis**              | Asynchronous task handling.           |
| **ReportLab**                   | PDF generation library.               |
| **Flower**                      | Celery task monitoring.               |
| **Docker Compose**              | Deployment of the entire stack.       |

---

## **Deployment**

The project is containerized using Docker Compose for consistent and streamlined deployment. The stack includes:

- Django (with Gunicorn for production-ready WSGI server)
- PostgreSQL (Database)
- Redis (Message broker for Celery tasks)
- Flower (Task monitoring)

To deploy, use the following command:

```bash
docker-compose up --build
```
