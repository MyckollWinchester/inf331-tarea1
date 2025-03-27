# Inventory Application

This is an inventory management application built with Flask. It provides functionalities for managing products and user authentication.

## Project Structure

```
inf331-tarea1
├── src
│   ├── app.py                # Main entry point for the Flask application
│   ├── models                # Directory for data models
│   │   ├── __init__.py
│   │   ├── product.py        # Product model for SQLite3
│   │   └── user.py           # User model for authentication
│   ├── controllers           # Directory for route controllers
│   │   ├── __init__.py
│   │   ├── product_routes.py  # CRUD routes for products
│   │   └── user_routes.py     # Authentication routes
│   ├── services              # Directory for business logic
│   │   ├── __init__.py
│   │   ├── product_service.py  # Logic for managing products
│   │   └── user_service.py     # Logic for user authentication
│   ├── utils                 # Directory for utility functions
│   │   ├── __init__.py
│   │   ├── logger.py          # Logger configuration
│   │   └── security.py        # Security functions
│   ├── tests                 # Directory for unit tests
│   │   ├── test_app.py        # Tests for the application
│   │   ├── test_products.py    # Tests for product operations
│   │   └── test_users.py       # Tests for user authentication
│   ├── static                # Directory for static files (CSS, JS, images)
│   └── templates             # Directory for HTML templates
├── requirements.txt          # List of required libraries
├── README.md                 # Project documentation
├── inventory.db              # SQLite3 database (optional)
└── logs/app.log             # Application logs
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd inf331-tarea1
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.