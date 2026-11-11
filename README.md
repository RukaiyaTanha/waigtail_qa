# Wagtail Bakerydemo QA Automation Framework

UI and API test automation for [Wagtail Bakerydemo](https://github.com/wagtail/bakerydemo), a demo website built with the Wagtail CMS. The framework uses Python, Selenium, and Pytest with the Page Object Model (POM) for UI automation, and Postman/Newman for API testing. Jenkins is used for CI/CD integration.

## Automation Coverage

| Testing Type | Tool | Test Cases |
|---|---|---:|
| UI Automation | Selenium, Pytest | 20 |
| API Testing | Postman, Newman | 20 |
| UI Test Reports | pytest-html | HTML Report |
| API Test Reports | Newman HTML Extra | HTML Report |
| CI/CD | Jenkins | Pipeline |

The UI test suite covers CMS page management, while the API collection covers Wagtail API v2 endpoints.

The UI HTML report is generated as `reports/report.html` after each test run.

The Newman HTML report is generated as `reports/newman-report.html` after API execution.

## What Is Tested

### UI Automation

| Area | Scenarios |
|---|---|
| Page Management | Create a page, empty-title validation, maximum-length title, edit page title, update introduction, save draft |
| Publishing | Preview draft, publish page, edit published page, submit page for moderation, approve page, request changes |
| Page Operations | Unpublish page, delete draft, restore previous revision, copy page, cancel deletion |
| Navigation and Access | Unauthorized page creation, automatic slug generation, search pages, compare revisions |

### API Testing

| Area | Scenarios |
|---|---|
| Pages API | Get all pages, get a page by ID, retrieve specific fields, pagination, filter by page type, search pages |
| Negative Testing | Nonexistent page ID, invalid page ID, invalid API endpoint, unsupported response format, invalid query parameters |
| Media API | Get all images, get all documents |
| Write Operation Validation | Attempt to create, update, and delete pages through the API |
| Custom API | Get all persons, search persons |
| Performance | Verify API response time |

The API tests use Wagtail API v2 endpoints. The standard page API is read-only, so the POST, PATCH, and DELETE tests verify that unsupported write operations are rejected.

## Tech Stack

- Python 3.10.11
- Selenium WebDriver
- Pytest
- pytest-html
- Page Object Model (POM)
- Postman
- Newman 6.2.3
- Newman HTML Extra Reporter
- Wagtail CMS
- Django
- Jenkins
- Git, GitHub
- Google Chrome


## CI/CD

The `Jenkinsfile` is used to configure the **Wagtail-Bakery-QA-Pipeline** job.

The pipeline is intended to:

1. Check the Python and Git environments.
2. Verify that the local Wagtail application is reachable.
3. Set up the Python virtual environment.
4. Install Python dependencies.
5. Run the Selenium UI automation suite.
6. Generate the UI HTML report.
7. Execute API tests using Newman.
8. Generate the Newman HTML report.
9. Archive test reports as Jenkins build artifacts.

The project is maintained on GitHub, with Jenkins used for automated test execution and reporting.

## Test Reporting

Both UI and API automation generate separate HTML reports.

| Report | File |
|---|---|
| Selenium UI Report | `reports/report.html` |
| Newman API Report | `reports/newman-report.html` |

These reports provide test execution details and help identify failed test cases during development and CI/CD execution.

## Project Focus

This project focuses on testing Wagtail CMS functionality from both the user interface and API perspectives. It covers page creation and publishing workflows, revision management, content search, API filtering, pagination, negative testing, and response-time validation.