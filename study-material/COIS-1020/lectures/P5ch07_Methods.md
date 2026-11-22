# P5ch07_Methods.pdf

Source: `source-material/P5ch07_Methods.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H: Programming for
    Computing Systems



             Chapter 7
           Using Methods
```

## PDF page 2

```text
Microsoft Visual C# 2010, Fourth                            2
             Edition
```

## PDF page 3

```text
Understanding Methods and
         Implementation Hiding

• Method
   – Encapsulated series of statements that perform a task
   – Using a method is called invoking or calling

           using System;
           public static class HelloClass
            {
             public static void Main()
               {
               Console.WriteLine("Hello");
               Console.ReadLine();
               }
            }

                                                                                        3
```

## PDF page 4

```text
Understanding Implementation Hiding

• Implementation hiding
   – An important principle of object-oriented programming
   – Keeps the details of a method’s operations hidden

• Only concern is the way you interface or interact with
  the method
   – Program does not need to know how method works





                                                                                       4
```

## PDF page 5

```text
Writing Methods with No Parameters
       and No Return Value

• Major reasons to create a method
   – Code will remain short and easy to follow
   – A method is easily reusable

• A method must include:
   – Method declaration (also called a method header)
   – Opening curly brace {
   – Method body
   – Closing curly brace }




                                                                                      5
```

## PDF page 6

```text
Method Example


using System;
public static class HelloClass
{
  public static void Main()
   {
    ShowWelcomeMessage();
    Console.WriteLine("Hello");
    Console.ReadLine();
   }

  public static void ShowWelcomeMessage()
   {
    Console.WriteLine("Welcome");
    Console.WriteLine("It's a pleasure to serve you");
    Console.WriteLine("Enjoy the program");
   }
}


                                                                                6
```

## PDF page 7

```text
Writing Methods with No Parameters
     and No Return Value (cont'd.)

• Method declaration
   – Defines the rules for using the method and contains:
         • Optional declared accessibility
         • Optional static modifier
         • Return type for the method
         • Method name, or identifier
         • Opening parenthesis
         • Optional list of method parameters
         • Closing parenthesis
   Example:
      public static void ShowWelcomeMessage()

                                                                                          7
```

## PDF page 8

```text
Writing Methods with No Parameters
    and No Return Value (cont'd.)

• Optional declared accessibility
   – Limits how other methods can use your method
   – Possible access values
         • public – unlimited access to the method
         • private – limits access to the class that contains method
   – Not going to cover but also
         • Protected internal
         • Protected                                                   public static void ShowWelcomeMessage()
         • Internal                             {                                                   Console.WriteLine("Welcome");
                                                       Console.WriteLine("It's a pleasure to serve you");
                                                   Console.WriteLine("Enjoy the program");
                                                            }

                                                                                      8
```

## PDF page 9

```text
Writing Methods with No Parameters
    and No Return Value (cont'd.)

• You can declare a method to be static or non-static
   – Methods are non-static by default

• static method
   – Can be called without referring to an object
         • Instead, you refer to the class
   – Cannot call non-static methods
         • Non-static methods can call static ones (later)





                                                                                       9
```

## PDF page 10

```text
Writing Methods with No Parameters
     and No Return Value (cont'd.)

• Every method has a return type
   – Indicates what kind of value the method will return to any
     other method that calls it
   – If a method does not return a value, its return type is void
• Method name must be a legal C# identifier

                                                                public static void ShowWelcomeMessage()
                                                                          {
                                                              Console.WriteLine("Welcome");
                              …
                                                                          }• Parameter to a method
   – Variable that holds data passed to a method when it is
      called (interface)


                                                                                          10
```

## PDF page 11

```text
Writing Methods with No Parameters
     and No Return Value (cont'd.)

using System;
public static class HelloClass                                   Welcome
{
                                                           It’s a pleasure to serve you  public static void Main()
                                        Enjoy the program   {
                                           Hello    ShowWelcomeMessage();
    Console.WriteLine("Hello");
    Console.ReadLine();
   }

  public static void ShowWelcomeMessage()
   {
    Console.WriteLine("Welcome");
    Console.WriteLine("It's a pleasure to serve you");
    Console.WriteLine("Enjoy the program");
   }
}

                                                                                          11
```

## PDF page 12

```text
Writing Methods That Use a Parameter

• You need:
   – Type of the parameter
   – A local identifier (name) for the parameter


        public static void DisplaySalesTax(double saleAmount)


   – Example


   public static void DisplaySalesTax(double saleAmount)





                                                                                     12
```

## PDF page 13

```text
Writing Methods That Use a Parameter


                                              Actual parameters
                                            Arguments within a method call or
                                                   invocation

                               public static void Main()
                                   {
                                       int y = 5;
                            DoubleNumber (y);
                                 Console.ReadLine();
                                   }
                               public static void DoubleNumber(int num)
                                   {
                                       int y = 2;
                        num *= y;
                                Console.WriteLine(num);
                                    }

Local variable                              Formal parameter
Declared within a method               A parameter in the method header
                                                            that accepts a value

                                     Microsoft Visual C# 2010, Fourth                           13
                                                   Edition
```

## PDF page 14

```text
Writing Methods That Use Parameters





public static void DisplaySalesTax(double saleAmount)
{
    double tax;
    const double RATE = 0.07;
    tax = saleAmount * RATE;
    Console.WriteLine("The tax on {0:C} is {1:C}", saleAmount, tax);
}





                                                                                    14
```

## PDF page 15

```text
Writing Methods That Use Parameters


using System;
public static class UseTaxMethod               The tax on $12.99 is $0.91
{                                      The tax on $35.67 Is $$2.50
  public static void Main()
   {
    double myPurchase = 12.99;
    DisplaySalesTax(myPurchase);
                                                Actual Parameters
     DisplaySalesTax(35.67);
    Console.ReadLine();
   }
  public static void DisplaySalesTax(double saleAmount)
   {
    double tax;                                               Formal Parameter
     const double RATE = 0.07;
     tax = saleAmount * RATE;
    Console.WriteLine("The tax on {0:C} is {1:C}", saleAmount, tax);
   }
}

                                                                                      15
```

## PDF page 16

```text
Writing Methods That Require Multiple
            Arguments

• Methods can take any number of parameters
• When you call the method, arguments must match
   – In both number and type

  public static void DisplaySalesTax(double saleAmount, double taxRate)
  {
       double tax;
       tax = saleAmount * taxRate;
       Console.WriteLine("The tax on {0:C} at {1:P} is {2:C}",
                         saleAmount, taxRate, tax);
   }

   – To invoke it in Main() use
              DisplaySalesTax(200, 0.10);


                                                                                    16
```

## PDF page 17

```text
Writing Methods That Return a
              Value

• A method can return, at most, one value through its
  name to a method that calls it
   – The data type of the return value is the same as the
     data type of the Method

• return statement
   – Causes a value to be sent back to the calling
    method

• You are not required to use a returned value
   –  it can be stored in a variable or used directly

                                                                                     17
```

## PDF page 18

```text
Writing a Method That Return a
           Value (cont'd.)


    public static double CalcPay(double hours, double rate)
    {
           double gross;
           gross = hours * rate;
           return gross;
     }

• The data type of the return value gross  is double
  which matches the return type of the method
  CalcPay
•  In Main()
   Result = CalcPay(35, 12.50);  // or
   Console.WriteLine(“The gross pay is {0:C},
                CalcPay(35, 12.50));

                                                                                    18
```

## PDF page 19

```text
Writing a Method That Return a
          Value (cont'd.)
using System;
public static class UseCalcPay
{                                                I worked 37.5 hours at 12.75 per hour
  public static void Main()
                       My gross pay is $478.13   {
    double myHours = 37.5;
    double myRate = 12.75;
    double grossPay;
    grossPay = CalcPay(myHours, myRate);
    Console.WriteLine("I worked {0} hours at {1} per hour", myHours, myRate);
    Console.WriteLine("My gross pay is {0:C}", grossPay);
    Console.ReadLine();
   }
  public static double CalcPay(double hours, double rate)
   {
    double gross;
     gross = hours * rate;
    return gross;
   }
}

                                                                                    19
```

## PDF page 20

```text
Nested Method Calls

    • A nested method call is when a method calls
     another method
     – Method calls placed inside other method calls


// This program demonstrates nested method calls                                                                                         // Deep displays message and calls Deeper
using System;                                                       public static void Deep()
public static class DeepAndDeeper                                                               {
{                                                      Console.WriteLine("I am now in Deep.");
  public static void Main()                                                         Deeper();
  {                                                   Console.WriteLine("Now I am back in Deep.");
   Console.WriteLine("I am starting in Main.");                                                               }
   Deep();
   Console.WriteLine("NowI am back in Main.");                                                                                        // The Deeper method displays a message
}                                                       public static void Deeper()
                                                              {
     I am starting in Main                                                      Console.WriteLine("I am now in Deeper.");
      I am now in Deep                                                               }
      I am in Deeper                                     }
   Now I am back in Deep
   Now I am back in Main                                                             20
```

## PDF page 21

```text
Summary

• Method is a series of statements that perform a task
• Some methods require passed-in information called
  arguments or parameters
• You write methods to make programs easier to
  understand and so that you can easily reuse them
•  Object-oriented programs hide their methods’
  implementation
• You can pass multiple arguments to a method





                                                                                      22
```

## PDF page 22

```text
Summary (cont'd.)

• The return type for a method can be any type used
   in the C# programming language
• You might see different Main() method headers in
  other books or in programs written by others





                                                                                    23
```

