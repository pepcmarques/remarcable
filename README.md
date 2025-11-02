# Remarcable - Assignment Documentation

## Overview

This application is result of a assignment which requested a simple Django project that models products, categories, and tags.

## Goals

- Create Django models with correct relationships.
- Populate the database using Django's admin interface.
- Implement search and filter functionality.
- Build an HTML page for user interaction.
- Demonstrate proficiency in writing Django queries.

## Requirements

### Data Population

- Use the Django admin interface to populate the database with sample data.
- Create at least 5 categories, 10 tags, and 20 products.
- Search and Filter Functionality
- Create a simple HTML page that allows users to:
  - Search products by description.
  - Filter products by category.
  - Filter products by tags.
  - Users should be able to combine search and filter options.

### Front-End

- To use Django templates or any front-end framework of your choice.
- The design and styling are not important.
- The focus is on functionality and query implementation.

### Deliverables

- A complete Django project with all source code.
- A README.md (this) file that includes:
  - Instructions on how to set up and run the project.
  - Any assumptions or additional notes.
  - If using a front-end framework, include build instructions.

## Versions and libraries

- Python (3.11.1)
- Django (5.2.7)
- djangorestframework (3.16.1)

## Instructions

### How to run this project

1. Clone this project

```
git clone https://github.com/pepcmarques/remarcable.git
```

2. Go to the `remarcable` directory

```
cd remarcable
```

3. Install a Python virtualenv

The installation depends on your operational system

```
python -m venv .venv   # Mac or Linux (perhaps it needs to be: python3 -m venv .venv)

py -3 -m venv .venv    # Windows
```

4. Activate the `virtual environment`

```
source .venv/bin/activate     # For Linux or Mac

.venv\Scripts\activate        # For Windows
```

5. Install dependencies

```
pip install -r requirements.txt
```

6. Run the project

```
python manage.py runserver   # Mac or Linux

py -3 manage.py runserver    # Windows
```

7. Open a browser and type on the URL: `http://127.0.0.1:8000/`

### Configuring

1. Creating a superuser

Stop the running service by pressing `control-c`, and run:

```
python manage.py createsuperuser
```

Follow the instructions to create the super user.

To enter in the admin environment, open the browser and navigate to `http://127.0.0.1:8000/admin`

### Populating the database.

The database is pre-populated. However if you have any problems, follow the steps below:

1. Delete the `db.sqlite3` file
2. From the project root, run:

- Mac or Linux
```
python manage.py migrate

python manage.py populatedb 
```

- Windows
```
py -3 manage.py migrate

py -3 manage.py populatedb 
```

**OR**

1. Populate the database manually by accessing `http://127.0.0.1:8000/admin`
2. Enter the credentials previously created
3. Clicking on `Categories`, `Tags`, or `Products` and add the correspondant data

## Assumptions

1. Using `pip` as package manager
2. The search by "description" was modified by "name" or "description" to create a composition of queries - speciffically using `OR` logical operator.
3. Products Model has `price` field. Usually, I wouldn't use `price` in the same model as `product`, because I understand that is necessary keeping historic values. However, it was used to show how to create constraints.
4. Products Model has `stock_count`. It is not being used, but it could be used for showing products in stock only. This is a business decision.
5. Although I am using `icontains` for searching part of the name and part of the description, I would use a vector database - to use embeddings - and make it possible to search for **similar** names and/or descriptions.

## Notes

- There is a Django command to populate the database `python manage.py populatedb` with initial data, described on the `Populating Database` section
- I created the `.gitignore` file using `https://gitignore.io`
- I decided to use Django template, instead of a different frontend framework to simplifying installlation and running - I would use Next.JS.
- I am not using API calls for this assignment, but as an **extra feature**, I used Django Rest Framerwork to create a search endpoint `http://127.0.0.1:8000/api/search/`. By using this search endpoint you can use names, instead of objects. See example on the next section.
- Both, form and api, use a service in `services.py`

## API Endpoints

### Search Product

Retrieves the products based on a search.

**Endpoint:** `/api/search/`

**Method:** `POST`

**Request Body:**

The request body should be a JSON object with the following properties:

| Property | Type | Required | Description |
|---|---|---|---|
| `search` | `string` | No | Text containing part of the Name or description of a product. |
| `category` | `string` | No | Category name. |
| `tags` | `list of strings` | No | List of tags of a product. |

**Example Request Body:**

```json
{
  "search": "wrench",
  "category": "Tools",
  "tags": ["DIY"]
}
```

**Example Response:**

```json
[
    {
        "id": 99,
        "name": "Adjustable Wrench",
        "description": "An adjustable wrench with a wide jaw capacity, designed for turning nuts and bolts of different sizes, built with chrome vanadium steel for strength and longevity.",
        "price": "14.99",
        "category": "Tools",
        "tags_list": [
            "DIY",
            "Durable",
            "Eco-friendly"
        ]
    }
]
```

## Artificial Intelligence (AI)

I used AI to:

- Create the `data.json` file. However, I fixed it later because there were some products' tags that didn't exist in `tags`.
- Create initial CSS file, and styling. I had to tweek it a bit.
