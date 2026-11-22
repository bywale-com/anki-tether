# Lab 4 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 4 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 21:59                                                    Lab 4 - COIS 1020

          Trent University: COIS 1020H

             Lab 4: Intro to Looping





  Part One



   The following program uses a sentinel value loop to compute the average for a list of numbers

    inputted by a user.


          a. Answer Template (One Drive, must be Trent Authenticated)


          Answer Template (GoogleDocs)


             Click one of the the links above to open this lab's answer template, use it to compile your

           answers to the lab questions below.


                               If using the OneDrive version, you'll need to download the file so you have a

                 working copy.

                               If using the Google Docs version, click on File>Make a Copy to get your own copy

                    of the file to work in.




                    When asked "What is the output", you need to copy and paste (or screen

                             capture) what is seen in the Output Window.


                      Be sure to copy the entire contents of the Output Window ... which includes

                          prompt strings, input and output (not just the last line).


                                                If you screencapture, please only capture the relevant portion of the window

                               (not your entire desktop)


https://loki.trentu.ca/courses/cois1020/04-loops.html                                                                                                   1/7
```

## PDF page 2

```text
21/11/2026, 21:59                                                    Lab 4 - COIS 1020

          b. Make a new Project in C# (Lab4_1). Delete the skeleton code, and rename Program.cs,

              to Lab4_1.cs.


                     If you don't remember the steps for creating a project from last week, you can open the

             section below to see them again (by clicking on the arrow):


             Reminder: Creating a C# Project in VS Code

           c. Paste the following code into your empty .cs file.




                                                                                            Copy
                 using System;
                 public static class Lab4_1
                 {
                   public static void Main()
                   {
                     int value = 0, sum = 0, count = 0;
                     double average = 0.0;
                     Console.Clear();
                     // Read initial value (seed the loop)
                     Console.Write("Enter a positive integer (-1 to stop): ");
                     value = Convert.ToInt32(Console.ReadLine());
                     // if the inputted value is not the sentinel value, process it
                     while (value >= 0)
                     {
                         // Calculate the running total
                         sum += value;         // same as sum = sum + value;
                         // Keep track of the number of inputted values
                         count++;              // same as count = count + 1;
                         // Read next value
                         Console.Write("Enter a positive integer (-1 to stop): ");
                         value = Convert.ToInt32(Console.ReadLine());
                     }
                     // Calculate average (only if the user inputted any numbers)
                     if (count > 0)
                         average = sum / (double) count;
                     else
                         average = 0;
                     // Print results
                     Console.WriteLine("sum = {0}, count = {1}", sum, count);
                     Console.WriteLine("average = {0:F2} ", average);

https://loki.trentu.ca/courses/cois1020/04-loops.html                                                                                                   2/7
```

## PDF page 3

```text
21/11/2026, 21:59                                                    Lab 4 - COIS 1020

             31     }
             32    }



          d. Build the solution. Resolve any syntax mistakes (if you make any) until the program

            compiles. Run the program, and when prompted enter the following data one number at a

             time: 6, 9, 7, 3, -1


          What is the output?


          e. Change Line 25 to: average = sum / count; and run the program using: 6, 9, 7, 3, -1


          What is the output?


         How is it different from Part (d), and why?


                 f. Change Line 25 to: average = sum / (1.0 * count); and run the program using: 6, 9, 7,

             3, -1


          What is the output?


         How is it different from Part (e), and why?


          g. Create your own code to add to the original program, after Line 30. The code you add

            should display whether the total number of values entered by the user (count) is small (<

             5) or large (>= 5). Use an If/Else statement.


         Show just the If/Else statement.


         Run the program using the input 6, 9, 7, 3, -1


          What is the output?
                                                                              


          h. Run the program using the input 6, 9, 7, 3, 8, -1


          What is the output?





https://loki.trentu.ca/courses/cois1020/04-loops.html                                                                                                   3/7
```

## PDF page 4

```text
21/11/2026, 21:59                                                    Lab 4 - COIS 1020

                   i. Let’s experiment with Breakpoints and loops. Remove the IF statement you added in Part

              (g) and put in a Breakpoint ( F9  ) at Line 13: while (value >= 0) . Run the program

             with the input: 9, 5, -1. Be sure to single step through so you can see the variables in the

            Locals window change (Remember: F11  or use the buttons).


          Comment on what you saw in regard to program flow and the changes in the local window.


                   j. Repeat Part (i) with the input: -1.


          Comment on what you saw.


           k. Leaving the Breakpoint in at Line 13, add a semicolon to the end of the line (i.e., while

          (value >= 0); ) Run the program with the input: 9, 5, -1. Be sure to single step

            through.


         How does it differ from Part (i) and why?


                   l. One last experiment with this program. Remove the semicolon from the end of Line 14.

              Let's see if it is possible to simplify the program by eliminating the initial prompt

                 ( Console.Write  / Console.ReadLine ). Remove Lines 10-22 inclusive and replace

             with the following:




                                                                                            Copy
             11   while (value >= 0) {
             12     // prompt the user to enter an integer
             13     Console.Write("Enter a positive integer (-1 to stop): ");
             14     value = Convert.ToInt32(Console.ReadLine());
             15
             16     // Calculate the running total
             17     sum += value; // same as sum = sum + value;
             18
             19     // Keep track of the number of inputted values
             20     count++; // same as count = count + 1;
             21   }


         Run the program with the input data: 6, 9, 7, 3, -1


          What is the output, and if it's different from Part (d), why?


https://loki.trentu.ca/courses/cois1020/04-loops.html                                                                                                   4/7
```

## PDF page 5

```text
21/11/2026, 21:59                                                    Lab 4 - COIS 1020




  Part Two



   For the last part of the lab, you are required to complete the following program that uses a sentinel

   value loop and if statement to input marks between 0 and 100, determine if the mark is a pass or

     fail, and output the percentage of passing and failing marks. The program is terminated by entering

   a negative mark.


          a. Open a new instance of VS Code by going to File > New Window. If you're in Lab, leave

            Part One open for later so you can use it to demo.

          b. Make a new C# project, delete the skeleton code, rename Program.cs to Lab4_2.cs.

           c. Add the following code to your empty .cs file.




                                                                                            Copy
                 // Name: xxxxxxxxxxxxx
                 // Student Number: xxxxxxx
                 // Lab 4 Part 2
                 // Program Description: This program uses a loop and if statement
                 //    between 0 and 100 from a user, determines if the mark is pas
                 //    and outputs the percentage of passing and failing marks. The
                 //    terminates the program by entering a negative value for a ma


                 using System;
                 public static class Lab4_2
                 {
                    public static void Main()
                    {
                       const int PASS = 50;
                       int numPass=0, numFail=0, totalMarks=0;
                       double mark, perPass=0, perFail=0;


                       // loop to read in a valid mark or the sentinel value
                       do
                       {


https://loki.trentu.ca/courses/cois1020/04-loops.html                                                                                                   5/7
```

## PDF page 6

```text
21/11/2026, 21:59                                                    Lab 4 - COIS 1020
             21
                          // Read initial mark (seed the loop)
             22
                          Console.Write("Enter a mark between 0 and 100 (-ve value
             23
                          mark = Convert.ToDouble(Console.ReadLine());
             24
                       } while (mark > 100);
             25
                       // if the inputted mark is not the sentinel value, process i
             26
             27
                       while (mark >= 0)
             28
                       {
             29
             30
                          // increment the counter for the total number of data val
             31
                          // *** Insert code
             32
             33
                          // Determine if the mark is a pass or fail (If statement)
             34
                          // *** Insert code to count as pass or fail depending on
             35
             36
                          // Read next mark
             37
                          // *** Insert code
             38
                       }
             39
             40
                       // Calculate the percentage of marks that were passes and fa
             41
                       // *** Insert code
             42
             43
                       // Print results
             44
                       Console.WriteLine("Total number of marks = {0}", totalMarks)
             45
                       Console.WriteLine("Percentage of passing marks = {0:P1}", pe
             46
                       Console.WriteLine("Percentage of failing marks = {0:P1}", pe
             47
                    }
             48
                 }



          d. Replace the lines marked with // *** with the appropriate C# code (may require more

            than one line of code to complete the missing parts).

          e. Once you are comfortable that your program works correctly, test it with the following 3

            sets of inputs and for each output, include a screen capture for each in your Answer Doc

               for this lab. (Use a screen capture tool such as Snipping Tool or Snip & Sketch ).



        Tests


https://loki.trentu.ca/courses/cois1020/04-loops.html                                                                                                   6/7
```

## PDF page 7

```text
21/11/2026, 21:59                                                    Lab 4 - COIS 1020

            Enter the comma separated values, one for each prompt:

                 a.  25 , 75 , 50 , -1 , (the results should be: 3, 66.7% and 33.3% )

                 b.  60 , 70 , 80 , -1 , (the results should be: 3,100.0% and 0.0% )

                  c.  -1 (the results should be: 0, 0.0% and 0.0% )





   You've now completed the lab! Demonstrate your completed lab for feedback and to receive your

   grade.


   You only need to submit on Blackboard if you didn't demonstrate and receive your mark in the lab!

   Please use File > Save  as, to save your document as a PDF. Upload your completed PDF, and

   Lab4_2.cs to Blackboard (you do not need to submit your code file for question 1). Please be sure

    to submit the files together in the same submission (not two separate submissions, since the

   marker will only look at your last one).





https://loki.trentu.ca/courses/cois1020/04-loops.html                                                                                                   7/7
```

