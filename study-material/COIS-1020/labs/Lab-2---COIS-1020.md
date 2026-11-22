# Lab 2 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 2 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 21:59                                                    Lab 2 - COIS 1020

          Trent University: COIS 1020H

          Lab 2: Input/Processing/Output





                  This lab deals with outputting currency values. Because the currency symbol displayed

                      in the console is controlled by your operating system's currency settings, some of you

                  probably won't see a $, but instead will see whatever your local currency symbol is.

                   Don't worry about it. The markers are used to this.




 C# Input and Output



          a. For this lab, you will need to create a new project in Visual Studio Code (name it Lab2).


                     If you don't remember the steps for creating a project from last week, you can open the

             section below to see them again (by clicking on the arrow):


             Reminder: Creating a C# Project in VS Code

          b. Delete the skeleton code, and rename Program.cs to Lab2.cs, then copy the program

           below into your now empty code file.




                                                                                            Copy
                 public static class Lab2
                 {
                     public static void Main()
                     {
                         int idNum;
                         double payRate, hours, grossPay;
                         string firstName;


https://loki.trentu.ca/courses/cois1020/02-inputouput.html                                                                                               1/7
```

## PDF page 2

```text
21/11/2026, 21:59                                                    Lab 2 - COIS 1020

             9
                         Console.Clear();             10
                         // prompt the user to enter employee's first name             11
                         Console.Write("Enter employee's first name => ");             12
                         firstName = Console.ReadLine();             13
             14
                         // prompt the user to enter employee's last name             15
                         Console.Write("Enter employee's last name => ");             16
                         lastName = Console.ReadLine()             17
             18
                         // prompt the user to enter a six digit employee number             19
                         Console.Write("Enter a six digit employee's ID => ");             20
                         idNum = Convert.ToInt32(Console.ReadLine());             21
             22
                         // prompt the user to enter the number of hours employee w             23
                         Console.Write("Enter the number of hours employee worked =             24
                         hours = Convert.ToInt32(Console.ReadLine());             25
             26
                         // prompt the user to enter the employee's hourly pay rate             27
                         console.Write("Enter employee's hourly pay rate: ");             28
                         payRate = Convert.ToDouble(Console.ReadLine());             29
             30
                         // calculate gross pay             31
                         grossPay = hours * payRate;             32
             33
                         // output results             34
                         Console.WriteLine("Employee {0} {1}, (ID: {2}) earned {3}"             35
                                 firstName, lastName, idNum, grossPay);             36
                     }             37
                 }




           c. Answer Template (One Drive, must be Trent Authenticated)


          Answer Template (GoogleDocs)


             Click one of the the links above to open this lab's answer template, use it to compile your

           answers to the lab questions below.




                                                                              



https://loki.trentu.ca/courses/cois1020/02-inputouput.html                                                                                               2/7
```

## PDF page 3

```text
21/11/2026, 21:59                                                    Lab 2 - COIS 1020

                 a.  If using the OneDrive version, you'll need to download the file so you have a

                 working copy.

                 b.  If using the Google Docs version, click on File>Make a Copy to get your own copy

                    of the file to work in.




                    When asked "What is the output", you need to copy and paste (or screen

                             capture) what is seen in the Output Window.


                      Be sure to copy the entire contents of the Output Window ... which includes

                          prompt strings, input and output (not just the last line).


                                                If you screencapture, please only capture the relevant portion of the window

                               (not your entire desktop)



          d. Run your program ( F5 ). Building your program will fail due to syntax errors. Resolve the

            syntax mistakes until the program compiles. There are 3 intentional syntax mistakes (Hint:

              think variable, semicolon and output), plus any you may make while copying.




                       The same mistake may lead to cascading error messages (so it might look

                                   like more then 3 originally).




          What are the 3 intentional syntactical mistakes?


          Once your program is free of syntax mistakes and compiles you will be able to run it.

           Throughout the rest of the lab, unless told otherwise, you should use the following data

           each time you run your program and it prompts you for input:



                              When asked for:  Enter


                                                First Name    John


                                         Last Name    Smith


                                              ID        123456


https://loki.trentu.ca/courses/cois1020/02-inputouput.html                                                                                               3/7
```

## PDF page 4

```text
21/11/2026, 21:59                                                    Lab 2 - COIS 1020

                              When asked for:  Enter


                                   Hours Worked   22.5


                                    Pay Rate     14.85



            Run the program ( F5 ) and when asked, input the data above. You'll discover that the

           program fails half way through data entry because of a logical error. Examine the line the

           program failed on to determine what is wrong. Fix the mistake.




                            This logical error was easy to find because it resulted in a failure which

                                  illustrated where the mistake occurred. Most logical errors are more difficult

                                to find and fix because you don't get any indication that something is wrong,

                                  just incorrect results.




          What was the logical mistake you fixed?


            Run the program again.( F5 ).


          What is the output?


          e. On Line 34, replace {3} with {3:C} and run the program again.




                                                                                            Copy
             34   Console.WriteLine("Employee {0} {1}, (ID: {2}) earned {3}",





                      Remember from last week, all line numbers refer to the line numbers in the

                         code you copied above, which probably won't be the same as yours (since

                         you will be changing things)




          What is the output?


          What is the difference in the output between this and the previous run?


https://loki.trentu.ca/courses/cois1020/02-inputouput.html                                                                                               4/7
```

## PDF page 5

```text
21/11/2026, 21:59                                                    Lab 2 - COIS 1020

                 f. Replace the statement on Lines 34-35 with the following statement:




                                                                                            Copy
             34   Console.WriteLine("Employee {0} {1}, (ID: {2}) earned {3:F4}",
             35           firstName.ToUpper(), lastName.ToLower(), idNum, grossPay);


                                                                              


            Run your program with the previously provided input.


          What is the output?


          What is the difference in the output between this and the previous run?


          g. Return Lines 34-35 to the form:




                                                                                            Copy
             34   Console.WriteLine("Employee {0} {1}, (ID: {2}) earned {3:C}",
             35           firstName, lastName, idNum, grossPay);


         Assume employees have their wages reduced by 20% to reflect the effects of taxes:


                 Modify the variable declarations in Line 6 to add netPay

                    After you have calculated grossPay add a new line of code into the program to

               compute netPay which is grossPay multiplied by 0.8 (80%).




                             Math Lesson Reminder: The 0.8 multiplier is 1.0 - 0.20 . If 20% of

                                   the employee's salary goes to tax, 80% of their salary (or 100% -

                            20%) is what they get to keep.



                 Modify Lines 34-35 to print out the value of netPay as well as grossPay (Hint:

                you need to include both the variable and a place in the format string for the

                   variable to go!).


          What is the output?





https://loki.trentu.ca/courses/cois1020/02-inputouput.html                                                                                               5/7
```

## PDF page 6

```text
21/11/2026, 21:59                                                    Lab 2 - COIS 1020

          h. Assume that instead of hardcoding the tax rate at 20%, you want the user to input this

            value when the program runs:


              Add a new variable called taxRate to Line 6

                 Then, similar to what was done in Lines 26-28, have the user input a value to

                taxRate , after line 28. You should ask them to enter their tax rate as a decimal

                  value between 0-1.




                                       In a situation like there were multiple formats might be valid, be sure

                                       to include the expected format in output your message. Clear user

                                   expectations reduce user error.



                      Finally, modify the line of code where netPay  is computed to use taxRate as

               opposed to the hardcoded value of 0.8.




                             Math Lesson Reminder: The 0.8 multiplier was 1.0 - 0.20 . If 20%

                                       of the employee's salary goes to tax, 80% of their salary (or 100% -

                            20%) is what they get to keep.




         Show the modified lines of code.


          What is the output (assuming a tax rate of 25%)?


                   i. Modify the output statement (Lines 34-35) to print out the data in the following format

           Smith: 123456 => $250.59 ).


         Show the modified lines of code.


          What is the output (assuming the same input as in Part (h))?




   You've now completed the lab! Demonstrate your completed lab for feedback and to receive your

   grade.



https://loki.trentu.ca/courses/cois1020/02-inputouput.html                                                                                               6/7
```

## PDF page 7

```text
21/11/2026, 21:59                                                    Lab 2 - COIS 1020

   You only need to submit on Blackboard if you didn't demonstrate and receive your mark in the lab!

   Please use File > Save  as, to save your document as a PDF. Upload your completed PDF to

   Blackboard.





https://loki.trentu.ca/courses/cois1020/02-inputouput.html                                                                                               7/7
```

