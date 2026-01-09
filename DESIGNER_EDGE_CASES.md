# Designer Agent - Edge Case Handling Guide

## Overview

The Designer agent has been enhanced with **explicit edge case handling** for scenarios where acceptance criteria is missing, blank, or in non-standard formats.

---

## The 4 Edge Cases & How Designer Handles Them

### CASE 1: ❌ NO ACCEPTANCE CRITERIA PROVIDED (Empty/Blank)

**Scenario:** User story exists but has NO acceptance criteria field

**What Designer Does:**
1. **STOPS and REJECTS the story** ⛔
2. Returns error: "REJECTION: No acceptance criteria provided"
3. Requests Architect to:
   - Define acceptance criteria in Given-When-Then format
   - Provide at least 3 concrete acceptance criteria
   - Clarify happy path, edge cases, error scenarios

**Output:**
```json
{
  "story_status": "REJECTED",
  "acceptance_criteria_status": "REJECTED - MISSING CRITERIA",
  "rejection_reason": "No acceptance criteria provided - story is not testable",
  "test_cases": [],
  "validation_errors": [
    "REJECTION: No acceptance criteria provided",
    "Architect must provide acceptance criteria in Given-When-Then format"
  ]
}
```

**Key Point:** Designer will **NOT create test cases** for stories without criteria

---

### CASE 2: 🔄 CRITERIA IN NON-STANDARD FORMAT (Not Given-When-Then)

**Scenario:** Story has criteria but not in "Given-When-Then" format

**Example Bad Formats:**
- "User can login with valid credentials" (no structure)
- "Validate password" (imperative, not scenario)
- "App displays error message" (missing precondition)
- "Enter password, click login" (action only, no context)

**What Designer Does:**
1. **TRANSFORMS criteria** to Given-When-Then format where possible
2. **Asks clarification questions:**
   - "Story says '[criterion text]' - is this a precondition (Given)? Action (When)? Expected outcome (Then)?"
3. **Identifies missing parts:**
   - Missing Given? → Ask for preconditions
   - Missing When? → Ask for action
   - Missing Then? → Ask for outcome
4. **Creates test cases** from transformed criteria ONLY
5. **Flags the transformation** in output

**Example Transformation:**
```
ORIGINAL (Bad):
"User can reset password with valid email"

TRANSFORMED (Good):
Given: User is on password reset page
When: User enters valid email and clicks reset button
Then: Email with reset link is sent within 2 minutes
```

**Output:**
```json
{
  "story_status": "PARTIALLY_VALID",
  "acceptance_criteria_status": "TRANSFORMED_FROM_NON_STANDARD_FORMAT",
  "test_cases": [
    {
      "title": "Reset password with valid email",
      "linked_criterion": "Criterion #1 (transformed from standard format)"
    }
  ],
  "clarification_questions": [
    "Criterion #2 'System validates strong password' - This seems like a validation rule. Please provide Given-When-Then format:",
    "Given [what state], When [user does what], Then [what happens]?"
  ],
  "validation_errors": [
    "Clarification needed for criterion #2 - not in Given-When-Then format"
  ]
}
```

**Key Point:** Designer will **TRANSFORM non-standard criteria** but asks for clarification before creating tests

---

### CASE 3: 🚫 BLANK/EMPTY USER STORY (No title, description, or criteria)

**Scenario:** User story is completely empty/missing

**What Designer Does:**
1. **STOPS and REJECTS the story** ⛔
2. Returns error: "REJECTION: User story is blank"
3. Requests story must include:
   - Story title/description
   - At least one acceptance criterion
   - Business value
4. **Does NOT attempt** to create any test cases

**Output:**
```json
{
  "story_status": "REJECTED",
  "acceptance_criteria_status": "REJECTED - MISSING CRITERIA",
  "rejection_reason": "User story is completely blank - cannot create tests from empty story",
  "test_cases": [],
  "validation_errors": [
    "REJECTION: User story is blank",
    "Cannot create test cases from empty story",
    "Architect must provide: story title, description, and acceptance criteria"
  ]
}
```

**Key Point:** Designer will **NOT create tests** from blank stories

---

### CASE 4: 🔶 PARTIAL CRITERIA (Mix of good and bad)

**Scenario:** Story has some Given-When-Then criteria AND some non-standard criteria

**Example:**
```
Criterion 1: Given user is logged in, When user clicks logout, Then user is redirected to login page
Criterion 2: System maintains session for 30 minutes
Criterion 3: Given invalid token, When user makes API call, Then 401 error returned
```

**What Designer Does:**
1. **Accepts valid criteria** (criteria 1 & 3 above)
2. **Questions unclear criteria** (criterion 2 - not in Given-When-Then)
3. **Creates test cases** for valid criteria only
4. **Documents both** in output
5. **Flags** which criteria are valid and which need clarification

**Output:**
```json
{
  "story_status": "PARTIALLY_VALID",
  "acceptance_criteria_status": "PARTIALLY_VALID - REQUESTING_CLARIFICATION",
  "valid_criteria": [
    "Criterion 1: Given user is logged in, When user clicks logout, Then user is redirected to login page",
    "Criterion 3: Given invalid token, When user makes API call, Then 401 error returned"
  ],
  "ambiguous_criteria": [
    "Criterion 2: System maintains session for 30 minutes - Not in Given-When-Then format"
  ],
  "test_cases": [
    {
      "id": "TC-001",
      "title": "User logout redirects to login page",
      "linked_criterion": "Criterion 1 (valid)"
    },
    {
      "id": "TC-002",
      "title": "Invalid token returns 401 error",
      "linked_criterion": "Criterion 3 (valid)"
    }
  ],
  "clarification_questions": [
    "Criterion 2 'System maintains session for 30 minutes' - Please provide Given-When-Then format:",
    "Given [what precondition], When [what action], Then [session lasts 30 minutes]?"
  ],
  "coverage_analysis": {
    "total_criteria": 3,
    "covered_criteria": 2,
    "coverage_percentage": "66.7%",
    "gaps": ["Criterion 2 needs clarification before test creation"]
  }
}
```

**Key Point:** Designer will **CREATE TESTS FOR VALID CRITERIA** and ask for clarification on unclear ones

---

## Decision Tree: What Designer Does

```
User Story Received
│
├─ NO ACCEPTANCE CRITERIA?
│  └─> REJECT ("REJECTION: No acceptance criteria provided")
│      └─> story_status: "REJECTED"
│          acceptance_criteria_status: "REJECTED - MISSING CRITERIA"
│
├─ STORY COMPLETELY BLANK?
│  └─> REJECT ("REJECTION: User story is blank")
│      └─> story_status: "REJECTED"
│
├─ ALL CRITERIA IN GIVEN-WHEN-THEN FORMAT?
│  └─> ACCEPT (story_status: "ACCEPTED")
│      └─> Create full test cases
│          Create test suites
│          Complete coverage analysis
│
└─ MIXED OR NON-STANDARD FORMAT?
   ├─> TRANSFORM criteria to Given-When-Then
   ├─> SEPARATE into: valid_criteria + ambiguous_criteria
   ├─> CREATE TEST CASES for valid_criteria only
   ├─> ASK CLARIFICATION for ambiguous_criteria
   └─> story_status: "PARTIALLY_VALID"
       acceptance_criteria_status: "TRANSFORMED_FROM_NON_STANDARD_FORMAT"
       OR "PARTIALLY_VALID - REQUESTING_CLARIFICATION"
```

---

## Output Status Fields

Designer now returns explicit status fields to communicate acceptance criteria quality:

### `story_status` Values:
- **"ACCEPTED"** - Story is complete and testable
- **"REJECTED"** - Story cannot be tested (blank or no criteria)
- **"PARTIALLY_VALID"** - Story has some testable criteria but needs clarification

### `acceptance_criteria_status` Values:
- **"VALID"** - All criteria are in Given-When-Then format
- **"REJECTED - MISSING CRITERIA"** - No acceptance criteria provided
- **"TRANSFORMED_FROM_NON_STANDARD_FORMAT"** - Criteria was converted to Given-When-Then
- **"PARTIALLY_VALID - REQUESTING_CLARIFICATION"** - Mix of valid and ambiguous criteria

### `validation_errors` Array:
Lists all issues found:
```json
"validation_errors": [
  "REJECTION: No acceptance criteria provided",
  "Clarification needed for criterion #2",
  "Missing Given context for criterion #3"
]
```

---

## Quality Gates Enforced

| Check | What Happens |
|-------|--------------|
| No acceptance criteria | ❌ REJECTED - Story not testable |
| Blank user story | ❌ REJECTED - No test creation |
| Non-Given-When-Then format | 🔄 TRANSFORMED - Ask clarification |
| Missing Given (precondition) | 🔶 FLAGGED - Request clarification |
| Missing When (action) | 🔶 FLAGGED - Request clarification |
| Missing Then (outcome) | 🔶 FLAGGED - Request clarification |
| Criteria too vague | 🔶 FLAGGED - Request specific values |
| Contradictory criteria | 🔶 HIGHLIGHTED - Ask which is correct |

---

## Communication Back to Architect

Designer now provides **actionable feedback** to Architect:

**When criteria is missing:**
```
"REJECTION: No acceptance criteria provided"

Architect must provide:
- At least 3 concrete acceptance criteria
- Each in Given-When-Then format
- Covering: happy path, edge cases, error scenarios
```

**When criteria is non-standard:**
```
"Clarification needed for criterion #2"

Story says: "User can reset password"

Please provide Given-When-Then format:
Given [user is on reset page], 
When [user enters valid email and clicks reset], 
Then [reset email is sent within 2 minutes]?
```

**When criteria is partially valid:**
```
"Partially valid criteria: 2 of 3 criteria are testable"

Valid criteria: Criteria 1, 3 (test cases created)
Need clarification: Criterion 2 (awaiting Given-When-Then format)
```

---

## Examples: Real Scenarios

### Example 1: Blank Story
**Input:**
```
Story: (empty)
```
**Output:**
```json
{
  "story_status": "REJECTED",
  "rejection_reason": "User story is completely blank",
  "test_cases": [],
  "validation_errors": [
    "REJECTION: User story is blank",
    "Cannot create test cases from empty story"
  ]
}
```

### Example 2: No Criteria
**Input:**
```
Title: "User login"
Description: "As a user, I want to login with my credentials so I can access my account"
Acceptance Criteria: (none)
```
**Output:**
```json
{
  "story_status": "REJECTED",
  "acceptance_criteria_status": "REJECTED - MISSING CRITERIA",
  "test_cases": [],
  "validation_errors": [
    "REJECTION: No acceptance criteria provided",
    "Architect: Please define acceptance criteria in Given-When-Then format",
    "Provide at least 3 concrete acceptance criteria"
  ]
}
```

### Example 3: Non-Standard Format
**Input:**
```
Title: "Password reset"
Acceptance Criteria:
1. "User can reset password with valid email"
2. "Email is sent with reset link"
```
**Output:**
```json
{
  "story_status": "PARTIALLY_VALID",
  "acceptance_criteria_status": "TRANSFORMED_FROM_NON_STANDARD_FORMAT",
  "test_cases": [
    {
      "id": "TC-001",
      "title": "Reset password with valid email",
      "linked_criterion": "Criterion 1 (transformed)"
    },
    {
      "id": "TC-002",
      "title": "Reset link sent in email",
      "linked_criterion": "Criterion 2 (transformed)"
    }
  ],
  "clarification_questions": [
    "Criterion 1: How long should reset email arrive? (seconds/minutes)",
    "Criterion 2: What's the reset link expiration time?"
  ]
}
```

---

## Summary: Designer Agent Robustness

| Scenario | Designer Response | Test Cases Created |
|----------|-------------------|-------------------|
| **Good criteria** (Given-When-Then) | ✅ ACCEPTS | ✅ YES |
| **No criteria** | ❌ REJECTS | ❌ NO |
| **Blank story** | ❌ REJECTS | ❌ NO |
| **Non-standard format** | 🔄 TRANSFORMS | ✅ YES (for transformed) |
| **Mixed valid + ambiguous** | 🔶 PARTIAL | ✅ YES (for valid only) |

**Bottom Line:** Designer agent will **NOT create test cases** for untestable stories. It will either **REJECT** (story has no criteria) or **TRANSFORM AND ASK** (criteria exists but needs clarification).

---

## File Location

[agents/designer.py](agents/designer.py) - Lines 45-95 contain edge case handling logic
