# Fleet Management System

This is a Fleet Management System built using Django and PostgreSQL. The system is designed to manage vehicle fleets, maintenance schedules, and driver records. The primary goal of this project is to ensure efficient fleet management while providing a user-friendly interface for administrators and authorized users.

## Features

- **Vehicle Management**: 
  - Add, update, delete, and view vehicle details such as name, license plate, vehicle type, and creation date.
  - Track vehicle maintenance schedules and records.
  
- **Driver Management**:
  - Add, update, delete, and view driver details including name, license number, and vehicle assignments.
  
- **Authentication & Security**:
  - User authentication and session management for secure access to the system.
  - Role-based access control to allow only authorized users to perform certain actions.

- **Responsive UI**: 
  - Simple and intuitive web interface built using Django templates and CSS.

- **Data Persistence**: 
  - PostgreSQL as the database to store vehicle and driver data.
  
- **Automatic Logout**: 
  - User session expires after 10 minutes of inactivity.

## Installation

### Prerequisites

- Python 3.8 or above
- Django 3.0 or above
- PostgreSQL

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <project_directory>
