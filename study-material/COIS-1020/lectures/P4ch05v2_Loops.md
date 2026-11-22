# P4ch05v2__Loops.pdf

Source: `source-material/P4ch05v2__Loops.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H: Programming for
    Computing Systems



             Chapter 5
              Looping
```

## PDF page 2

```text
Loops

• Loop
   – Structure that allows repeated execution of a block
      of statements
• Loop body
   – Block of statements within a looping structure
• Empty body
   – Body with no statements in it





                                                                                      2
```

## PDF page 3

```text
C# Loops

• C# types of loops
   – while loop
   – for loop
   – do loop (or do-while loop)





                                   Microsoft Visual C# 2010, Fourth                            3
                                                 Edition
```

## PDF page 4

```text
while Loop





                                                        4
```

## PDF page 5

```text
Using the while Loop

• while loop
   – Used to execute a body of statements continuously
     as long as some condition continues to be true
   – Pretest loop
• Making a while loop end correctly
   – Initialize the loop control variable
   – Test the control variable in the while expression
   – Alter the value of the control variable





                                                                                      5
```

## PDF page 6

```text
Using the while Loop (cont'd.)





                                                                             6
```

## PDF page 7

```text
Using the while Loop (cont'd.)

using System;
public static class FourHellos
{
                                              Hello  public static void Main()
   {                                           Hello
     int number = 1;                             Hello
    const int LIMIT = 5;                         Hello
    while (number < LIMIT)
     {
       Console.WriteLine("Hello");
     number = number + 1;
     }
   }
}




                                                                                   7
```

## PDF page 8

```text
Using the while Loop (cont'd.)


•  Infinite loop
   – A loop that never ends





                                                                                      8
```

## PDF page 9

```text
Using the while Loop (cont'd.)

•  Alter the control variable by:
   – Incrementing, or adding to it
   – Decrementing it

• Definite loop or counted loop
   – Loop for which the number of iterations is predetermined


•  Indefinite loop
   – The value of a loop control variable is not altered by
      arithmetic, but instead, is altered by user input



                                                                                        9
```

## PDF page 10

```text
Using the while Loop (cont'd.)

using System;
                          Do you want to see your balance? Y or N …Ypublic static class LoopingBankBal
                              Bank balance is $1,000.00{
                          Do you want to see next year’s balance? Y or N …Y  public static void Main()
   {                           Bank balance is $1,040.00
    double bankBal = 1000;        Do you want to see next year’s balance? Y or N …N
    const double INT_RATE = 0.04;   Have a nice day!
    char response;
    Console.Write("Do you want to see your balance? Y or N ...");
    response = Convert.ToChar(Console.ReadLine());
    while (response == 'Y')
     {
      Console.WriteLine("Bank balance is {0:C}", bankBal);
      bankBal = bankBal + bankBal * INT_RATE;
      Console.Write("Do you want to see next year’s balance? Y or N ...");
      response = Convert.ToChar(Console.ReadLine());
     }
    Console.WriteLine("Have a nice day!");
    Console.ReadLine();
   }
}

                                                                                       10
```

## PDF page 11

```text
Using the for Loop

• for loop
   – Shorthand way to create definite loops


•  Also, a pretest loop


• Sections of the loop
   – Control variable initialization
   – Control variable testing
   – Control variable updating





                                                                                        11
```

## PDF page 12

```text
Using the for Loop (cont'd.)





                                                                         12
```

## PDF page 13

```text
Computing an Average using For Loop

 using System;
 public static class ComputeAverageFor
 {
    public static void Main()
                                              Definite Loop    {
       int numMarks, mark, total = 0;
     double averageMark;
     Console.Write("Enter the number of marks (+ve) => ");
    numMarks = Convert.ToInt32(Console.ReadLine());
      for (int i = 0; i < numMarks; ++i)
      {
        Console.Write("Enter a mark => ");
      mark = Convert.ToInt32(Console.ReadLine());
         total = total + mark;
      }



                                                                                     13
```

## PDF page 14

```text
Computing an Average using For Loop
                 (Con’t)


       if (numMarks > 0)
      averageMark = total / (1.0 * numMarks);
     else
      averageMark = 0.0;

    Console.WriteLine("The average of {0} marks is {1:F}", numMarks,
                     averageMark);
    Console.ReadLine();
   }
                             Enter the number of marks (+ve) => 3}
                             Enter a mark => 87
                             Enter a mark => 64
                             Enter a mark => 78
                        The average of 3 marks is 76.33


                                                                                     14
```

## PDF page 15

```text
Computing an Average using while Loop

     using System;
     public static class ComputeAverageWhile
      {
        public static void Main()
                                                  Indefinite Loop         {
           int numMarks = 0, mark, total = 0;
         double averageMark;
         Console.Write("Enter a mark or -ve number to quit => ");
        mark = Convert.ToInt32(Console.ReadLine());
         while(mark >= 0)
                                     SentinnelSentinnel valueValue           {
              total = total + mark;
          numMarks++;
            Console.Write("Enter a mark or -ve number to quit => ");
         mark = Convert.ToInt32(Console.ReadLine());
           }

                                                                                         15
```

## PDF page 16

```text
While Loop Average (Con’t)


       if (numMarks > 0)
      averageMark = total / (1.0 * numMarks);
     else
      averageMark = 0.0;

    Console.WriteLine("The average of {0} marks is {1:F}",
         numMarks, averageMark);
    Console.ReadLine();
   }
}                         Enter a mark or -ve number to quit => 84
                         Enter a mark or -ve number to quit => 67
                         Enter a mark or -ve number to quit => 78
                         Enter a mark or -ve number to quit => -1
                     The average of 3 marks is 76.33


                                                                                16
```

## PDF page 17

```text
Using the for Loop (cont'd.)

• Other tasks
   – Decrement or perform some other task at the end of the
      loop’s execution


   – Leave one or more portions of the for expression empty
         • Be careful with for(;;)
         – It is an intentional infinite loop (POOR STYLE)





                                                                                        18
```

## PDF page 18

```text
Using the do Loop

• do loop
   – Checks at the bottom of the loop
      after one repetition has occurred
   – posttest loop

• Convenient when you know you
  want to perform some task at least
  one time





                                                                                     19
```

## PDF page 19

```text
Using the do Loop (cont'd.)





                                                                       20
```

## PDF page 20

```text
Using the do Loop (cont’d)

•  Applications of do loop
   – Validating data

    • Example
      Console.Write(“Enter a number between 1 and 10”);

      num = Convert.ToInt32(Console.ReadLine());


   becomes
      do

      {
         Console.Write(“Enter a number between 1 and 10”);
         num = Convert.ToInt32(Console.ReadLine());
      } while (num < 1 || num > 10);


                                                                                        21
```

## PDF page 21

```text
Validating Input Example


using System;
public static class ComputeAverageWhileValidateData
{
  public static void Main()
   {
     int numMarks=0, mark, total = 0;
    double averageMark;
       // Input and validate a mark
    do
     {
      Console.Write("Enter a mark or -1 to quit => ");
     mark = Convert.ToInt32(Console.ReadLine());
     } while (mark < -1 || mark > 100);





                                                                                  22
```

## PDF page 22

```text
Validating Input Example (cond’t)


  // loop while not seeing the sentinel value
  while (mark >= 0)
  {
     total = total + mark;
   numMarks++;
       // Input and validate the next mark
    do
     {
      Console.Write("Enter a mark or -ve number to quit => ");
     mark = Convert.ToInt32(Console.ReadLine());
     } while (mark < -1 || mark > 100);
  }





                                                                               23
```

## PDF page 23

```text
Validating Input Example (cond’t)


      // make sure the numMarks is not 0
       if (numMarks > 0)
      averageMark = total / (1.0 * numMarks);
     else
      averageMark = 0.0;

    Console.WriteLine("The average of {0} marks is {1:F}",
                numMarks, averageMark);
    Console.ReadLine();
   }
}





                                                                                  24
```

## PDF page 24

```text
Using Nested Loops

• When loops are nested, each pair contains an
  inner loop and an outer loop
   – The inner loop must be entirely contained within the
     outer loop
   – Loops can never overlap





                                                                                    25
```

## PDF page 25

```text
Using Nested Loops (cont'd.)





                                                                         26
```

## PDF page 26

```text
using System;                                                                                                    Starting bank balance is $1,000.00
public static class LoopingBankBal2                                                          Interest Rate: 4.00%
{                                                                                                   Starting bank balance is $1,000.00
  public static void Main()                                                              After year 1, bank balance is $1,040.00
   {                                                                                          After year 2, bank balance is $1,081.60
                                                                                              After year 3, bank balance is $1,124.86    double bankBal;
                                                                                              After year 4, bank balance is $1,169.86
    double rate;                                                                                              After year 5, bank balance is $1,216.65
     int year;                                                                                         Interest Rate: 6.00%
    const double START_BAL = 1000;                                                  Starting bank balance is $1,000.00
    const double START_INT = 0.04;                                                 After year 1, bank balance is $1,060.00
    const double INT_INCREASE = 0.02;                                           After year 2, bank balance is $1,123.60
                                                                                              After year 3, bank balance is $1,191.02    const double LAST_INT = 0.08;
                                                                                              After year 4, bank balance is $1,262.48
    const int END_YEAR = 5;                                                                                              After year 5, bank balance is $1,338.23
     for (rate = START_INT; rate <= LAST_INT; rate += INT_INCREASE)    Interest Rate: 8.00%
     {                                                                                             Starting bank balance is $1,000.00
      bankBal = START_BAL;                                                        After year 1, bank balance is $1,080.00
      Console.WriteLine("Starting bank balance is {0:C}", bankBal);          After year 2, bank balance is $1,166.40
                                                                                              After year 3, bank balance is $1,259.71       Console.WriteLine("Interest Rate: {0:P}", rate);
                                                                                              After year 4, bank balance is $1,360.49
       for (year = 1; year <= END_YEAR; ++year)                                                                                              After year 5, bank balance is $1,469.33
        {
        bankBal = bankBal + bankBal * rate;
        Console.WriteLine(" After year {0}, bank balance is {1:C}", year, bankBal);
        }
     }
    Console.ReadLine();
   }
}

                                                                                         27
```

## PDF page 27

```text
Accumulating Totals

•  Totals are accumulated
   – Gathered together and added into a final sum
         • By processing individual records one at a time in a loop
           sum = sum + mark;  // or
           sum += mark;
• Garbage
   – Unknown value (initial value of sum)
   – C# compiler helps to prevent seeing an incorrect total
         • By requiring you to provide a starting value
   – C# will not use the garbage value that happens to be
     stored at an uninitialized memory location


                                                                                    28
```

## PDF page 28

```text
Accumulating Totals

                                                   Enter purchase amount
using System;                                       14.50
public static class TotalPurchase                          Enter purchase amount, or 0 to quit
{                                                  5.19
  public static void Main()
                                                   Enter purchase amount, or 0 to quit   {
    double purchase;                                  3.04
    double total = 0;                                   Enter purchase amount, or 0 to quit
    const double QUIT = 0;
                                            0    Console.WriteLine("Enter purchase amount ");
    purchase = Convert.ToDouble(Console.ReadLine());       Your total is $22.73

     while (purchase != QUIT)
     {
        total += purchase;
      Console.WriteLine("Enter next purchase amount, or 0 to quit ");   Use a sentinel value to signal the
                                                                   end of data input      purchase = Convert.ToDouble(Console.ReadLine());
     }                                                        A sentinel value is a value of
    Console.WriteLine("Your total is {0:C}", total);                                                                                       the same data type but not a
    Console.ReadLine();                                                                  legal data value
   }
}



                                                                                        29
```

## PDF page 29

```text
Improving Loop Performance

• Make sure the loop does not include unnecessary
  operations or statements
• Example
   – A loop should execute while x is less than the sum
      of two integers, a and b
•  Initial solution
    while (x < a + b)
       // loop body
•  Better solution
    int sum = a + b;
    while (x < sum)
       // loop body


                                                                                    30
```

## PDF page 30

```text
Summary

• A loop is a structure that allows repeated execution
  of a block of statements
• Use a while loop to execute a body of statements
  continuously while some condition continues to be
  true
• When using a for statement, you can indicate in
  one place:
   – Starting value for the loop control variable
   – Test condition that controls loop entry
   – Expression that alters the loop control variable



                                                                                    31
```

## PDF page 31

```text
Summary (cont'd.)

• The do loop checks the bottom of the loop after
  one repetition has occurred
• You can nest any combination of loops to achieve
  desired results
•  In computer programs, totals frequently are
  accumulated
• Improve loop performance by making sure loop
  does not include unnecessary operations





                                                                                    32
```

