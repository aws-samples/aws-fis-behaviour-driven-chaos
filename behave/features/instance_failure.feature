Feature: Instance Failure

    Experiment with EC2 instance failure scenarios to ensure my website is resilient

    Scenario: My website is resilient to infrastructure failure
    Given My website is up and can serve 10 transactions per second
    And I have an EC2 Auto-Scaling Group with at least 3 running EC2 instances
    And I have an EC2 Auto-Scaling Group with instances distributed across at least 3 Availability Zones
    When an EC2 instance is lost
    Then I can continue to serve 10 transactions per second
    And 90 percent of transactions to my website succeed