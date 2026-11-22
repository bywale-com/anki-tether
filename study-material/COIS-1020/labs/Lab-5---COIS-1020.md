# Lab 5 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 5 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 21:59                                                    Lab 5 - COIS 1020

               Trent University: COIS 1020H

       Lab 5: Introduction to Methods (with Debugging)





    This lab will introduce you to methods, parameter passing, and the helpfulness of the Debugger.


           a. Answer Template (One Drive, must be Trent Authenticated)


           Answer Template (GoogleDocs)


              Click one of the the links above to open this lab's answer template, use it to compile your answers to the lab

             questions below.


                                If using the OneDrive version, you'll need to download the file so you have a working copy.

                                If using the Google Docs version, click on File>Make a Copy to get your own copy of the file to work in.




                     When asked "What is the output", you need to copy and paste (or screen capture) what is seen in

                             the Output Window.


                      Be sure to copy the entire contents of the Output Window ... which includes prompt strings, input

                         and output (not just the last line).


                                                 If you screencapture, please only capture the relevant portion of the window (not your entire

                            desktop)




           b. Make a new Project in C# (Lab5). Delete the skeleton code, and rename Program.cs, to Lab5.cs.


                      If you don't remember the steps for creating a project from last week, you can open the section below to see

           them again (by clicking on the arrow):


              Reminder: Creating a C# Project in VS Code

            c. Paste the following code into your empty .cs file.




                                                                                                                Copy
              1   using System;
              2   public static class Lab5
              3   {
              4       public static void Main()
              5       {
              6           // declare variables
              7           int inpMark;
              8
https://loki.trentu.ca/courses/cois1020/05-methods.html                                                                                                1/5
```

## PDF page 2

```text
21/11/2026, 21:59                                                    Lab 5 - COIS 1020
              8
                          string lastName;
              9
                          char grade = ' ';
              10

              11
                          Console.Clear();
              12
                          // enter the student's last name
              13
                          Console.Write("Enter the last name of the student => ");
              14
                          lastName = Console.ReadLine();
              15
                          // enter (and validate) the mark
              16
                          do
              17
                          {
              18
                              Console.Write("Enter a mark between 0 and 100 => ");
              19
                              inpMark = Convert.ToInt32(Console.ReadLine());
              20
                          } while (inpMark < 0 || inpMark > 100);
              21
              22
                          // Use the method to convert the mark into a letter grade
              23
                          grade = MarkToGrade();
              24

              25
                          // print out the results
              26
                          Console.WriteLine("{0}'s mark of {1} converts to a {2}", lastName,
              27
                           inpMark, grade);
              28
                      }
              29

              30
                      // Method: MarkToGrade
              31
                      // Parameter
              32
                      //      mark: call by value parameter to be converted to a letter grade
              33
                      // Returns: the corresponding letter grade
              34
                      public static char MarkToGrade(int mark)
              35
                      {
              36
                          char letterValue;
              37
              38
                          // multi-alternative If statement to determine letter grade
              39
                          if(mark > 0 && mark < 50)
              40
                              letterValue = 'F';
              41
                          else if(mark >= 50 && mark < 60)
              42
                              letterValue = 'D';
              43
                          else if(mark >= 60 && mark < 75)
              44
                              letterValue = 'C';
              45
                          else if(mark >= 75 && mark < 85)
              46
                              letterValue = 'B';
              47
                          else if(mark >= 85 && mark <= 100)
              48
                              letterValue = 'A';
              49
                          else
              50
                          {
              51
                              Console.WriteLine("***Error - invalid mark");
              52
                              letterValue = 'X';
              53
                          }
              54
              55
                          //return the letter grade back to Main
              56
                          return letterValue;
              57
https://loki.trentu.ca/courses/cois1020/05-methods.html                                                                                                2/5
```

## PDF page 3

```text
21/11/2026, 21:59                                                    Lab 5 - COIS 1020
              57
                      }
              58
                  }



           d. Run the program using input Smith and 98


           What is the syntax error and how did you fix it?


           What is the output?


           e. Run the program using input Smith and 34


           What is the output?


                  f. Run the program using input Smith and 59


           What is the output?


           g. Run the program using input Smith and 72


           What is the output?


           h. Run the program using input Smith and 83


           What is the output?


                    i. Run the program using input Smith and then -1, 101 and 90 for the marks


           What is the output?


         Why do you think the input values for mark in Parts (d)-(i) were chosen?


                    j. Now we are going to see how the Debugger can help us understand the functionality of methods. Put in a

             Breakpoint ( F9 ) at the point where the method is invoked or called (Line 22). You will see that a red dot

            appears to the left of the line.


         Now run the program ( F5 ) using a last name of Smith and a mark of 75. Notice that the program stops at the

               line with the Breakpoint (and the line is now highlighted in yellow). Also notice that, like last week, a new

             sidebar has appeared with a panel labeled Locals that shows the current values for all the variables declared

               in Main() : inpMark , lastName , and grade .


            Step Into ( F11  or buttons) once and notice the program has jumped into the method MarkToGrade and the

             values in the Locals window now correspond to the variables and parameters of the method: mark and

           letterValue .


            Also notice further down in the new side panel in the Call Stack pane, there are two entries: one for Main

           and one for MarkToGrade with the later one active (appears in color). Continue to single step your program

https://loki.trentu.ca/courses/cois1020/05-methods.html                                                                                                3/5
```

## PDF page 4

```text
21/11/2026, 21:59                                                    Lab 5 - COIS 1020

                until you reach the return statement on Line 55.


             Single step from Line 55 and describe what you are seeing in terms of where you are in the program (line

            number), what is in the Locals window (variables and values), and what is in the Call Stack window (will require

            two to three more single steps to see the program jump.

            k. Remove the BreakPoint from Line 22 (press: F9  while on the line) . At Line 53, add the following statement:




                                                                                                                Copy
              53   Console.WriteLine("The value of the mark is {0}", inpMark);



           What error message did you receive and why?


                    l. Remove the extra line you added in Part (k). Now let’s change the method header to include a call by address

              (reference) parameter. Change Line 33 to be:




                                                                                                                Copy
              33   public static void MarkToGrade(int mark, ref char letterValue)


          Remove Lines 35 ( char letterValue; ) and 55 ( return letterValue; ))


          Change Line 22 to be:




                                                                                                                Copy
              22   MarkToGrade(inpMark, ref grade);


          Run the program with the input of Smith and 98.


           What is the output?


           What do you notice about the output relative to what you saw in Part (d)?


         Why did we have to remove Line 35 (try putting it back in)?


         Why did we have to remove Line 55 (try putting it back in)?


         Why did the method call (invocation) in Line 22 have to change?


        m. One last set of changes to the program from Part (l). In the method call (Line 22), change it to:




                                                                                                                Copy
              22   grade = MarkToGrade(inpMark);



           What error message did you receive and why?


          What if we change Line 22 to:

https://loki.trentu.ca/courses/cois1020/05-methods.html                                                                                                4/5
```

## PDF page 5

```text
21/11/2026, 21:59                                                    Lab 5 - COIS 1020


                                                                                                                Copy
              22   grade = MarkToGrade(inpMark, ref grade);



           What error message did you receive and why?


                Finally, how about if we change Line 22 to:




                                                                                                                Copy
              22   MarkToGrade(ref grade, inpMark);



           What error messages did you receive and why?





    You've now completed the lab! Demonstrate your completed lab for feedback and to receive your grade.


   You only need to submit on Blackboard if you didn't demonstrate and receive your mark in the lab! Please use File >

    Save  as, to save your document as a PDF. Upload your completed PDF to Blackboard. Please be sure to submit the

     files together in the same submission (not two separate submissions, since the marker will only look at your last one).





https://loki.trentu.ca/courses/cois1020/05-methods.html                                                                                                5/5
```

