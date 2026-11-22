# P6ch08v5_Methods Advanced Concepts.pdf

Source: `source-material/P6ch08v5_Methods Advanced Concepts.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H: Programming for
    Computing Systems



             Chapter 8
     Advanced Method Concepts
```

## PDF page 2

```text
Microsoft Visual C# 2010, Fourth                            2
             Edition
```

## PDF page 3

```text
Understanding Parameter Types

• Mandatory parameter
   – Argument for it is required in every method call
• Four types of mandatory parameters
   – Value parameters
         • Declared without any modifiers
   – Reference parameters
         • Declared with the ref modifier
   – Output parameters
         • Declared with the out modifier
   – Parameter arrays (not important for this course)
         • Declared with the params modifier


                                                                                      3
```

## PDF page 4

```text
Using Mandatory Value Parameters

• Value parameter
   – Method receives a copy of the value passed to it
   – Copy is stored at a different memory address than
     actual parameter
• Changes to value parameters never affect the
   original argument in the calling method





                                                                                      4
```

## PDF page 5

```text
Using Value Parameters

                                 Output:
using System;                                       In Main quantity is 4
public static class ValueParameter                                       In DisplayValueParameter(), number is 888
{
                                       In Main quantity is 4  public static void Main()
   {
     int quantity = 4;
    Console.WriteLine("In Main quantity is {0}", quantity);
    DisplayValueParameter(quantity);
    Console.WriteLine("In Main quantity is {0}", quantity);
    Console.ReadLine();
   }
  public static void DisplayValueParameter(int number)
   {
    number = 888;
    Console.WriteLine("In DisplayValueParameter(), number is {0}", number);
   }
}




                                                                                          5
```

## PDF page 6

```text
Using Reference and Output
           Parameters

• Reference and output parameters
   – Have memory addresses that are passed to a
     method, allowing it to alter the original variables
• Differences
   – Reference parameters need to contain a value
     before calling the method
   – Output parameters do not need to contain a value
• Reference and output parameters act as aliases
   – For the same memory location occupied by the
      original passed variable



                                                                                        6
```

## PDF page 7

```text
Using Reference Parameters

                                   Output:
using System;
                                         In Main quantity is 4public static class ReferenceParameter
                                         In DisplayReferenceParameter(), number is 888{
  public static void Main()                 In Main quantity is 888
   {
     int quantity = 4;
    Console.WriteLine("In Main quantity is {0}", quantity);
    DisplayReferenceParameter(ref quantity); // notice use of ref
    Console.WriteLine("In Main quantity is {0}", quantity);
    Console.ReadLine();
   }
  public static void DisplayReferenceParameter(ref int number)
    // notice use of ref
   {
    number = 888;
    Console.WriteLine("In DisplayReferenceParameter(), number is {0}", number);
   }
}



                                                                                          7
```

## PDF page 8

```text
Using Output Parameters

                                          Output:
using System;
                                                Enter first integer 87public static class InputMethodDemo
                                                Enter second integer 25{
                                                 After InputMethod first is 87  public static void Main()
   {                                        and second is 25
     int first, second;
    InputMethod(out first, out second); // notice use of out
    Console.WriteLine("After InputMethod first is {0}", first);
    Console.WriteLine("and second is {0}", second);
    Console.ReadLine();
   }
  public static void InputMethod(out int one, out int two)
    // notice use of out
   {
    Console.Write("Enter first integer => ");
    one = Convert.ToInt32(Console.ReadLine());
    Console.Write("Enter second integer => ");
    two = Convert.ToInt32(Console.ReadLine());
   }
}

                                                                                          8
```

## PDF page 9

```text
Using Reference and Output
           Parameters

• Advantage of using reference and output
  parameters
   – Method can change multiple variables


• Disadvantage to using reference and output
  parameters
   – Allow multiple methods to have access to the same
     data, weakening the “black box” paradigm





                                                                                      9
```

## PDF page 10

```text
Introduction to Recursion


• We have been calling other methods from a method.


•  It’s also possible for a method to call itself.


• A method that calls itself is a recursive method.


   – Each time it calls itself, the cycle is repeated endlessly.
   – Like a loop, a recursive method must have some way to
      control the number of times it repeats.





                                                                                    10
```

## PDF page 11

```text
RecursionDemo.cs


    // Message is a recursive method, which displays a message n times.
  public static void Message(int n)
   {
       if (n > 0)
     {
      Console.WriteLine("This is a recursive method.");
      Message(n - 1);
     }
                      Output:
   }
                              This is a recursive method}
                              This is a recursive method
                              This is a recursive method
                              This is a recursive method
                              This is a recursive method

                                                                                      12
```

## PDF page 12

```text
More on Recursion


The method is first called
                                          First call of the methodfrom the Main method of
                               n = 5the RecursionDemo
class.                                   Second call of the method
                                  n = 4
The second through the
                                          Third call of the method
sixth calls are recursive.
                                     n = 3

                                              Fourth call of the method
                                         n = 2

                                                         Fifth call of the method
                                            n = 1

                                                        Sixth call of the method
                                               n = 0




                                                                                    13
```

## PDF page 13

```text
Solving Problems With Recursion


•  Recursion can be a powerful tool for solving repetitive
  problems.


•  Recursion is never absolutely required to solve a
  problem.
   – Any recursive problem can also be solved iteratively,
      with a loop.


•  In many cases,
   – recursive algorithms are less efficient than iterative
      algorithms.


                                                                                    14
```

## PDF page 14

```text
Solving Problems With Recursion

•  Recursion works like this:
   – A base case is established.
       • If matched, the method solves it and returns.
   –  If the base case cannot be solved now:
       • the method reduces it to a smaller problem (recursive
          case)
       • and calls itself to solve the smaller problem.
   – By reducing the problem with each recursive call, the
     base case will eventually be reached, and the recursion
        will stop.





                                                                                      15
```

## PDF page 15

```text
Solving Problems With Recursion
Example: Factorial
– In mathematics, the notation n! is the factorial of the number n.
                    n! = n x (n-1) x (n-2) x … x 2 x 1





                                                                                     16
```

## PDF page 16

```text
Solving Problems With Recursion





                                                                                 17
```

## PDF page 17

```text
Solving Problems With Recursion





                                                                                 18
```

## PDF page 18

```text
FactorialDemo.cs


using System;
public class FactorialDemo
{
  public static static void Main()
   {
    int number;
    long result
    Console.Write("Enter a nonnegative integer: ");
   number = Convert.ToInt32(Console.ReadLine());
    result = Factorial(number);
    Console.WriteLine("{0}! is {1}", number, result);
      // Or Console.WriteLine("{0}! is {1}", number, Factorial(number));
    Console.ReadLine();
   }



                                                                                    19
```

## PDF page 19

```text
FactorialDemo.cs


    // The factorial method uses recursion to calculate
    // the factorial of its argument, which is assumed to be a nonnegative number.
    // **param n The number to use in the calculation.
    //  **return The factorial of n.
  public static long Factorial(int n)
   {
      if (n <= 1)
     return 1;                              // base case
    else
     return n * Factorial(n - 1);    //recursive case
   }
}                              Output:
                                          Enter a nonnegative integer: 4
                                           4! is 24



                                                                                         20
```

## PDF page 20

```text
Solving Problems With Recursion


The method is first called
                                        First call of the methodfrom the Main method of
the FactorialDemo            n = 4
class.                           Return value: 24
                                Second call of the method
                               n = 3
                                   Return value: 6
                                     Third call of the method
                                 n = 2
                                     Return value: 2
                                        Fourth call of the method
                                   n = 1
                                       Return value: 1
                                                Fifth call of the method
                                     n = 0
                                         Return value: 1
                                                                                   21
```

## PDF page 21

```text
Iterative Version of Factorial



// The factorial method uses repitition (looping) to calculate
// the factorial of its argument, which is assumed to be a nonnegative number.
// **param n The number to use in the calculation.
//  **return The factorial of n.
public static long Factorial(int n)
{
   long result = 1;
    for(int i = 1; i <= n; ++ i)
       result = result * i;
   return result;
}





                                                                                      22
```

## PDF page 22

```text
Microsoft Visual C# 2010, Fourth                           23
             Edition
```

## PDF page 23

```text
Overloading Methods

• Overloading
   – Involves using one term to indicate diverse
     meanings


• When you overload a C# method:
   – You write multiple methods with a shared name
   – Compiler understands your meaning based on the
     arguments you use with the method





                                                                                      24
```

## PDF page 24

```text
Overloading Methods

• Methods are overloaded correctly when:
   – They have the same identifier,
   – Different parameter lists  public static void m1(int x)
                                      {…   }

                                      public static void m1(double x)
                                      {    … }

• Methods with same identifier that have identical
  parameter lists but different return types
   – Are not overloaded         public static void m1( int x )
                                       {…   }

                                       public static double m1( int x )
                                       {    … }

                                                                                      25
```

## PDF page 25

```text
Overloading Methods

using System;
public static class BorderDemo1                           Output:
{                                              ******
  public static void Main()
                                               * Ed *   {
    DisplayWithBorder("Ed");                           ******
    DisplayWithBorder("Theodore");
    DisplayWithBorder("Jennifer Ann");
    Console.ReadLine();                               ************
   }                                             * Theodore *
  public static void DisplayWithBorder(string word)
                                               ************   {
     const int EXTRA_STARS = 4;
     const string SYMBOL = "*";                          ****************
     int size = word.Length + EXTRA_STARS;
     int x;                                         *  Jennifer Ann  *
     for (x = 0; x < size; ++x)                             ****************
      Console.Write(SYMBOL);
    Console.WriteLine();
    Console.WriteLine(SYMBOL + " " + word + " " + SYMBOL);
     for (x = 0; x < size; ++x)
      Console.Write(SYMBOL);
    Console.WriteLine("\n\n");
   }
}

                                                                                  26
```

## PDF page 26

```text
Overloading Methods

                                                               Output: public static void DisplayWithBorder(int number)
                                                             ******   {
                                                              * Ed *    const int EXTRA_STARS = 4;        Different DataType
                                                             ******    const string SYMBOL = "*";
     int size = EXTRA_STARS + 1; Same Method Name
     int leftOver = number;                                       *****
     int x;                                                      * 3 *
    while (leftOver >= 10) //Check how many digits in “number”         *****
     {
       leftOver = leftOver / 10;                                     *******
       ++size;                                                              * 456 *
     }                                                             *******
     for (x = 0; x < size; ++x)
      Console.Write(SYMBOL);                                                             **********
    Console.WriteLine();
                                                              * 897654 *
    Console.WriteLine(SYMBOL + " " + number + " " + SYMBOL);
                                                             **********     for (x = 0; x < size; ++x)
      Console.Write(SYMBOL);
                                                             ************    Console.WriteLine("\n\n");
                                                              *  Veronica  *   }
                                                             ************}

                                                                                         27
```

## PDF page 27

```text
Understanding Overload Resolution
public static void main()
{
    short y = 5;                        Which version of m1
    m1(y);                                                   will be called??
}


public static void m1(int x)
{
    console.WriteLine("{0} is printed from M1 that use int", x);
}


public static void m1(long x)
{
    console.WriteLine("{0} is printed from M1 that use long", x);
}


public static void m1(float x)
{
    console.WriteLine("{0} is printed from M1 that use float", x);
                                   Microsoft Visual C# 2010, Fourth                           30}
                                                 Edition
```

## PDF page 28

```text
Understanding Overload Resolution


• Overload resolution
   – Used by C# to determine which method to execute
    when a method call could execute multiple
     overloaded method
• Applicable methods
   – Set of methods that can accept a call with a specific
        list of arguments
• Betterness rules
   – Rules that determine which method version to call
   – Similar to the implicit data type conversion rules


                                                                                    31
```

## PDF page 29

```text
Understanding Overload Resolution





                                                                                    32
```

## PDF page 30

```text
Avoiding Ambiguous Methods


• Ambiguous method
   – Compiler cannot determine which method to use
   – Occurs when you overload methods





                                                                                    33
```

## PDF page 31

```text
Avoiding Ambiguous Methods





                                                                             34
```

## PDF page 32

```text
Using Optional Parameters


• Optional parameter
   – One for which a default value is automatically
     supplied
• Make a parameter optional by providing a value for
    it in the method declaration
   – Only value parameters can be given default values
• Any optional parameters in a parameter list must
  follow all mandatory parameters
   – i.e., must appear to the right of the parameter list




                                                                                    35
```

## PDF page 33

```text
Using Optional Parameters

using System;
                                    Output:public static class OptionalParameterDemo
                                     Using 2 arguments: Size is 24{
  public static void Main()                 Using 3 arguments: Size is 192
   {
    Console.Write("Using 2 arguments: ");
     DisplaySize(4, 6);
    Console.Write("Using 3 arguments: ");
     DisplaySize(4, 6, 8);
    Console.ReadLine();
   }

  public static void DisplaySize(int length, int width, int height = 1)
   {
   int area = length * width * height;
  Console.WriteLine("Size is {0}", area);
   }
}


                                                                                   36
```

## PDF page 34

```text
Using Optional Parameters





                                                                         37
```

## PDF page 35

```text
Advantages to Using Optional
        Parameters





                                                                             38
```

## PDF page 36

```text
Overload Resolution with
          Optional Arguments

•  Optional arguments affect overload resolution
   – Rules for betterness on argument conversions are
      applied only for arguments that are given explicitly
   public static void AMethod(int a, double b = 2.2)
   public static void AMethod(int a, char b = ‘H’)
   AMethod(12); // causes a problem
•   If two signatures are equally good
   – Signature that does not omit optional parameters is
     considered better
   public static void BMethod(int a)
   public static void BMethod(int a, char b = ‘H’)
   BMethod(12); // call the first version



                                                                                    39
```

## PDF page 37

```text
Summary

• Method parameters can be mandatory or optional
• Types of formal parameters
   – Value parameters
   – Reference parameters
   – Output parameters
• When you overload a C# method, you write
  multiple methods with a shared name
   – But different argument lists





                                                                                    40
```

## PDF page 38

```text
Summary (cont'd.)

• When you overload a method, you run the risk of
  creating an ambiguous situation
• An optional parameter to a method is one for which
  a default value is automatically supplied
   – If you do not explicitly send one as an argument





                                                                                    41
```

