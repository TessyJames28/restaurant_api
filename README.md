# Restaurant Management System API

This repository contains the API for a restaurant management system. The API allows for user registration, user authentication, menu item management, user group management, cart management, and order management. The API follows RESTful principles and returns appropriate HTTP status codes for error handling.

## User Groups

The following user groups are available in the system:

- Manager
- Delivery Crew

Users not assigned to a group will be considered customers.

## User Roles

The API displays error messages with appropriate HTTP status codes for specific errors. Here is a list of the HTTP status codes used:

- 200 - Ok: For all successful GET, PUT, PATCH, and DELETE calls.
- 201 - Created: For all successful POST requests.
- 403 - Unauthorized: If authorization fails for the current user token.
- 401 - Forbidden: If user authentication fails.
- 400 - Bad request: If validation fails for POST, PUT, PATCH, and DELETE calls.
- 404 - Not found: If the request was made for a non-existing resource.

## API Endpoints

### User Registration and Token Generation Endpoints

- POST `/api/users`: Creates a new user with name, email, and password.
- GET `/api/users/users/me/`: Displays only the current user.
- POST `/token/login/`: Generates access tokens that can be used in other API calls.

### Menu Items Endpoints

- GET `/api/menu-items`: Lists all menu items (available to customers and delivery crew).
- POST, PUT, PATCH, DELETE `/api/menu-items`: Denies access and returns 403 - Unauthorized.
- GET `/api/menu-items/{menuItem}`: Lists a single menu item (available to customers and delivery crew).
- POST, PUT, PATCH, DELETE `/api/menu-items/{menuItem}`: Returns 403 - Unauthorized.
- GET `/api/menu-items` (Manager): Lists all menu items.
- POST `/api/menu-items` (Manager): Creates a new menu item and returns 201 - Created.
- GET `/api/menu-items/{menuItem}` (Manager): Lists a single menu item.
- PUT, PATCH `/api/menu-items/{menuItem}` (Manager): Updates a single menu item.
- DELETE `/api/menu-items/{menuItem}` (Manager): Deletes a menu item.

### User Group Management Endpoints

- GET `/api/groups/manager/users` (Manager): Returns all managers.
- POST `/api/groups/manager/users` (Manager): Assigns a user to the manager group and returns 201 - Created.
- DELETE `/api/groups/manager/users/{userId}` (Manager): Removes a user from the manager group.
- GET `/api/groups/delivery-crew/users` (Manager): Returns all delivery crew.
- POST `/api/groups/delivery-crew/users` (Manager): Assigns a user to the delivery crew group and returns 201 - Created.
- DELETE `/api/groups/delivery-crew/users/{userId}` (Manager): Removes a user from the delivery crew group.

### Cart Management Endpoints

- GET `/api/cart/menu-items` (Customer): Returns current items in the cart for the current user token.
- POST `/api/cart/menu-items` (Customer): Adds a menu item to the cart.
- DELETE `/api/cart/menu-items` (Customer): Deletes all menu items created by the current user token.

### Order Management Endpoints

- GET `/api/orders` (Customer): Returns all orders with order items created by the user.
- POST `/api/orders` (Customer): Creates a new order item for the user, adds cart items to the order, and clears the cart.
- GET `/api/orders/{orderId}` (Customer): Returns all items for the order. Displays an error if the order ID doesn't belong to the user.
- GET `/api/orders` (Manager): Returns all orders with order items by all users.
- PUT, PATCH `/api/orders/{orderId}` (Customer): Updates the order. Managers can set a delivery crew and update the order status.
- DELETE `/api/orders/{orderId}` (Manager): Deletes an order.
- GET `/api/orders` (Delivery Crew): Returns all orders with order items assigned to the delivery crew.
- PATCH `/api/orders/{orderId}` (Delivery Crew): Updates the order status.

## Getting Started

To use the Restaurant Management System API, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary dependencies.
3. Set up your database and configure the connection settings.
4. Run the API and make requests to the appropriate endpoints.
