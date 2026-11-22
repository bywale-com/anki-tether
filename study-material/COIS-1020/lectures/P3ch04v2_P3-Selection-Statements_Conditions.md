# P3ch04v2_P3 Selection Statements_Conditions.pdf

Source: `source-material/P3ch04v2_P3 Selection Statements_Conditions.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H: Programming for
    Computing Systems



             Chapter 4
         Making Decisions
```

## PDF page 2

```text
Understanding Logic-Planning Tools
       and Decision Making

• Pseudocode
   – Tool that helps programmers plan a program’s logic
     by writing plain English statements

• Flowchart
   – You write the steps in diagram form as a series of
     shapes connected by arrows





                                                                                      2
```

## PDF page 3

```text
Understanding Logic-Planning Tools
        and Decision Making


• Sequence structure
   – One step follows another
      unconditionally





                                                                                         3
```

## PDF page 4

```text
Understanding Logic-Planning Tools
    and Decision Making (cont'd.)


• Sometimes, logical steps do not follow in an
  unconditional sequence

• Decision structure
   – Involves choosing between alternative courses of
     action based on some value within a program
   – All computer decisions are yes-or-no decisions
         • When reduced to their most basic form




                                                                                      4
```

## PDF page 5

```text
Understanding Logic-Planning Tools
   and Decision Making (cont'd.)





                                                                                   5
```

## PDF page 6

```text
Making Decisions Using the if
             Statement

• if statement
   – Used to make a single-alternative decision





                                                                                      6
```

## PDF page 7

```text
Declare an integer
                variable X


      Declare an integer variable
         y and initialize it to 5



       Assign the value 10 to X




No                               Yes
           X > Y?




                                              Print (“Good Job”)




                  Print (“Good Job”)
```

## PDF page 8

```text
Making Decisions Using the if
     Statement (cont'd.)





                                                                             8
```

## PDF page 9

```text
Making Decisions Using the if
             Statement

• Block
   – One or more statements contained within a pair of
      curly braces





                                                                                      9
```

## PDF page 10

```text
Making Decisions Using the if
     Statement (cont'd.)





                                                                            10
```

## PDF page 11

```text
Making Decisions Using the if
     Statement (cont'd.)





                                                                              11
```

## PDF page 12

```text
Making Decisions Using the if
     Statement (cont'd.)





                                                                            12
```

## PDF page 13

```text
Making Decisions Using the if
         Statement (cont'd.)
• Nested if
   – One decision structure is contained within another





                                                                                    13
```

## PDF page 14

```text
Making Decisions Using the if
          Statement (cont'd.)
using System;
public static class NestedDecision                 Enter an integer 8
{                                   8 is between 5 and 10
  public static void Main()
   {
    const int HIGH = 10, LOW = 5;               Enter an integer 4
     int number;
    Console.Write("Enter an integer ");
    number = Convert.ToInt32(Console.ReadLine());  Enter an integer 10
    if(number > LOW)
       if(number < HIGH)
          Console.WriteLine("{0} is between {1} and {2}", number, LOW, HIGH);
    Console.ReadLine();
   }
}



                                                                                       14
```

## PDF page 15

```text
Making Decisions Using the if-else
             Statement

• Dual-alternative decisions
   – Have two possible outcomes
• if-else statement
   – Used to
         • perform one action when a Boolean expression
         evaluates as true
         • And an alternate action when it evaluates as false





                                                                                    15
```

## PDF page 16

```text
Making Decisions Using the if-else
        Statement (cont'd.)





                                                                                   16
```

## PDF page 17

```text
Making Decisions Using the if-else
        Statement (cont'd.)

using System;
public static class IfElseDecision               Enter an integer 8
 {                                 8 is not greater than 10
   public static void Main()
   {
     const int HIGH = 10;                                       Enter an integer 32
      int number;                                  32 is greater than 10
     Console.Write("Enter an integer ");
    number = Convert.ToInt32(Console.ReadLine());
       if (number > HIGH)
       Console.WriteLine("{0} is greater than {1}", number, HIGH);
      else
       Console.WriteLine("{0} is not greater than {1}", number, HIGH);
     Console.ReadLine();
   }
 }


                                                                                   17
```

## PDF page 18

```text
Using Compound Expressions in if
            Statements


• You can combine multiple decisions into a single
  if statement
   – Using a combination of AND (&&) and OR (||)
     operators





                                                                                    18
```

## PDF page 19

```text
Using the Conditional AND Operator

• Conditional AND operator
   – Determines whether two expressions are both true
   – Written as two ampersands (&&)
   – You must include a complete Boolean expression on
     each side of the operator
•  Short-circuit evaluation
   – Expressions in each part of an AND expression are
     evaluated only as much as necessary
         •  if the first condition is false, the second condition is
         not evaluated (overall condition will always be false)



                                                                                    19
```

## PDF page 20

```text
Using the Conditional AND Operator
                    (cont'd.)





• Common application of Conditional AND
   – Determine if a number falls into a range (0 ≤ grade ≤ 100)
            if ((grade >= 0) && (grade <= 100))   // correct
            if (0 <= grade <= 100)                        // incorrect


                                                                                          20
```

## PDF page 21

```text
Using the Conditional OR Operator

• Conditional OR operator
   – Used when you want some action to occur even if
     only one of two conditions is true
   – Short circuited as well (if first condition is true)
   – Written as ||





                                                                                    21
```

## PDF page 22

```text
Combining AND and OR Operators

using System;
public static class MovieDiscount
{
  public static void Main()
   {
     int age = 10;
    char rating = 'R';
     const int CHILD_AGE = 12;
     const int SENIOR_AGE = 65;
    Console.WriteLine("When age is {0} and rating is {1}", age, rating);
       if ((age <= CHILD_AGE || age >= SENIOR_AGE) && rating == 'G')
      Console.WriteLine("Discount applies");
     else
      Console.WriteLine("Full price");
    Console.ReadLine();
   }
}



                                                                                    22
```

## PDF page 23

```text
Multi-Alternative If Statements

• Multi-alternative if statements are used if it is
  necessary to have more than just two
  alternatives
• if-else-if statements can become very
  complex.
• Imagine the following decision set.
      if it is very cold, wear a heavy coat,
    else, if it is chilly, wear a light jacket,
    else, if it is windy, wear a windbreaker,
    else, if it is hot, wear no jacket.


                                                                                    24
```

## PDF page 24

```text
Multi-Alternative If Statements


if (expression)
  statement or block
else if (expression)
  statement or block
else if (expression)
  statement or block
. . .             // Put as many else ifs as needed
else
  statement or block

• Care must be used since else statement matches up
   with the immediately preceding unmatched if
  statement.
• Example: Assume you are to assign a letter grade
  based on a numeric grade that has been input


                                                                                   25
```

## PDF page 25

```text
LetterGrade.cs

// This program asks the user to enter a numeric mark and assigns and prints a
// letter grade for the score. The program displays an error message if an invalid
// mark (> 100) is entered.

using System;

public static class LetterGrade
{
  public static void Main()
  {
    int mark;         // numeric mark
   char grade;      // letter grade
     // Get the numeric test score.
   Console.Write("Enter your numeric mark => ");
   mark = Convert.ToInt32(Console.ReadLine());




                                                                                    26
```

## PDF page 26

```text
LetterGrade.cs (cont’d)

     // Display the grade.
     if (mark < 60)                             Output 1:
      grade = ‘F’;                                   Enter your numeric mark => 78
    else if (mark < 70)
                             The letter grade for 78 is C.      grade = ‘D’;
    else if (mark < 80)
       grade = ‘C’;                             Output 2:
    else if (mark < 90)                                   Enter your numeric mark => 103
       grade = ‘B’;
                             The letter grade for 103 is X.    else if (mark <= 100)
       grade = ‘A’;
    else         // Invalid score
    {
        Console.WriteLine("Invalid mark.");
       grade = ‘X’;
    }
   Console.WriteLine(“The letter grade for {0} is {1}.”, mark, grade);
   Console.ReadLine();
  }
}
                                                                                     27
```

## PDF page 27

```text
if-else-if Flowchart





                                                               28
```

## PDF page 28

```text
Decisions Using the switch Statement


 • switch structure
    – Tests a single variable against a series of exact
      matches
  • Keywords
    – switch, case, break, and default
  • C# supports “No fall through rule”
    – Not allowing code to reach the end of a case
    – Use a break statement at the end of each case (or
      cases)





                                                                                      29
```

## PDF page 29

```text
Decisions Using the switch Statement


•  Switch Solution

                                                                    •   Multi-alternative If Solutionswitch(year)
{
                                                     if (year == 1)   case 1:

                                                          Console.WriteLine(“Freshman”);         Console.WriteLine(“Freshman”);
         break;
                                                     else if (year == 2)   case 2:
          Console.WriteLine(“Sophmore”);
                                                          Console.WriteLine(“Sophmore”);         break;
                                                     else if (year == 3)   case 3:
          Console.WriteLine(“Junior”);
                                                          Console.WriteLine(“Junior”);         break;
                                                     else if (year == 4)   case 4:
                                                           Console.WriteLine(“Senior”);          Console.WriteLine(“Senior”);
                                                     else         break;
                                                           Console.WriteLine(“Invalid   default:
                                                     year”);          Console.WriteLine(“Invalid year”);
         break;
   }


                                                                                         30
```

## PDF page 30

```text
Decisions Using the switch Statement


  • The keyword case is followed by one of the
   possible values that might equal the selector


  • A switch does not need a default case
    – Good programming practice to include one





                                                                                      31
```

## PDF page 31

```text
Decisions Using the switch Statement





                                                                                     32
```

## PDF page 32

```text
Practice:
           PetFood.cs
// This program demonstrates a menu-driven interface using a switch statement
using System;

public static class PetFood
{
  public static void Main()
  {
    char foodGrade;   // Grade of pet food

     // Prompt the user for a grade of pet food.
   Console.WriteLine("Our pet food is available in three grades: A, B, and C");
   Console.Write("Which do you want pricing for => ");
   foodGrade = Convert.ToChar(Console.ReadLine());





                                                                                    33
```

## PDF page 33

```text
PetFood.cs (cont’d)

     // Display pricing for the selected grade.
                                     Output 1:   switch(foodGrade)
                                            Our pet food is available in three grades:    {
                                               A, B, and C.     case 'a':  case 'A':
                                           Which do you want pricing for? b       Console.WriteLine(“75 cents per kg.");
                                              50 cents per kg.       break;
     case 'b':  case 'B':
       Console.WriteLine(“50 cents per kg.");                                     Output 2:
       break;
                                            Our pet food is available in three grades:
     case 'c':  case 'C':                                               A, B, and C.
       Console.WriteLine(“35 cents per kg.");                                           Which do you want pricing for? A
       break;                                              75 cents per kg.
     default:
        Console.WriteLine("Invalid choice.");
       break;                           Output 3:
    }                                        Our pet food is available in three grades:
   Console.ReadLine();                         A, B, and C.
                                           Which do you want pricing for? x  }
                                                         Invalid choice}

                                                                                         34
```

## PDF page 34

```text
PetFood.cs (cont’d)

 // Alternate form of the switch statement using the char.ToUpper() method
// to reduce the number of cases

 switch(char.ToUpper(foodGrade))
 {
  case ‘A':
     Console.WriteLine(“75 cents per kg.");
     break;
  case 'B':
     Console.WriteLine(“50 cents per kg.");
     break;
  case 'C':
     Console.WriteLine(“35 cents per kg.");
     break;
  default:
     Console.WriteLine("Invalid choice.");
     break;
 }


                                                                                  35
```

## PDF page 35

```text
Using the Conditional Operator

• Conditional operator
   – Used as an abbreviated version of the if-else
     statement
   – A ternary operator
   – Has limited application

• Syntax
       testExpression ? trueResult : falseResult;

• Example
       biggerNum = (a > b) ? a : b;


                                                                                    36
```

## PDF page 36

```text
Using the NOT Operator

• NOT operator
   – Written as an exclamation point (!)
   – Negates the result of any Boolean expression
   – Used more to improve readability of a program than an
     absolute must especially with Boolean data types: while
     (!done)

• Example: consider car insurance premiums
      if (age > 25) then premium = 200; else premium = 125;
      if (!(age > 25)) then premium = 125; else premium = 200;



                                                                                       37
```

## PDF page 37

```text
Avoiding Common Errors When
         Making Decisions

• Most frequent errors include:
   – Using the assignment operator instead of the
     comparison operator (= vs. ==)
   – Inserting a semicolon after the Boolean expression
      in an if statement (semantic versus syntax error)
            if (salary > 50000);    // incorrect
   – Failing to block a set of statements with curly braces
   – Failing to include a complete Boolean expression on
     each side of an && or || operator
        if(grade >= 0 && <= 100)            // incorrect
        if(grade >= 0 && grade <= 100)  // correct

                                                                                    38
```

## PDF page 38

```text
Performing Accurate and Efficient
         Range Checks

• Range check
   – A series of if statements that determine whether a
     value falls within a specified range
• Problem





                                                                                    39
```

## PDF page 39

```text
Performing Accurate and Efficient
       Range Checks (cont'd.)

•  Solution
      if(saleAmount >= 1000)
         commissionRate = 0.08;                                          why is it not
      else if(saleAmount >= 500)     Else if(saleAmount < 500)
         commissionRate = 0.06;
      else commissionRate = 0.05;

• Never substitute a series of single if statements for
  a multi-alternative if statement





                                                                                         40
```

## PDF page 40

```text
Summary

• A flowchart is a pictorial tool that helps you
  understand a program’s logic
• You use an if statement to make a single-
  alternative decision
• When you make a dual-alternative decision, you
  can use an if-else statement
•  Conditional AND operator determines whether two
  expressions are both true
• Use the conditional OR operator when you want
  some action to occur when one or both of two
  conditions are true


                                                                                    43
```

## PDF page 41

```text
Summary (cont'd.)


• AND operators take precedence
• The switch statement tests a single variable
  against a series of exact matches
• The conditional operator is used as an abbreviated
  version of the if-else statement
• You use the NOT operator to negate the result of
  any Boolean expression
• Common errors when making decisions





                                                                                    44
```

