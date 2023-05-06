# Django E-commerce App
This project is an ecommerce web application built with Django and Django Rest Framework (DRF). It provides a user-friendly interface for customers to browse and purchase products online, and an easy-to-use administration panel for store owners to manage their inventory, orders, and customers.
Some of the key features of the app include:

- User authentication and authorization
- Product catalog with search, filtering, and sorting options
- Shopping cart and checkout functionality
- Payment integration with popular services like Stripe or PayPal
- Order tracking and history for customers
- Dashboard with sales and inventory reports for store owners

The app is designed to be scalable and customizable, with a modular architecture that allows developers to add or remove features as needed. It also follows best practices for security, performance, and accessibility, ensuring a seamless user experience for both customers and store owners.

# Getting Started

## Prerequisites
Before running the project, you need to have the following software or tools installed:
- python
- pip
- git


## Installation
To install and run the project, follow these steps:

1. Clone this [repo](https://www.example.com): `git clone https://github.com/duaasayed/drf-ecommerce-api.git`
2. In the project dir:
    - Create a new virtual env: `python3 -m venv venv`
    - Activate the virtual env: `source venv/bin/activate`
    - Install dependencies: `pip install -r requirements.txt`
3. Copy core/.env.example it core/.env and set your config
4. Run migrations: `python3 manage.py migrate`
5. Now you are ready to start running the project: `python3 manage.py runserver`


# Features
## Customers' Accounts:
Allows customers to have an account in the application and use it to manage their carts, orders...

- Signup.
- Email Verification (you'll need to set mail configs).
- Token-based Authentication
- Forget/Reset password.
- Two-factor authentication (if customer enables it).
- Logout

## Shop:
Allows customers to browse the products catalog and see products details

- Browse products
- Filter products with category
- Filter products with price range
- Filter products with brand
- Filter products with store
- Show specific product details
- Show products reviews/rating
- Show asked questions related to products and their answers
- Show specific category details
- Show specific brand details
- Show specific store details
- Top 10 best sellers for each category
- Top 10 new arrivals for each category
- Add to cart

## Cart:
Allows customer to add products to their cart and manege them later (update, delete, checkout)

- Add to cart
- Edit wanted quantity
- Remove product from cart
- Chackout

## Orders:
Allows customers to manage their orders

- Checkout/place a new order
- Show order history
- Ability to cancel orders
- Show specific order details

## Profiles
Allows customers to manage their information and preferences

- Add their address to deliver orders to
- Enable/disable Two-factor authentication

## Sellers' Dashboard:
Allows Stores representatives to manage their data (products, orders,...)

- Login with their pre-created acccounts
- Manage products (add, update, show, delete)
- Manage orders (show, update status for order tracking)
- Manage representatives (ability to add many representative for each store)
- Manage representatives' permissions


# Built with
The project was built using the following technologies, frameworks, and libraries:
- Django, Django Rest Framework

# Contact
If you have any questions or feedback about the project, please contact us at:
- [E-mail](mailto:doaas0213@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/douaa-sayed/)

# Authors
- Doaa Sayed

# References
This project was inspired by the following articles, papers, or resources:

- Created features inspired by [amazon.eg](https://www.amazon.eg/)

# Disclaimer
This project is provided as-is and with no warranty or guarantee of fitness for any purpose. Use at your own risk.

