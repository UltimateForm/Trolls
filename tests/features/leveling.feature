Feature:leveling algorytim
  To make sure a certain amount of exp represents a certain level

  Scenario: with mytroll as troll.Troll(), adding exp
    Given mytroll.level is 1
    When i call troll.add_exp with X
    Then mytroll.level becomes 25
