Feature: Task Management

  Scenario: Filtering tasks by category
    Given a nonempty list of tasks
    When I filter tasks by category Work
    Then only tasks belonging to Work should be displayed

  Scenario: Sorting tasks by due date
    Given a nonempty list of tasks
    When I sort the tasks by date
    Then the tasks should be ordered with the task with the closest due date first to the task with the furthest due date

  Scenario: Flagging a task
    Given a nonempty list of tasks
    When I flag a task with ID 1
    Then the task with ID 1 should have a toggled flagged value

  Scenario: Editing a task
    Given a nonempty list of tasks
    When I update the task with ID 2 to have a new title Updated Task and category Personal
    Then the task with ID 2 should have title Updated Task and category Personal

  Scenario: Generating a unique ID for a new task
    Given a nonempty list of tasks
    When I generate a new unique task ID
    Then the ID should be one greater than the highest existing ID



