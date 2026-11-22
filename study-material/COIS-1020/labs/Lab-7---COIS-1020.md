# Lab 7 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 7 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 22:00                                                    Lab 7 - COIS 1020

               Trent University: COIS 1020H

                     Lab 7: Arrays





    In this lab, we would like to introduce you to arrays, parameter passing, and the more uses of the Debugger.


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




           b. Make a new Project in C# (Lab7). Delete the skeleton code, and rename Program.cs, to Lab7.cs.


                      If you don't remember the steps for creating a project from last week, you can open the section below to see

           them again (by clicking on the arrow):


              Reminder: Creating a C# Project in VS Code

            c. Paste the following code into your empty .cs file.




                                                                                                                Copy
                  using System;
                  public static class Lab7
                  {
                      public static void Main()
                      {

                          string[] dataArray = new string[10] {"a","b","c","d","e","f","g","h","i","
                          int n = 0;

              8
https://loki.trentu.ca/courses/cois1020/07-arrays.html                                                                                                   1/5
```

## PDF page 2

```text
21/11/2026, 22:00                                                    Lab 7 - COIS 1020
              8
              9
                          Console.Clear();
              10
                          // Fill the array
              11
                          Fill(dataArray, ref n);
              12

              13
                          // Display the array contents
              14
                          Dump();
              15
              16
                      }
              17
              18
                      // Method:       Fill
              19
                      // Description:  Fill an array with values.
              20
                      // Parameters:   arrValues: the array to fill.
              21
                      //               num: number of elements in the array.
              22
                      // Returns:      void
              23
                      public static void Fill(string[] arrValues, ref int num)
              24
                      {
              25
                          // input the number of data values to put in the array
              26
                          do
              27
                          {
              28
                              Console.Write("Enter the number of elements (between 0 and 10) => ");
              29
                              num = Convert.ToInt32(Console.ReadLine());
              30
                          } while (num < 0 || num > 10);
              31

              32
                          // loop to enter the values, using the loop counter (i)
              33
                          // to access consecutive positions in the array
              34
                          for (int i = 0; i < num; ++i)
              35
                          {
              36
                              Console.Write("Enter name {0} => ", i);
              37
                              arrValues[i] = Console.ReadLine();
              38
                          }
              39
                      }
              40
              41
                      // Method:       Dump
              42
                      // Description:  Display the contents of an array.
              43
                      // Parameters:   arrVals: array to be displayed.
              44
                      //               num: number of elements in the array.
              45
                      // Returns:      void
              46
                      public static void Dump(string[] arrVals, int num)
              47
                      {
              48
                          // output the values from the array
              49
                          Console.WriteLine("\nThe elements in the array are:");
              50
                          for (int i = 0; i < num; ++i)
              51
                              Console.WriteLine(" {0}", arrVals[i]);
              52
                      }
              53
              54
                  }




https://loki.trentu.ca/courses/cois1020/07-arrays.html                                                                                                   2/5
```

## PDF page 3

```text
21/11/2026, 22:00                                                    Lab 7 - COIS 1020

             This program focuses on arrays and uses two user-defined methods: one to have the user fill up an array and

             the second to print out the contents of an array.


             Notice again how we simplify Main() and leave much of the real work to the user-defined methods. There is

           one syntax error in this program that needs to be fixed before it will compile.


           d. Run the program using input 4, Rich, Mary, Bob, Sue




                             Note: With the provided input, the first number (4) is the number of elements while the remaining

                         numbers are to be used each time it prompts to enter another element.




           What is the syntax error and how did you fix it?


           What is the output?


           e. Run the program using input -2, 15, 4,Rich, Mary, Bob, Sue


           What is the output?


         Why is it the same as in Part (d) even though the input is not the same?


                  f. Now we are going to again investigate the usefulness of the Debugger. Put in two Breakpoints ( F9 ): one at

             the point where the method Fill  is invoked (Line 11) and one where Dump  is invoked (Line 14). You will

           see both lines will have a red dot to the left of the line.


           g. Now run the program ( F5 ) using the input of 4, Rich, Mary, Bob, Sue.


             Notice that the program stops before you enter any input. This is due to the fact that the program has not

            invoked the method where the data is input ( Fill ).


           Look at the Locals window new sidebar. Notice that there are two identifiers in this window: dataArray and

           n . The identifier dataArray has a   preceding it indicating that it is a complex data type that contains

              additional information ( n  is a scalar (or simple) data type that contains the number 0).


              Click on the  and you will see the contents of dataArray (the numbers 9 - 0 that the array was initialized

               with). Step Into ( F11  or button) once and notice the program has jumped into the method Fill and the

             values in the Locals window now correspond to the variables and parameters of the method: arrValues and

           num .


           What are the values in arrValues and num in Fill ?


           h. Press ( F5 ) to resume your program from the current instruction and notice that it provides you the

             opportunity now to input the data. Once you are done inputting the data: 4, Rich, Mary, Bob, Sue, the program

                 will continue to the next breakpoint or to the end if there are not more breakpoints. In your case, the program


https://loki.trentu.ca/courses/cois1020/07-arrays.html                                                                                                   3/5
```

## PDF page 4

```text
21/11/2026, 22:00                                                    Lab 7 - COIS 1020

                 will stop at the second breakpoint on Line 14 (call to Dump ). From the Locals window examine dataArray

           and n .


           What are the values in dataArray and n in Main ?


         Why have they changed?


                    i. Single step ( F11  or button) once again and notice the program has jumped into the method Dump and the

             values in the Locals window now correspond to the variables and parameters of the method: arrVals and

           num .


           What are the values in arrVals and num in Dump


                    j. Single step ( F11  or button) your way through Dump  until at least 2 values from the array are printed on the

             output screen and then press ( F5 ) to move to the end of the program.


           What is the output?


         Why are only 4 values from the array being output given that you know from Part (i) that there were 10 values in

             the array that was to be printed?


            k. Remove the breakpoints from Lines 11 and 14. Let's add another user-defined method to the program.


             This method, called ReverseDump  is to output the values in the array in reverse order.




                           Please note that you are NOT to use the Array.Reverse method from the Array class. The goal here

                                      is to practice traversing an array yourself.



          The approach is quite simple: your ReverseDump method will look very similar to the Dump method with the

             exception that the for loop will count backwards from from the end of the array to the beginning.




                        Remember: because array indices start at position 0, the position of the last element in the array

                                       will always be 1 less then the number of elements in the array.




          The method header will look like:




                                                                                                                Copy
             public static void ReverseDump(string[] arrItems, int num)



             Provide the code you wrote for the ReverseDump method .


             Provide the code you added ReverseDump  call (in Main ).


https://loki.trentu.ca/courses/cois1020/07-arrays.html                                                                                                   4/5
```

## PDF page 5

```text
21/11/2026, 22:00                                                    Lab 7 - COIS 1020

           What is the output?


                    l. Let's add one last user-defined method to the program.


             This method, called FindName , is to return an integer representing the index (position) in the array where the

          name is found or -1 otherwise.


          The approach is to use a simple for loop to search the array and examine each location to see if the name

             stored at the location is what you are searching for. If it is, return the array index. If you search the entire array

           and do not find the name, return a -1.


          The method header will look like:




                                                                                                                Copy
             public static int FindName(string name, string[] arrItems, int num)



          Add the following lines of code to Main after the call to ReverseDump .




                                                                                                                Copy
             string locateName = "Sue";
             int found = FindName(locateName, dataArray, n);
             if(found >= 0)

                   Console.WriteLine("{0} was found in the array", locateName);
             else
                   Console.WriteLine("{0} does not exist in the array", locateName);



             Provide the details (the code) of your FindName method.


            Using the input 4, Rich, Mary, Bob, Sue, What is the output?


        m. Change the contents of the variable locateName to Fred and rerun the program with the input 4, Rich, Mary,

              Bob, Sue


           What is the output?





    You've now completed the lab! Demonstrate your completed lab for feedback and to receive your grade.


   You only need to submit on Blackboard if you didn't demonstrate and receive your mark in the lab! Please use File >

    Save  as, to save your document as a PDF. Upload your completed PDF to Blackboard (you don't need to submit your

   code file).





https://loki.trentu.ca/courses/cois1020/07-arrays.html                                                                                                   5/5
```

