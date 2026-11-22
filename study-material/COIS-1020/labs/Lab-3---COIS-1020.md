# Lab 3 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 3 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 21:59                                                    Lab 3 - COIS 1020

                   Trent University: COIS 1020H

           Lab 3: More Input/Output & Selection Statements





                The first question in this lab again deals with outputting currency values. Because the currency symbol displayed

                        in the console is controlled by your operating system's currency settings, some of you probably won't see a $, but

                    instead will see whatever your local currency symbol is. Don't worry about it.


                    This will seem extra odd when the user is entering the number of Canadian coins, but if your results don't show a

             CDN $. That's ok, the markers are used to this!




  Part One



    For the first part of the lab, you are required to complete the following program that computes the amount of money in a piggy-bank

    based on the number of each type of coin: pennies, nickels, dimes, quarters, one dollar coins (loonies), and two dollar coins (twoonies).

    The program prompts the user for their name and the number of each type of coin. The program then computes the amount in the piggy

    bank and prints the result in an appropriate fashion (dollar sign and two digits after the decimal point).


            a. Answer Template (One Drive, must be Trent Authenticated)


           Answer Template (GoogleDocs)


               Click one of the the links above to open this lab's answer template, use it to compile your answers to the lab questions below.


                                 If using the OneDrive version, you'll need to download the file so you have a working copy.

                                 If using the Google Docs version, click on File>Make a Copy to get your own copy of the file to work in.




                     When asked "What is the output", you need to copy and paste (or screen capture) what is seen in the Output

                          Window.


                       Be sure to copy the entire contents of the Output Window ... which includes prompt strings, input and output (not

                                    just the last line).


                                                  If you screencapture, please only capture the relevant portion of the window (not your entire desktop)




            b. Create a new C# project in Visual Studio named Lab3_1. Delete the skeleton code, and rename the Program.cs to Lab3_1.cs


                       If you don't remember the steps for creating a project from last week, you can open the section below to see them again (by

               clicking on the arrow):


              Reminder: Creating a C# Project in VS Code



https://loki.trentu.ca/courses/cois1020/03-input-output-selection.html                                                                                    1/5
```

## PDF page 2

```text
21/11/2026, 21:59                                                    Lab 3 - COIS 1020

             c. Paste the following code in your project and replace (or complete) the lines marked with // *** using the appropriate C#

            code (you may require more than one line of code to complete the missing parts).




                                                                                                                                Copy
               1   // Name: xxxxxxxxxxxxx
               2       // Student Number: xxxxxxx
               3       // Lab 3, Part 1
               4       // Program Description: This program computes the amount of money in a
               5       //     piggy-bank given the number of pennies, nickels, dimes, quarters,
               6       //     loonies, and twoonies.
               7
               8       using System;
               9       public static class Lab3_1
              10       {
              11         public static void Main()
              12         {
              13             // declare the variables and constants
              14             int numPens, numNicks, numDimes, numQuarts, numLoons, numTwoons;
              15             double amtInPiggyBank;
              16             string name;
              17             Console.Clear();
              18             // Input the name of the user
              19             Console.Write("Enter your name => ");
              20             name = Console.ReadLine();
              21             // Input the number of pennies
              22             Console.Write("Enter the number of pennies in the Piggy Bank => ");
              23             numPens = Convert.ToInt32(Console.ReadLine());
              24             // Input the number of nickels
              25             Console.Write("Enter the number of nickels in the Piggy Bank => ");
              26             numNicks = Convert.ToInt32(Console.ReadLine());
              27             // Input the number of dimes
              28             //*** Insert code in input the number of dimes
              29             // Input the number of quarters
              30             //*** Insert code in input the number of quarters
              31             // Input the number of loonies
              32             //*** Insert code in input the number of loonies
              33             // Input the number of twoonies
              34             //*** Insert code in input the number of twoonies
              35             // Compute the amount in the Piggy Bank
              36             //*** Complete the following statement to include dimes,
              37             //*** quarters, loonies and twoonies
              38             amtInPiggyBank = numPens * 0.01 + numNicks * 0.05;
              39             // Print out the amount in the Piggy Bank
              40             //*** Fix the following statement so it prints a $ and two digits
              41             //*** after the decimal point
              42             Console.WriteLine("{0} has {1} in the Piggy Bank", name, amtInPiggyBank);
              43         }
              44       }





                            For those of you not used to CDN currency. The CDN coins and their corresponding values are:

                              Dimes are worth 10 cents

                                   Quarters are worth 25 cents

                                  Loonies are worth 1 dollar

https://loki.trentu.ca/courses/cois1020/03-input-output-selection.html                                                                                    2/5
```

## PDF page 3

```text
21/11/2026, 21:59                                                    Lab 3 - COIS 1020

                                Twoonies are worth 2 dollars

                        Where there are 100 cents in a dollar.




            d. Once you are comfortable that your program works correctly, test it with the following 3 sets of inputs and for each output,

              include a screen capture for each in your Answer Document for this lab. (use a screen capture tool such as Snipping Tool or

             Snip & Sketch ).




         Tests



             Enter the comma separated values, one for each prompt:

                  a.  Rich , 2 , 4 , 3 , 8 , 2 , 1 (the money in the piggy bank should be $6.52)

                  b.  Mary , 3 , 2 , 10 , 4 , 5 , 8 (the money in the piggy bank should be $23.13)

                    c.  Bob , 0 , 0 , 0 , 0 , 0 , 0 (the money in the piggy bank should be $0.00)





  Part Two



    The second part of this lab aims introduce you to Selection Statements (more specifically IF statements) and the Debugger that is

     available for you to use in Visual Studio Code. Answer the highlighted questions in your Lab 3 answer doc.


     This program uses an if statement to compute the postal charge for package delivery (there are various classes of packages based

    on weight plus a flat charge of $1.25 for every package). The program prompts the user for weight (double) and then computes and

     output the cost (double).


            a. Open a new instance of VS Code by going to File > New Window. If you're in Lab, leave Part One open for later so you can use

                         it to demo.

            b. Create a New Project (use Lab3_2 for both the Project and Code File names), and be sure to delete the skeleton code, then

           add the following code to your new project. There is one syntax error in this program that you will need to fix before it will

              compile.




                       Be careful as the error message may not be the exact error. Look carefully at the whole line where the error

                            occurs and compare it to similar lines.





                                                                                                                                Copy
               1   using System;
               2       public static class Lab3_2
               3       {
               4        public static void Main()
               5        {
               6            // declare the variables and constants
               7            const double FLAT = 1.25;
               8            double weight;

https://loki.trentu.ca/courses/cois1020/03-input-output-selection.html                                                                                    3/5
```

## PDF page 4

```text
21/11/2026, 21:59                                                    Lab 3 - COIS 1020
               9            double cost, pricePerKg = 0;
              10
              11            Console.Clear();
              12            // Input the weight
              13            Console.Write("Enter a positive weight of the package => ");
              14            weight = Convert.ToDouble(Console.ReadLine());
              15           // Determine the cost per kilogram
              16           if (weight <= 0)
              17              Console.WriteLine("*** Invalid weight");
              18           else if (weight < 1)
              19              pricePerKg = 0.25;
              20           else if (weight <= 3.5)
              21              pricePerKg = 0.5;
              22           else (weight > 3.5)
              23              pricePerKg = 1.0;
              24           // Compute the cost to send the package
              25           if (weight > 0)
              26              cost = weight * pricePerKg + FLAT;
              27           else
              28              cost = 0;
              29           // Output the results
              30           Console.WriteLine("The cost to send the package is {0:C}", cost);
              31         }
              32       }




           What is the syntax error and how did you fix it?


             c. Run the program using an input weight of 2.5


           What is the output?


            d. Run the program using an input weight of 4


           What is the output?


            e. Run the program using an input weight of 0.5


           What is the output?


                   f. Run the program using an input weight of -1


           What is the output?


          Why do you think the input values for weight in Parts (c) through (f) were chosen?


            g. Now we are going to introduce a very helpful set of tools for finding semantic (logic) errors (i.e., your program compiles but

            produces the wrong answer).


           The first debugging tool is the Breakpoint ( F9 ). A Breakpoint causes a program to stop at an executable statement. Let's put

                in a Breakpoint at Line 16:




                                                                                                                                Copy
              16   if(weight<=0)


https://loki.trentu.ca/courses/cois1020/03-input-output-selection.html                                                                                    4/5
```

## PDF page 5

```text
21/11/2026, 21:59                                                    Lab 3 - COIS 1020

          Move your cursor to that line and press F9  . You will see that there is a red dot to the left of the line.


         Now run the program ( F5 ) using a weight input of 2.5 . Notice that the program stops at the line with the Breakpoint (and the

                line is now highlighted in yellow).


             Also notice that a new sidebar has appears beside the Activity Bar at the top of which is a window labeled Locals that shows

              the current values for all the variables declared in Main() .


           Use Step Into ( F11 ) to single step your way through the program (paying notice to how the values in the Locals window

           change and which line is highlighted yellow).


           You can also use the buttons that appear once you've stopped on a breakpoint for stepping.





             Describe what you are seeing as you single step through the program.


            h. Repeat Part (g) once for each of the following weight inputs: 4 , 0.5 , and -1 .


          Comment on what you see. How was each run different in regards to the flow of execution and what you saw in the locals window?





    You've now completed the lab! Demonstrate your completed lab for feedback and to receive your grade.


    You only need to submit on Blackboard if you didn't demonstrate and receive your mark in the lab! Please use File > Save  as, to save

    your document as a PDF. Upload your completed PDF, and Lab3_1.cs to Blackboard (you do not need to submit your code file for

     question 2). Please be sure to submit the files together in the same submission (not two separate submissions, since the marker will

     only look at your last one).





https://loki.trentu.ca/courses/cois1020/03-input-output-selection.html                                                                                    5/5
```

