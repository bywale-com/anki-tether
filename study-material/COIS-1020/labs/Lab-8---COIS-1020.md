# Lab 8 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 8 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 22:00                                                    Lab 8 - COIS 1020

          Trent University: COIS 1020H

           Lab 8: Arrays - More Arrays





  Question 1



  A very common application of arrays is computing statistics on lists of numbers. Below you will find

   a template of a program that uses four user-defined methods to: input an array of numbers,

   compute the average the array, find the largest number in the array, and find the smallest number

    in the array.


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




https://loki.trentu.ca/courses/cois1020/08-arrays2.html                                                                                                 1/5
```

## PDF page 2

```text
21/11/2026, 22:00                                                    Lab 8 - COIS 1020

                                                If you screencapture, please only capture the relevant portion of the window

                               (not your entire desktop)




          b. Make a new Project in C# (Lab8). Delete the skeleton code, and rename Program.cs, to

            Lab8.cs.


                     If you don't remember the steps for creating a project from last week, you can open the

             section below to see them again (by clicking on the arrow):


             Reminder: Creating a C# Project in VS Code

           c. Paste the following code into your empty .cs file.




                                                                                            Copy
                 // Name: xxxxxxxxxxxxx
                 // Student Number: xxxxxxx
                 // Lab 8
                 // Program Description: This program uses four user-defined method
                 //    to input an array of numbers, one to compute the average the
                 //    to find the largest number in the array, and one to find the
                 //    number in the array.


                 using System;
                 public static class Lab8
                 {
                    public static void Main()
                    {
                       int[] compStats = new int[25];
                       int n = 0, large, small;
                       double avg = 0;


                       Console.Clear();
                       // Input values into the array
                       InpArray(compStats, ref n);


                       // Find the average of the elements in the array
                       // *** Insert the code for the call to the FindAverage metho


                       // Find the largest element in the array
                       // *** Insert the code for the call to the FindLarge method

https://loki.trentu.ca/courses/cois1020/08-arrays2.html                                                                                                 2/5
```

## PDF page 3

```text
21/11/2026, 22:00                                                    Lab 8 - COIS 1020


                       // Find the smallest element in the array
                       // *** Insert the code of the call to the FindSmall method


                       // Print out the results
                       Console.WriteLine("\nThe Average of the array is {0:F2}", av
                       // *** Insert the code to print out the largest and smallest


                    }


                    // Method:       InpArray
                    // Description:  Input values into an array.
                    // Parameters:   arrValues: the array to fill.
                    //               num: number of elements in the array.
                    // Returns:      void
                    public static void InpArray(int[] arrValues, ref int num)
                    {
                       // input the number of data values to put in the array
                       do
                       {
                           Console.Write("Enter the number of elements (<= 25) => "
                           num = Convert.ToInt32(Console.ReadLine());
                       } while (num < 0 || num > 25);


                       // loop to enter the values
                       for (int i = 0; i < num; ++i)
                       {
                           Console.Write("Enter the Element {0} => ", i);
                           arrValues[i] = Convert.ToInt32(Console.ReadLine());
                       }
                    }


                    // Method:       FindAverage
                    // Description:  Computes the average of the elements in the ar
                    // Parameters:   arrVals: array to be processed
                    //               num: number of elements in the array.
                    // Returns:      the average of the elements in the array
                    public static double FindAverage(int[] arrVals, int num)
                    {
                       // *** Insert the details of the FindAverage Method


https://loki.trentu.ca/courses/cois1020/08-arrays2.html                                                                                                 3/5
```

## PDF page 4

```text
21/11/2026, 22:00                                                    Lab 8 - COIS 1020

                    }             68
             69
                    // Method:       FindLarge             70
                    // Description:  Determines the largest element in the array.             71
                    // Parameters:   arrVals: array to be processed             72
                    //               num: number of elements in the array.             73
                    // Returns:      the largest element in the array             74
                    public static int FindLarge(int[] arrVals, int num)             75
                    {             76
                       // *** Insert the details of the FindLarge Method             77
                       // *** Do not use built in C# array functions (like Sort or             78
                       // *** it should be done using iteration.             79
                    }             80
             81
                    // Method:       FindSmall             82
                    // Description:  Determines the smallest element in the array.             83
                    // Parameters:   arrVals: array to be processed             84
                    //               num: number of elements in the array.             85
                    // Returns:      the smallest element in the array             86
                    public static int FindSmall(int[] arrVals, int num)             87
                    {             88
                       // *** Insert the details of the FindSmall Method             89
                       // *** Do not use built in C# array functions (like Sort or             90
                       // *** it should be done using iteration.             91
                    }             92
                 }



          d. Replace the lines marked with // *** with the appropriate C# code (may require more

            than one line of code to complete the missing parts).

          e. Once you are comfortable that your program works correctly, test it with the following 4

            sets of inputs and for each output, include a screen capture for each in your Answer Doc

               for this lab. (use a screen capture tool such as Snipping Tool or Snip & Sketch ).



        Tests



            Enter the comma separated values, one for each prompt:

https://loki.trentu.ca/courses/cois1020/08-arrays2.html                                                                                                 4/5
```

## PDF page 5

```text
21/11/2026, 22:00                                                    Lab 8 - COIS 1020

                 a.  5 , 2 , 4 , 6 , 8 , 1 (the results should be: Average: 4.20, Largest: 8 and

                   Smallest: 1 )

                 b.  3 , 5 , -2 , 6 , (the results should be: Average: 3.00, Largest: 6 and Smallest: -2 )

                  c.  0 (the results should be: Average: 0.00, Largest: 0 and Smallest: 0 )

                 d.  3 , -5 , -4 , -6 , (the results should be: Average: -5.00, Largest: -4 and Smallest:

                   -6 )





   You've now completed the lab! Demonstrate your completed lab for feedback and to receive your

   grade.


   You only need to submit on Blackboard if you didn't demonstrate and receive your mark in the lab!

   Please use File > Save  as, to save your document as a PDF. Upload your completed PDF and

   Lab8.cs to Blackboard. Please be sure to submit the files together in the same submission (not two

   separate submissions, since the marker will only look at your last one).





https://loki.trentu.ca/courses/cois1020/08-arrays2.html                                                                                                 5/5
```

