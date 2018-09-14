# Shopify Internship Challenge
> Submission by Jordan Dearsley (SoftEng UWaterloo)

This project was built using Django and Django-graphene. I haven't used GraphQL before so please forgive any conventions best practices, etc. I haven't followed! I've tried my best to follow the provided documentation.

This project is live and deployed via Kubernetes as of this commit. Please see the [Demo](#demo) section to access it.

# Table of Contents
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Demo](#demo)
- [API](#api)
    - [Subthing](#product)
- [Testing](#testing)

## Prerequisites

- Python 3.5+
- PostgresQL installed and running on host
- DB with name "shopdb" created with proper permissions
- Django and any other pip dependencies it complains about during startup (I will put together a virtual env if I get the chance!)

## Installation and Setup

Clone the repo as-is, and in the root directory, run:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
If that doesn't work, try praying and/or doing a good deed before running again.

## Demo

Login
A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

## API

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

## Testing

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.
