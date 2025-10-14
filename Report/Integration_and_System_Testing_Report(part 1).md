# 📝 Integration and System Testing Report (Part 1)

## Part 1: Integration and System Testing of the MobileFoodDeliveryApp

This report documents the application of integration and system testing methods, following best practices, for the MobileFoodDeliveryApp codebase.

### 1. Project & Team Information

| Field | Value |
| :---- | :---- |
| **Assignment Name** | Part 1: Integration and System Testing of the MobileFoodDeliveryApp |
| **Course** | Software Testing (Autumn 2025) |
| **Group Members** | Muditha Kumara ([muditha.kumara@centria.fi](mailto:muditha.kumara@centria.fi)), Chuks Henry |
| **Date Submitted** | 15/10/2025 |
| **App Version/Commit** | Alpha 1.0 |
| **Code Repository** | https://github.com/Muditha-Kumara/SoftwareTesting/tree/2.1.phase1 |

### 2. Roles & Responsibilities

| Member | Role |
| :----- | :--- |
| Muditha Kumara | Test Lead, Integration Specialist |
| Chuks Henry | System Tester |

### 3. Integration Testing

#### 3.1. Strategy Chosen

**Approach:** Top-Down Integration Testing

**Rationale:** This approach allows us to validate the main application flow early, using stubs for unfinished lower-level modules (e.g., Payment and Notification services). It helps catch integration issues at the user interface and controller level before moving to backend details.

#### 3.2. Modules & Sequence

| Sequence | Module | Stub/Driver Used |
| :------- | :----- | :-------------- |
| 1 | Application Controller (main.py) | Stubs for PaymentProcessing, NotificationService |
| 2 | Order Placement (Order_Placement.py) | Real module |
| 3 | Payment Processing (Payment_Processing.py) | Stubbed responses |

#### 3.3. Test Scenarios & Results

| Test Case | Description | Expected Result | Actual Result | Pass/Fail |
| :-------- | :---------- | :-------------- | :------------ | :-------- |
| TC1 | Place order with valid cart and payment | Order confirmed, payment processed | Success, order ID returned | Pass |
| TC2 | Place order with invalid payment (stubbed failure) | Payment declined, order not confirmed | Failure message shown | Pass |
| TC3 | Place order with unavailable menu item | Error message, order not placed | Error shown | Pass |

#### 3.4. Key Findings
- Top-down integration exposed UI-to-backend communication issues early.
- Stubbing PaymentProcessing allowed simulation of both success and failure cases.
- Error handling for unavailable items and payment failures worked as expected.

### 4. System Testing

Each member performed one functional and one non-functional test on a selected module.

#### 4.1. Functional Tests

| Member | Module | Test Case | Acceptance Criteria | Result |
| :----- | :----- | :-------- | :----------------- | :----- |
| Muditha Kumara | Payment_Processing.py | Valid credit card processes payment | Payment succeeds, transaction ID returned | Pass |
| Chuks Henry | Order_Placement.py | Add item to cart and place order | Item added, order confirmed | Pass |

#### 4.2. Non-Functional Tests

| Member | Aspect | Test Type | Metric/Tool | Criteria | Result |
| :----- | :----- | :-------- | :---------- | :------- | :----- |
| Muditha Kumara | Performance | Simulate 50 concurrent orders | Python threading, response time | <2s per order | Pass |
| Chuks Henry | Usability | Heuristic evaluation of checkout | User feedback, checklist | No critical usability issues | Pass |

### 5. Reflections & Lessons Learned

#### 5.1. Challenges
- Creating realistic stubs for PaymentProcessing required careful design.
- Ensuring test isolation between integration and system tests.

#### 5.2. Observations
- The top-down approach helped catch integration bugs early.
- System tests confirmed both functional correctness and non-functional quality.

#### 5.3. Lessons Learned
- Integration testing is essential for validating module interactions, not just individual correctness.
- Non-functional testing (performance, usability) is critical for real-world readiness.

### 6. Attachments & Evidence
- Screenshots of test runs and coverage reports (see attached images).
- Sample output logs from performance and usability tests.

---

*End of Report*
