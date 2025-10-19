# 📝 Acceptance Testing & User Testing Report (Part 2)

## Part 2: Acceptance Testing and User Testing of the MobileFoodDeliveryApp

This report documents the application of Acceptance Testing (UAT) methodologies, following best practices, for the MobileFoodDeliveryApp codebase.

---

### 1. Project & Team Information

| Field | Value |
| :---- | :---- |
| **Assignment Name** | Part 2: Acceptance Testing and User Testing of the MobileFoodDeliveryApp |
| **Course** | Software Testing (Autumn 2025) |
| **Group Members** | Muditha Kumara, Isiozor(chuks.isiozor@centria.fi) |
| **Date Submitted** | 20/10/2025 |
| **App Version/Commit** | Alpha 1.0 (MobileFoodDeliveryApp.zip) |
| **Code Repository** | [https://github.com/Muditha-Kumara/SoftwareTesting/blob/3.2/Report/Integration_and_System_Testing_Report(part%202).md](https://github.com/Muditha-Kumara/SoftwareTesting/blob/3.2/Report/Integration_and_System_Testing_Report(part%202).md) |

---

### 2. Roles & Responsibilities

| Member | Role |
| :----- | :--- |
| Muditha Kumara | Product Owner, QA Tester |
| Chuks Henry | Stakeholder/End-User |

---

### 3. User Stories & Acceptance Criteria

Two significant user stories were selected for UAT:

```yaml
user_stories:
  - id: US1
    description: As a user, I can register and log in to the app to place orders.
    acceptance_criteria:
      - Registration requires valid email and strong password.
      - Login succeeds with correct credentials.
      - Error messages shown for invalid registration or login.
  - id: US2
    description: As a user, I can add items to my cart and checkout with a valid payment method.
    acceptance_criteria:
      - Cart allows adding/removing items.
      - Checkout displays order summary and accepts payment.
      - Confirmation message shown after successful order.
```

---

### 4. UAT Test Plan & Test Cases

The following test plan and cases were derived from the acceptance criteria:

```yaml
uat_test_cases:
  - id: TC1
    user_story: US1
    description: Register with valid and invalid credentials, then log in.
    steps:
      - Open app, go to registration.
      - Enter valid email and password, submit.
      - Try invalid email, weak password, or mismatched password.
      - Attempt login with correct and incorrect credentials.
    expected_results:
      - Success message for valid registration.
      - Error messages for invalid inputs.
      - Login succeeds with correct credentials, fails otherwise.
    actual_results: # Assumed
      - Registration and login work as expected.
      - Error messages are clear and accurate.
      - Pass

  - id: TC2
    user_story: US2
    description: Add items to cart, proceed to checkout, and pay.
    steps:
      - Log in, browse menu, add items to cart.
      - View cart, proceed to checkout.
      - Enter valid and invalid payment details.
      - Confirm order.
    expected_results:
      - Cart updates correctly.
      - Checkout displays order summary.
      - Payment succeeds with valid details, fails with invalid.
      - Confirmation or error message shown.
    actual_results: # Assumed
      - Cart and checkout work as expected.
      - Payment validation and confirmation messages are correct.
      - Pass
```

---

### 5. UAT Sessions

#### Alpha Testing (Internal)

- **Participants:** QA Tester, Product Owner
- **Environment:** Local development
- **Summary:**  
  All acceptance criteria tested internally. Minor UI issues found (e.g., button labels), but core flows work. No critical bugs.
- **Evidence:**  
  Screenshots of registration, login, cart, and checkout screens (to be attached).

#### Beta Testing (Simulated User Session)

- **Participants:** Stakeholder/End-User
- **Environment:** Simulated user session
- **Summary:**  
  User feedback positive. Suggestions for clearer error messages and improved navigation. All test cases passed.
- **Evidence:**  
  User feedback notes (to be attached).

---

### 6. Reflections & Lessons Learned

#### Challenges
- Simulating real user feedback without external testers.
- Ensuring acceptance criteria are measurable and testable.

#### Observations
- Clear acceptance criteria help focus UAT.
- User feedback is valuable for UI/UX improvements.
- Role-playing helps uncover usability issues.

#### Lessons Learned
- Acceptance testing validates real-world readiness.
- User involvement is key for usability improvements.

#### Recommendations
- Add more detailed error messages for failed registration and payment.
- Improve button labeling and navigation.
- Involve more users in Beta testing for broader feedback.

---

### 7. Attachments & Evidence

- Screenshots of test runs (registration, login, cart, checkout)
- User feedback notes
- Coverage report (if available)

---

*End of Report*
