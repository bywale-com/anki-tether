# Lab 1 - COIS 1020.pdf

Source: `source-material/cois-anki-tether/Lab 1 - COIS 1020.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
21/11/2026, 21:58                                                    Lab 1 - COIS 1020

          Trent University: COIS 1020H

  Lab 1: Getting familiar with MS Visual Studio Code





   The goal of this lab is to get the software installed, have you use it to create a simple program, and

   get you used to the submission process.





   For completion of this lab, you are required to create and run a simple program (see below), and

   then submit your code file (the .cs) as well as a screen capture (.png or .jpg) of the output window

    to the Lab 1 Dropbox on BlackBoard Learn. Unless you are unable to attend the lab period, DO

  NOT submit on Blackboard until after you've demo'd to the lab demonstrator.





  Part One - Installing and Configuring VS

 Code



   Follow the setup instructions to complete installation and setup.





https://loki.trentu.ca/courses/cois1020/01-intro.html                                                                                                    1/7
```

## PDF page 2

```text
21/11/2026, 21:58                                                    Lab 1 - COIS 1020



  Part Two - Creating a .NET project



   This section will teach you to create a C# project in VS Code.


       1. There are two different methods to trigger the creation of a C# project:

              a. Go to the Explorer View (     ) in the Activity Panel and select Create .NET Project

              b. Launch the Command Palette Ctrl + Shift + P and then type .NET and find and

                select the .NET: New Project command

       2. Next you'll need to choose a project template. For this course, the project template will

        always be: Console App





       3. Next you'll need to specify where you want to save your project. You will need to create a

          folder for your lab to be saved in. You should always create a new folder for each project

       you work on. I'd strongly suggest you first create a folder that is going to hold all your

        course work and put your project folder in it. Call your folder Lab1.




                                          If you're using a Lab Machine, you must save your projects on the network

                         storage associated with your account. You'll find this under This PC, and it will


https://loki.trentu.ca/courses/cois1020/01-intro.html                                                                                                    2/7
```

## PDF page 3

```text
21/11/2026, 21:58                                                    Lab 1 - COIS 1020

                    show up as yourtrentusername (\\habitat...).




       4. You will probably see a prompt asking if you trust the author of files in this folder. If you

         created a parent folder for your all your projects, select the checkbox saying to trust all files

           in the parent folder (this will save you from having to answer this question every time),

         otherwise, you should ignore the checkbox. Press the Yes I trust the authors button.





       5. You'll then be asked to name your C# project. Call it Lab1





       6. Lastly, you will verify the combined project name and location, giving VS Code permission to

         create the necessary files.





https://loki.trentu.ca/courses/cois1020/01-intro.html                                                                                                    3/7
```

## PDF page 4

```text
21/11/2026, 21:58                                                    Lab 1 - COIS 1020





   Your first project is now setup!





  Part Three - Completing Your First .NET

  Project



       1. Go to the Explorer View and locate the Program.cs file that was created. Rename this file

         Lab1.cs. Open your renamed file.

       2. Replace all the code that was inserted automatically with the following:




                                                                                       Copy Code
           1   using System;
           2   public static class Lab1
           3   {
           4       public static void Main()
           5       {
           6           Console.WriteLine("Hello COIS1020H, my name is xxx");
           7       }
           8   }


       3. On line 6, change xxx to your name.




                     Lab instructions that reference line numbers will always refer to the numbers in

                        our example. In many cases, these may not be exactly the same as the line





https://loki.trentu.ca/courses/cois1020/01-intro.html                                                                                                    4/7
```

## PDF page 5

```text
21/11/2026, 21:58                                                    Lab 1 - COIS 1020

                     numbers in your code. Be sure to look at the appropriate line in our example to

                   make sure you know which line is being referenced.



       4. Use F5  to run your program.




                                          If you're using a laptop who's function keys are mapped to things like brightness

                     and volume, you will probably need to press Fn + F5




       5. The first time you run a program, you will be prompted to choose a Debugger. You should

        choose C#





                                          If you receive an error saying No C# project currently loaded (this seems to

                     happen mostly on lab machines). Use these steps to resolve the issue:

                                a. Open the Command Palette: Press Ctrl + Shift + P  .

                                b. Select the Command: Type and select >.NET: Generate Assets for Build

                                   and Debug  .




       6. You will also be asked to choose a Launch Configuration, there should only be one option,

        based on your project name.





       7. Your program will now run and you'll see the output in the Terminal Window.





https://loki.trentu.ca/courses/cois1020/01-intro.html                                                                                                    5/7
```

## PDF page 6

```text
21/11/2026, 21:58                                                    Lab 1 - COIS 1020





       8. Notice the garbage that appears before your Hello COIS1020 output, which is a result of VS

       Code launching our program. We can clean up our output by including a Console.Clear()

         before we write anything to the screen. Add this to your program before the

        Console.WriteLine and run it again. Your console should now be limited to the actual

         output of the program.





         Note: Your command prompt (the part that appears after the Hello COIS1020 line), will look

           different then mine, and will probably be the path to your Project.


       9. Take a screenshot of your final output.




                     Lab 1 in COIS1010 has a good introduction to the various methods of screen-

                          capturing if you need the refresher.




        To keep submissions small and easy for the marker to read, you should always

        screenshot only relevant portion of the window. We will deduct marks for poorly sized or

          blurry screenshots. For example, your screen capture for Lab 1 should look similar to this:





https://loki.trentu.ca/courses/cois1020/01-intro.html                                                                                                    6/7
```

## PDF page 7

```text
21/11/2026, 21:58                                                    Lab 1 - COIS 1020


                     You can do this with:

                           Pre-Windows 10 (or really out-of-date Windows 10) - Snipping Tool

                         Windows 10 - Snip & Sketch

                         Windows 11 - Snipping Tool




     10. Upload your screenshot and your Lab1.cs file to the Lab1 DropBox on Blackboard.




                                          If you don't see the extensions of your files, you should turn on File Extensions

                            to make it easy to see the correct files to submit. You can learn how in this

                          Microsoft Support Article.





https://loki.trentu.ca/courses/cois1020/01-intro.html                                                                                                    7/7
```

