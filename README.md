# Vehicle Maintenance Management System

A backend API for managing vehicle maintenance requests, vehicle assignments, maintenance records, and role-based workflows.

The project is designed for a company environment where delivery drivers can report vehicle maintenance issues and authorized employees can review, manage, confirm, and track the maintenance process.

> This project was originally inspired by an internal commercial project for a delivery company. Although the original project was canceled during development, I decided to continue building it independently as a complete backend project and learning experience.

---

## Features

* User registration and authentication
* JWT-based authentication
* Role-based authorization
* Permission-based endpoint protection
* User and role management
* Driver profiles
* Vehicle management
* Driver-to-vehicle assignment
* Maintenance categories
* Maintenance subcategories
* Multiple maintenance items per ticket
* Controlled ticket status transitions
* Vehicle maintenance history
* PostgreSQL database integration
* SQLAlchemy ORM
* Pydantic validation
* Layered backend architecture
* Interactive API documentation

---

# Project Workflow

## User Registration

Users can register an account through the application.

New users receive a default role and can later receive additional responsibilities through administrative role management.

Depending on their responsibilities, users may become:

* Drivers
* Reviewers
* Accountants
* Administrators
* Other authorized roles

---

# Driver and Vehicle Workflow

Drivers can be assigned to vehicles.

When a driver experiences a problem with their vehicle, they can create a maintenance ticket.

The ticket contains information about the required maintenance and the vehicle involved.

A single ticket can contain multiple maintenance items.

For example, a driver may need multiple repairs at the same time. Instead of creating a separate ticket for every repair, one ticket can contain multiple maintenance items, each with its own maintenance information and price.

The total ticket price represents the combined cost of the maintenance items.

---

# Ticket Workflow

The application uses controlled ticket status transitions to prevent invalid workflow changes.

## Open

The driver creates a maintenance request.

The ticket is waiting for review.

---

## Waiting Reply

Additional information is required from the driver.

The driver must review the request and provide the required information before the workflow can continue.

---

## Accepted

The maintenance request has been accepted by the reviewer.

The driver can proceed with repairing the vehicle.

---

## Fixed

The driver confirms that the vehicle has been repaired.

The required documents and evidence can then be submitted for final confirmation.

---

## Waiting for Confirmation

The driver submits the required receipt and supporting evidence.

The ticket is waiting for final validation.

---

## Pending

Additional information or clarification is required before the ticket can be confirmed.

---

## Confirmed

The maintenance process has been successfully reviewed and validated.

Once confirmed:

* The repair is considered completed.
* The maintenance information can be added to the vehicle's maintenance history.

Only confirmed repairs should automatically become part of the vehicle maintenance history.

---

## Closed

A ticket can be closed when the maintenance request does not proceed.

Examples include:

* The request is rejected.
* The driver cancels a ticket created by mistake.

A closed ticket does not necessarily mean that a repair was completed.

---

# Maintenance Management

The application separates maintenance information into categories and subcategories.

This helps keep vehicle maintenance records organized and consistent.

Instead of allowing users to manually enter different versions of the same maintenance operation, the system uses predefined maintenance categories and subcategories.

For example:

```text
Wheel Alignment
Wheel alignment
Wheels Alignment
```

can be represented by one standardized maintenance record.

This improves:

* Data consistency
* Maintenance history accuracy
* Reporting
* Searching
* Future analytics
* Duplicate prevention

---

# Maintenance History

Each vehicle have a maintenance history.

Maintenance history can represent completed maintenance operations associated with the vehicle.

The project separates the concept of:

* Closing a ticket
* Completing a repair
* Confirming a repair

This prevents incorrect maintenance records from being automatically added when a ticket is simply rejected or closed.

---

# Authentication

The API uses JWT authentication.

---

# Authorization and Permissions

Authentication and authorization are handled separately.

Example permissions may follow a format such as:

```text
user:create
user:read
user:update
user:delete
```

Different roles can have different permissions.

---

# Ownership

Permissions and ownership are treated as separate concepts.

A user having permission to access a resource does not automatically mean they should be allowed to access every instance of that resource.

For example, a driver may have permission to work with maintenance tickets while still being restricted to tickets related to their own workflow or assigned vehicle.

---

# Project Architecture

The project follows a layered architecture to separate responsibilities.

```text
API Request
    ↓
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

## Routers

The router layer handles the HTTP API.

Responsibilities include:

* Defining endpoints
* Receiving requests
* Dependency injection
* Calling services
* Returning responses

---

## Services

The service layer contains business logic.

Examples include:

* Workflow validation
* Ticket status transitions
* Business rules
* Authorization decisions
* Application-level validation

---

## Repositories

The repository layer handles database operations.

Examples include:

* Retrieving records
* Creating records
* Updating records
* Deleting records
* Executing database queries

---

## Models

SQLAlchemy models define the database structure and relationships.

---

## Schemas

Pydantic schemas define API requests and responses.

They provide:

* Input validation
* Response validation
* Data serialization
* API documentation

---

# Project Structure

```text
VehicleMaintenance/
│
├── core/
│   ├── config.py
│   └── security.py
│
├── database/
│   ├── database.py
│   └── models.py
│
├── repositories/
│   ├── users_repository.py
│   ├── roles_repository.py
│   ├── driver_user_repository.py
│   ├── vehicle_repository.py
│   ├── ticket_repository.py
│   ├── maintenance_category_repository.py
│   ├── maintenance_subcategory_repository.py
│   └── maintenance_history_repository.py
│
├── routers/
│   ├── users_router.py
│   ├── roles_router.py
│   ├── drivers_router.py
│   ├── vehicle_router.py
│   ├── tickets_router.py
│   ├── maintenance_category_router.py
│   ├── maintenance_subcategory_router.py
│   └── maintenance_history_router.py
│
├── schemas/
│
├── services/
│
├── role_permissions.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# Technology Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT
* pwdlib
* Pytest

---

# Installation

## Clone the repository

```bash
git clone https://github.com/KarimElfar404/VehicleMaintenance.git
```

```bash
cd VehicleMaintenance
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file based on `.env.example`.

---

# Run the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API documentation will then be available at:

```text
/docs
```

ReDoc documentation:

```text
/redoc
```

OpenAPI schema:

```text
/openapi.json
```

---

# API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI can be used to:

* Explore endpoints
* Test API requests
* Send request bodies
* Add authorization tokens
* View API responses

---

# Future Improvements

Potential future improvements include:

* Database migrations with Alembic
* Docker support
* CI/CD
* GitHub Actions
* Logging
* Improved error handling
* File and image storage
* Notification system
* Email notifications
* Reporting and analytics
* Dashboard
* Deployment
* Frontend integration
* Monitoring and observability

---

# Learning Goals

This project was built to apply backend development concepts in a practical application.

The project combines knowledge from:

* Python
* Databases
* SQL
* SQLAlchemy
* PostgreSQL
* Git
* GitHub
* FastAPI
* JWT authentication
* Authorization
* Role-based permissions
* Dependency injection
* Layered architecture
* Automated testing

The goal was not simply to create CRUD endpoints, but to design and implement a backend application with real business workflows and application rules.

---
