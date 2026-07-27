# Hands-On 7 – Page Object Model

## Topics Covered

- Base Page
- Page Object Model
- Reusable Page Classes
- pytest
- Selenium WebDriver

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
pytest tests/ -v
```

## Generate HTML Report

```bash
pytest tests/ --html=report.html --self-contained-html
```

## Expected Output

- All tests pass
- No `driver.find_element()` calls in test files
- Reusable page classes
- Clean Page Object Model structure
