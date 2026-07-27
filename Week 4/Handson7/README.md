# Hands-On 7 – Page Object Model (POM)

## Objective

Implement Selenium automation using the Page Object Model design pattern.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
pytest -v
```

## Project Structure

```
HandsOn7/
│
├── pages/
│   └── home_page.py
│
├── tests/
│   └── test_home.py
│
├── conftest.py
├── requirements.txt
└── README.md
```

## Concepts Covered

- Selenium WebDriver
- Page Object Model
- pytest
- Fixtures
- Explicit Wait
- Assertions

## Expected Output

- Browser launches
- Selenium homepage opens
- Title verified
- Heading displayed
- Downloads page opened
- Test passes
- Browser closes automatically
