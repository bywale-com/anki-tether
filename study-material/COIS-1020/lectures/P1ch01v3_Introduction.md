# P1ch01v3_Introduction.pdf

Source: `source-material/P1ch01v3_Introduction.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H:
Programming for Computing
        Systems

           using
      Microsoft Visual C#

            Chapter 1
    A First Program Using C#
```

## PDF page 2

```text
Why Programming

• Give me examples of systems, apps, devices, etc.,
  that we use in everyday activities!!
   – Phones and mobile apps
   – Games
   – Banks
   – Hospitals
   – ….
• Who designed and implemented these systems??





                                                                                      2
```

## PDF page 3

```text
What is Programming

• Something Mysterious?!!
   – No

• Programming is about
   – Solving problems
   – Designing instructions
   – Developing new things

• Like learning a new language
    • You talk with the computer.

                                                                                      3
```

## PDF page 4

```text
In this course

•  First program


• Face errors!
   – And issues


• Key success factors
   – Curiosity
   – Patience
   – Practice       GET YOUR HANDS DIRTY!!!



                                                                                      4
```

## PDF page 5

```text
Programming

• Computer program
   – Set of instructions that tells a computer what to do
   – Also called software


• Software comes in two broad categories
   – System software
         • administer the system resources.
         • Essential to run the system
   – Application software (or Apps)
         • Carry specific users’ needs



                                                                                      5
```

## PDF page 6

```text
Programming (cont'd.)

• Machine language
   – Expressed as a series of 1s and 0s
         • 1s represent switches that are on, and 0s represent
         switches that are off
         • Understandable to a computer
• High-level programming languages
   – Use reasonable terms such as “read,” “write,” or “add”
         • Instead of the sequence of on/off switches that perform
        these tasks
   – Has its own syntax (rules of the language)
         • E.g., “print” or “write”


                                                                                      6
```

## PDF page 7

```text
C# Example                 Machine Code

•  int x = 5;                           • 10111000 00000101
•  int y = 3;                           • 10111011 00000011
•  int sum = x + y;                   • 00000001 11011000





                                                                                          7
```

## PDF page 8

```text
Programming (cont'd.)

• Compiler/Interpreter/Assembler
   – Translates programs statements into machine
     language (or machine code)
• Programming logic
   – Involves executing the various statements and
     procedures in the correct order
         • To produce the desired results
• Debugging
   – Process of removing all syntax and logical errors
     from the program


                                                                                      8
```

## PDF page 9

```text
Procedural and Object-Oriented
          Programming

• Procedural program
   – Create and name computer memory locations that
     can hold values (variables)
   – A series of steps or operations to manipulate those
     values
• Procedures/methods
   – Logical units that group individual operations in a
     program
   – Called or invoked by other procedures/methods





                                                                                      9
```

## PDF page 10

```text
The C# Programming Language

• Developed as an object-oriented language
•  Part of Microsoft Visual Studio
   – Thus, contains a simple GUI interface

• Modeled after the C++ programming language
   – eliminates some of the most difficult features


• Very similar to Java syntactically





                                                                                    12
```

## PDF page 11

```text
Writing a C# Program that Produces
             Output

access modifier                            identifier

                                                                         literal string

      public static class FirstClass
      {
          public static void Main()
          {
              System.Console.WriteLine("This is my first C# program");
              Console.ReadLine();
          }
      }
                                  method                                                      argument
       namespace




                                                                                       14
```

## PDF page 12

```text
Writing a C# Program that Produces
          Output (cont'd.)

• Namespace
   – Provides a way to group similar classes (more later)





         Lumber Toolbox                      Mechanic Toolbox
                                                                                    15
```

## PDF page 13

```text
Writing a C# Program that Produces
          Output (cont'd.)

• Access modifier
   – Defines the circumstances under which the method
     can be accessed



• Keywords
   – Predefined and reserved identifiers that have special
    meaning to the compiler





                                                                                    16
```

## PDF page 14

```text
Writing a C# Program that Produces
          Output (cont'd.)

• Whitespace
   – Any combination of spaces, tabs, and carriage
     returns (blank lines)
   – Organizes your code and makes it easier to read





                                                                                    17
```

## PDF page 15

```text
Writing a C# Program that Produces
          Output (cont'd.)

• C# method parts
   – Method header

         • Includes the method name and information about how
         information will be shared with the method
   – Method body
         • Contained within a pair of curly braces and includes all
         the instructions executed by the method




                   public static void Main()
                      {
                          System.Console.WriteLine("This is my first C# program");
                      }


                                                                                    18
```

## PDF page 16

```text
Writing a C# Program that Produces
          Output (cont'd.)


• The name of the method is Main()
   – Every console application must have a Main()
    method

• The method returns nothing as indicated by the
  keyword void



         public static void Main()
            {
               System.Console.WriteLine("This is my first C# program");
            }

                                                                                    19
```

## PDF page 17

```text
Selecting Identifiers

• Requirements
   – Must begin with an underscore, at sign (@), or letter
         • Letters include foreign-alphabet letters


   – Can contain only letters, digits, underscores, and the
      at sign
         • Not special characters such as #, $, or &


   – Cannot be a C# reserved keyword




                                                                                    20
```

## PDF page 18

```text
21
```

## PDF page 19

```text
Selecting Identifiers (cont'd.)





 The Rules:
      •   Starts with _, @, or letter
      •  contains letters, digits, _ , and the @
      •  Not a reserved keyword

                                                                        22
```

## PDF page 20

```text
Selecting Identifiers (cont'd.)





                 The Rules:
                           • Starts with _, @, or letter
                           • contains letters, digits, _ ,
                     and the @
                           • Not a reserved keyword





                                                                        23
```

## PDF page 21

```text
Selecting Identifiers (cont'd.)





                                                                        24
```

## PDF page 22

```text
Selecting Identifiers (cont’d.)





                                                                         25
```

## PDF page 23

```text
Selecting Identifiers (cont'd.)





                                                                        26
```

## PDF page 24

```text
Improving Programs by Adding
        Program Comments

• Program comments
   – Non-executing statements that document a program


• Comment out
   – Turn a statement into a comment


• Types of comments in C#
   – Line comments                     //
   – Block comments                /* … */



                                                                                    27
```

## PDF page 25

```text
Adding Comments to a Program

• Line comment example
    // Filename Hello.cs
    // Written by <your name>
    // Written on <today’s date>


• Block comment example
    /* This program demonstrates the use of
    the WriteLine() method to print the
    message Hello, world! */



                                                                                    28
```

## PDF page 26

```text
Adding Program Comments (cont'd.)


/* This program is written to demonstrate using comments */
public static class ClassWithOneExecutingLine
{
    public static void Main()
    {
        // The next line writes the message
        System.Console.WriteLine("Message");
        // This holds the output screen for Windows computers
        System.Console.ReadLine();
    } // End of Main
} // End of ClassWithOneExecutingLine





                                                                                    29
```

## PDF page 27

```text
Using the System Namespace


  • Part of the .NET framework
  • Root namespace for various types
                                                     Box A
public static class ThreeLinesOutput
{
    public static void Main()
    {
        System.Console.WriteLine("Line one");
                                                     Box B
        System.Console.WriteLine("Line two");
        System.Console.ReadLine();
    }
}

                                                     Box C   Console class is used to represent
   the standard input, output, and error
   streams for the console applications                                               30
```

## PDF page 28

```text
Using the System Namespace
                   (cont'd.)


using System; //”Using” clause or using directive
public static class ThreeLinesOutput
                                                     Box A{
    public static void Main()
    {
        Console.WriteLine("Line one");
        Console.WriteLine("Line two");
                                                     Box B        Console.WriteLine("Line three");
        Console.ReadLine();
    }
}

                                                     Box C


                                                                                        31
```

## PDF page 29

```text
Writing and Compiling a C# Program

• Steps for viewing a program output
   – Compile source code into intermediate language (IL)
   – C# just in time (JIT) compiler translates the
     intermediate code into executable statements of
     machine code

• Can be done using either
   – A command line environment like Linux (not for us!)
   – An Integrated Development Environment (IDE) like
     Visual Studio


                                                                                        32
```

## PDF page 30

```text
Compiling Code from within the Visual
              Studio IDE

• Advantages of using the Visual Studio IDE
   – Some of the code you need is already created for you
   – The code is displayed in colour
   – You can double-click an error message, and the cursor
       will move to the line of code that contains the error
   – Many other useful debugging tools are available
         • Will be introduced to these in the lectures and labs.


• How to install Visual Studio



                                                                                     33
```

## PDF page 31

```text
Example (Part of Lab work)
• Problem: Create the following C# program (replace
  xxx with your name) using Microsoft Visual C#



  using System;
  public static class Lab1
  {
      public static void Main()
      {
          Console.WriteLine("Hello COIS1020H, my name is xxx");
          Console.ReadLine();
      }
  }





                                                                                      35
```

## PDF page 32

```text
Summary

• A computer program is a set of instructions that tell
  a computer what to do


• The C# programming language is an object-
  oriented language


• System.Console.WriteLine() method
   – Produces a line of console output





                                                                                    39
```

## PDF page 33

```text
Summary (cont'd.)

• You can define a C# class or variable by using any
  name or identifier


• Comments are non-executing statements that you
  add to document a program
   – Or to disable statements when you test a program


• To create a C# program, you can use the Microsoft
  Visual Studio environment




                                                                                    40
```

## PDF page 34

```text
Syllabus





                                                  41
```

