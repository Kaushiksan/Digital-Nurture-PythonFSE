# Hands-On 3 – Test Automation Process & Framework Types

## Name
Kaushik A

---

# Task 1: Test Automation Process

## What is Test Automation?

Test Automation is the process of using software tools to execute test cases automatically, compare actual and expected results, and generate reports.

### Test Automation Process

1. Requirement Analysis
2. Tool Selection
3. Framework Design
4. Test Script Development
5. Test Execution
6. Report Generation
7. Maintenance

---

# Task 2: Types of Automation Frameworks

## 1. Linear Framework

- Test scripts are written sequentially.
- Easy to create.
- Suitable for small projects.

### Advantages
- Simple
- Easy to understand

### Disadvantages
- Poor reusability
- Difficult to maintain

---

## 2. Modular Framework

- Application is divided into independent modules.
- Each module has separate test scripts.

### Advantages
- Better code reuse
- Easier maintenance

### Disadvantages
- Initial design effort is higher

---

## 3. Data-Driven Framework

- Test data is stored separately (Excel, CSV, JSON, etc.).
- The same script runs with multiple datasets.

### Advantages
- High reusability
- Easy testing with multiple inputs

### Disadvantages
- More complex implementation

---

## 4. Keyword-Driven Framework

- Test steps are represented by predefined keywords.

Example:

| Keyword | Action |
|----------|---------|
| Open Browser | Launch browser |
| Click | Click a button |
| Enter Text | Type input |
| Verify | Validate output |

### Advantages
- Minimal coding
- Easy for testers

### Disadvantages
- Higher initial setup effort

---

## 5. Hybrid Framework

Hybrid Framework combines two or more automation frameworks (for example, Data-Driven + Keyword-Driven).

### Advantages

- Highly scalable
- Flexible
- Widely used in industry

### Disadvantages

- More complex architecture

---

# Task 3: Test Pyramid

```
          UI Tests
       (Few, Slow)

   Integration Tests
   (Moderate Number)

 Unit Tests
(Many, Fast)
```

### Explanation

- Unit Tests are fast, inexpensive, and should be the largest portion.
- Integration Tests verify communication between modules.
- UI Tests are slower and should be fewer in number.

---

# Task 4: Choosing an Automation Strategy

## Scenario

A large e-commerce website releases updates every two weeks and has many regression test cases.

### Recommended Framework

**Hybrid Framework**

### Reason

- Supports reusable components
- Enables data-driven testing
- Easier maintenance
- Scales well for large applications
- Suitable for continuous integration and Agile development

---

# Task 5: Benefits of Test Automation

- Faster execution
- Reduced manual effort
- Increased accuracy
- Reusable test scripts
- Better regression testing
- Continuous Integration support
- Faster feedback
- Improved software quality

---

# Task 6: Limitations of Test Automation

- Initial setup cost
- Requires programming knowledge
- Maintenance needed when UI changes
- Not suitable for exploratory testing
- Some scenarios still require manual testing

---

# Conclusion

This hands-on covered:

- Test Automation Process
- Automation Frameworks
- Test Pyramid
- Framework Selection
- Benefits and Limitations of Automation

**Status:** Completed
