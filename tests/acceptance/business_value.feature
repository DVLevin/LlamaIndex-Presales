Feature: Evaluate the effort and quality of a reviewed proposal
  As a team evaluating a proposal drafting workflow
  I want to compare completed manual and assisted work on the same brief
  So that my decision reflects the cost and quality of work my team can use

  @roi-measurement @critical
  Scenario: Capture a comparable pair of runs
    Given a transcript, a required document list and written review criteria
    And the same inputs and acceptance criteria are available for each run
    When reviewers check a manual draft and an assisted draft against the transcript
    Then they record the drafting time, review time, corrections and final decision for each
    And they record wall-clock time separately from active staff time
    And they label demo, simulated and provider-backed runs separately
    And they keep the result when the assisted workflow takes longer

  @quality-comparison
  Scenario: Record substantive corrections
    Given the reviewer can trace each requirement and commercial figure to the input
    When either draft omits a requirement or introduces an unsupported commitment
    Then the reviewer records the discrepancy and the time spent correcting it
    And records whether the final draft was accepted, revised or rejected

  @roi-measurement
  Scenario: Check the arithmetic with fictional inputs
    Given a fictional manual run took 100 staff minutes including review
    And a fictional assisted run took 80 staff minutes including review
    When I subtract assisted time from manual time
    Then the example difference is 20 staff minutes or 20% of the manual baseline
    And I label the result as an illustration wherever I quote it

  @scalability-value
  Scenario: Separate capacity estimates from cash savings
    Given three fictional comparable proposals per month
    And a model assumption of 20 staff minutes released per proposal
    And an assumed cost of 60 euros per staff hour
    When I estimate the value of the released time
    Then I report one hour of capacity valued at 60 euros per month before tooling costs
    And I show provider charges and any other operating costs separately
    And I require an observed expense change before reporting realized cash savings

  @customer-experience
  Scenario: Record only feedback that a reviewer or recipient actually gives
    Given a reviewer or recipient has seen a proposal
    When I document their feedback
    Then I distinguish their comments from my interpretation
    And I leave unobserved satisfaction, conversion and revenue outcomes unmeasured
