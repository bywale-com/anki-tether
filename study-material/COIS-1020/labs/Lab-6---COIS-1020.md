# Lab 6 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 6 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 22:00                                                    Lab 6 - COIS 1020

          Trent University: COIS 1020H

              Lab 6: More Methods





   The program in this lab uses two user-defined methods: one with call by value formal parameters

   and one with call by address formal parameters. The program computes the Gross Pay and Net

   Pay for an employee after entering the employee's last name, hours worked, hourly rate, and

   percentage of tax.


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




          b. Make a new Project in C# (Lab6). Delete the skeleton code, and rename Program.cs, to

            Lab6.cs.


https://loki.trentu.ca/courses/cois1020/06-methods2.html                                                                                               1/6
```

## PDF page 2

```text
21/11/2026, 22:00                                                    Lab 6 - COIS 1020

                     If you don't remember the steps for creating a project from last week, you can open the

             section below to see them again (by clicking on the arrow):


             Reminder: Creating a C# Project in VS Code

           c. Paste the following code into your empty .cs file.




                                                                                            Copy
                 // Name: xxxxxxxxxxxxx
                 // Student Number: xxxxxxx
                 // Lab 6
                 // Program Description: This program uses two user defined methods
                 //    the gross pay and net pay for an employee after entering the
                 //    last name, hours worked, hourly rate, and percentage of tax.


                 using System;
                 public static class Lab6
                 {
                    public static void Main()
                    {
                      // declare variables
                      double ratePay, taxRate, grossPay, netPay=0, hrsWrked;
                      string lastName;


                      Console.Clear();
                      // enter the employee's last name
                      Console.Write("Enter the last name of the employee => ");
                      lastName = Console.ReadLine();


                      // enter (and validate) the number of hours worked (positive
                      do
                      {
                         Console.Write("Enter the number of hours worked (> 0) => "
                         hrsWrked = Convert.ToDouble(Console.ReadLine());
                      } while (hrsWrked < 0);


                      // enter (and validate) the hourly rate of pay (positive numb
                      // *** Insert the code to enter and validate the ratePay


                      // enter (and validate) the percentage of tax (between 0 and
                      // *** Insert the code to enter and validate taxRate

https://loki.trentu.ca/courses/cois1020/06-methods2.html                                                                                               2/6
```

## PDF page 3

```text
21/11/2026, 22:00                                                    Lab 6 - COIS 1020

             34
             35        // Call a method to calculate the gross pay (call by value)
             36        grossPay = CalculateGross(hrsWrked, ratePay);
             37
             38        // Invoke a method to calculate the net pay (call by referenc
             39        CalculateNet(grossPay, taxRate , ref netPay);
             40
             41        // print out the results
             42        Console.WriteLine("{0} worked {1} hours at {2:C} per hour", l
             43                          hrsWrked, ratePay);
             44        // *** Insert the code to print out the Gross Pay and Net Pay
             45       }
             46
             47     // Method: CalculateGross
             48     // Parameters
             49     //      hours: double storing the number of hours of work
             50     //      rate: double storing the hourly rate
             51     // Returns: double storing the computed gross pay
             52     public static double CalculateGross(double hours, double rate)
             53     {
             54        // *** Insert the contents of the CalculateGross Method
             55     }
             56
             57     // Method: CalculateNet
             58     // Parameters
             59     //      grossP: double storing the grossPay
             60     //      tax: double storing tax percentage to be removed from gr
             61     //      netP: call by reference double storing the computed net
             62     // Returns: void
             63     public static void CalculateNet(double grossP, double tax, ref d
             64     {
             65        // *** Insert the details of the CalculateNet Method
             66     }
             67   }



          d. Replace the lines marked with // *** with the appropriate C# code (may require more

            than one line of code to complete the missing parts).





https://loki.trentu.ca/courses/cois1020/06-methods2.html                                                                                               3/6
```

## PDF page 4

```text
21/11/2026, 22:00                                                    Lab 6 - COIS 1020

          e. Build the solution. Resolve any syntax mistakes (if you make any) until the program

            compiles. Run the program using the input data: Smith, 40, 12.5, 0.2. You should find

              that the gross pay is $500.00 and net pay is $400.00


          What is the output?


                 f. Run the program using input Smith, -8, 40, 12.5, 0.2.


          What is the output?


          g. Run the program using input Smith, 40, -3, 12.5, 0.2.


          What is the output?


          h. Run the program using input Smith, 40, 12.5, 9, 0.2.


          What is the output?


                   i. Run the program using input Smith, 44, 12.5, 0.2.


          What is the output?


                   j. Now let's add another user-defined method to our program . This method will compute

           any overtime pay.




                      Assume the employees receive time and a half (1.5) for any hours worked

                           over 40.



           Your method should be invoked after you compute gross pay with CalculateGross but

            before you compute net pay with CalculateNet  (i.e., between Lines 37 and 40).


          The new method is to be called CalculateOT , and it is to have to following method

            header:




                                                                                            Copy
            public static double CalculateOT(double hours, double rate)




https://loki.trentu.ca/courses/cois1020/06-methods2.html                                                                                               4/6
```

## PDF page 5

```text
21/11/2026, 22:00                                                    Lab 6 - COIS 1020

              In this method, both formal parameters are call by value with hours representing the

          number of hours work and rate representing the hourly wage.


           CalculateOT  is to return only the amount of overtime pay (in excess of regular pay)

           which is computed from the number of hours greater than 40 multiplied by the hourly

          wage and then multiplied by 0.5.




                         CalculateOT  is only returning the overtime amount which must be added

                                to the gross pay variable in Main() before netPay  is calculated



         Run the program using the input data: Smith, 40, 12.5, 0.2.


          What is the output?


           k. Run the program using input Smith, 44, 12.5, 0.2.




                       The grossPay for this data should be $575 and the netPay should be $460. If

                         you get a different answer, you've made a mistake and should revisit your

                           code.




          What is the output?


         How does the result differ from Part (i)?


                   l. Run the program using input Smith, 20, 12.5, 0.2.




                       The grossPay for this data should be $250 and the netPay should be $200. If

                         you get a different answer, you've made a mistake and should revisit your

                           code.




          What is the output?





https://loki.trentu.ca/courses/cois1020/06-methods2.html                                                                                               5/6
```

## PDF page 6

```text
21/11/2026, 22:00                                                    Lab 6 - COIS 1020




   You've now completed the lab! Demonstrate your completed lab for feedback and to receive your

   grade.


   You only need to submit on Blackboard if you didn't demonstrate and receive your mark in the lab!

   Please use File > Save  as, to save your document as a PDF. Upload your completed PDF and

   Lab6.cs to Blackboard. Please be sure to submit the files together in the same submission (not two

   separate submissions, since the marker will only look at your last one).





https://loki.trentu.ca/courses/cois1020/06-methods2.html                                                                                               6/6
```

