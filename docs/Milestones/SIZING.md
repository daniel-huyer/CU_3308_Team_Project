# Lab 3 Team Sizing Document

Replace the sample text in this document with your team’s actual information.

Recommended filename for your completed document:

```text
SIZING.md
```

---

## Team Information

**Team Number:** Team 4

**Team Name:** ___

**Meeting Day/Time:** June 8  @4 pm MT

**Team Members Present:**

- Daniel Huyer
- Kevin Bell
- Bri Rowe
- Alejandro Banuelos Vielmas

**Scrum Master for This Meeting:** Daniel Huyer

**Zoom Recording Link:** 
https://o365coloradoedu-my.sharepoint.com/personal/brro5166_colorado_edu/_layouts/15/stream.aspx?id=%2Fpersonal%2Fbrro5166%5Fcolorado%5Fedu%2FDocuments%2FRecordings%2FGroup%20Meeting%2D20260608%5F180325%2DMeeting%20Recording%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2E00c2971c%2De929%2D4577%2D9738%2D80cb8d97d0c0

---

## Planning Poker Summary

Briefly describe how your team conducted planning poker.
- We first discussed the story and attempted to reach a shared understanding of what the story was about. Each team member then privately selected an effort value for each user story. We revealed our estimates at the same time. When estimates differed, the highest and lowest voters explained their reasoning, the team discussed the story, and we then discussed until a consensus was reached. 

Example:

> Each team member privately selected an effort value for each user story. We revealed our estimates at the same time. When estimates differed, the highest and lowest voters explained their reasoning, the team discussed the story, and we voted again until we reached consensus.

---

## Stories Included

List the story numbers assigned to your team.

```text
Stories included: [2, 19, 20]
```

---

## User Story 2

**As a** developer  
**I want** to validate incoming data in Python before further processing  
**So that** invalid or incomplete data does not cause runtime errors.

**Agreed Effort Level:** 5

### Acceptance Criteria

**Scenario:** User input is valid

**Given** the input is valid 
**When** the user inputs valid data
**Then** the program accepts input and continues

**Scenario:** User input is invalid

**Given** the input is invalid  
**When** the user inputs invalid or incorrectly formatted data
**Then** the program displays an error message and prompts user with correct format for reentry

---

## User Story 19

**As a** product stakeholder  
**I want** to have the system produce meaningful output from stored data  
**So that** users gain value from interacting with it.

**Agreed Effort Level:** 8

### Acceptance Criteria

**Scenario:** Data available and clean

**Given** the stored data exists in DB
**When** user requests output based on available data
**Then** system produces requested meaningful output

**Scenario** Data unavailable 

**Given** the stored data doesn't exist in DB
**When** user requests output based on unavailable data
**Then** system informs user that no data for their request is available

---

## User Story 20

**As a** team  
**I want** to break large features into smaller Python- or SQL-focused tasks  
**So that** work can be estimated and assigned more accurately.

**Agreed Effort Level:** 2

### Acceptance Criteria

**Scenario:** Team Leader delegates Python or SQL tasks

**Given** the Team leader delegates Python or SQL tasks to a team
**When** the team members receive their respective Python or SQL tasks 
**Then** the team members completes their various Python or SQL tasks given to them.
