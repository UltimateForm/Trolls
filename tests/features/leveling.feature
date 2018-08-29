Feature:leveling algorytim
  To make sure a certain amount of exp represents a certain level

  Scenario: with mytroll as troll.Troll(), adding exp
    Given mytroll.level is 1
    When i call mytroll.add_exp with random number between 1 and 10000 as X
    Then mytroll.level becomes rounded integer square root of X, minimum 1
