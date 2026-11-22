# P2ch02v2_Variables.pdf

Source: `source-material/P2ch02v2_Variables.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H: Programming for
    Computing Systems



             Chapter 2
            Using Data
```

## PDF page 2

```text
Learning Objectives

• Declare Variables
• Display Variable values
• Use integral and floating-point data types.
• Use arithmetic operations
• Use other data types (bool, char, string)
• Define named constant
• Accept console input





                                   Microsoft Visual C# 2008, Third                             2
                                                 Edition
```

## PDF page 3

```text
Declaring Variables

• Constant
   – Cannot be changed after a program is compiled
   – Can be called Literal constants
   – Its value is taken literally at each use
• Variable
   – A named location in computer memory that can hold
      different values at different points in time
• Data type
   – Describes the format and size of (amount of memory
     occupied by) a data item
   – And what type of operations can be performed

                                                                               3
```

## PDF page 4

```text
4
```

## PDF page 5

```text
Declaring Variables (cont'd.)

• Variable declaration
   – Statement that names a variable and reserves
     storage
   – Example:

                int myAge = 25;

• You can declare multiple variables of the same type
   – In separate statements on different lines
   – in a single statement
         • By using the type once and separating the variable
         declarations with a comma


                                                                               5
```

## PDF page 6

```text
Displaying Variable Values


using System;
public static class DisplaySomeMoney
{
    public static void Main()
    {
        double someMoney = 39.45;
        Console.WriteLine(someMoney);
        Console.ReadLine();
    }
}

                                     39.45


                                                                    6
```

## PDF page 7

```text
Displaying Variable Values (cont'd.)

  using System;
  public static class DisplaySomeMoney2
  {
    public static void Main()
     {
      double someMoney = 39.45;
      Console.Write(“The money is $”);
      Console.WriteLine(someMoney);
      Console.ReadLine();
     }
  }

             The money is $39.45


                                                                           7
```

## PDF page 8

```text
Displaying Variable Values (cont'd.)


• Format string
   – A string of characters that optionally contains fixed text
   – Contains one or more format items or placeholders for
      variable values
• Placeholder
   – Consists of a pair of curly braces containing a number
      that indicates the desired variable’s position
         • In a list that follows the string





                                                                                 8
```

## PDF page 9

```text
Displaying Variable Values (cont'd.)

using System;
public static class DisplaySomeMoney3
{
  public static void Main()
   {
    double someMoney = 39.45;
    Console.WriteLine("The money is ${0} exactly", someMoney);
    Console.ReadLine();
   }
}


           The money is $39.45 exactly

                                                                               9
```

## PDF page 10

```text
Displaying Variable Values (cont'd.)

• Formatting output
     int num1 = 4, num2 = 56, num3 = 789;
     Console.WriteLine(“{0, 5}”, num1);
     Console.WriteLine(“{0, 5}”, num2);
     Console.WriteLine(“{0, 5}”, num3);


                  4
                 56
                789





                                                                              10
```

## PDF page 11

```text
Using the Integral Data Types

•  Integral data types
   – Types that store whole numbers
   – byte, sbyte, short, ushort, int, uint, long,
    ulong, and char
• Variables of type int
   – Store (or hold) integers, or whole numbers
• Shorter integer types
   – byte, sbyte (which stands for signed byte), short
      (short int), or ushort (unsigned short int)




                                                                                    11
```

## PDF page 12

```text
Using Floating-Point Data Types

• Floating-point number
   – Contains decimal positions
•  Floating-point data types
   – float
         • Can hold up to seven significant digits of accuracy
   – double (default)
         • Can hold 15 or 16 significant digits of accuracy
   – decimal
         • Has a greater precision and a smaller range
         • Suitable for financial and monetary calculations


                                                                              12
```

## PDF page 13

```text
Using Floating-Point Data Types
                 (cont'd.)

• Double  is the default floating point
•  Suffixes
   – Put an F after a number to make it a float
     float val = 54.7;  // incorrect
     float val = 54.7F; // correct
   – Put a D after it to make it a double
   – Put an M after it to make it a decimal
     decimal wage = 12.55;  // incorrect
     decimal wage = 12.55M; // correct




                                                                              13
```

## PDF page 14

```text
Using Floating-Point Data Types
                 (cont'd.)

•  Scientific notation
   – Includes an E (for exponent)


   -123.78 is the same as -1.2378E2
   0.000382 is the same as 3.82E-4





                                                                              14
```

## PDF page 15

```text
Formatting Floating-Point Values

• C# displays floating-point numbers in the most
  concise way it can
   – While maintaining the correct value
• Standard numeric format strings
   – Strings of characters expressed within double
     quotation marks that indicate a format for output
   – Take the form X0
         • X is the format specifier; 0 is the precision specifier
• Format specifiers
   – Define the most commonly used numeric format types
   – Can be one of nine built-in format characters

                                                                              15
```

## PDF page 16

```text
Formatting Floating-Point Values
              (cont'd.)





                                                                       16
```

## PDF page 17

```text
Formatting Floating-Point Values

                                                                1. The number is 34.456
                                                                2. The number is 34.46using System;
                                                                3. The number is  34.5public static class FormatExample
                                                                4. The number is 34.456
{
                                                                5. The number is 3.445600E+001
  public static void Main()                                                                6. The number is $34.46
   {                                                                7. The number is $23,456.780
    double val = 34.456;
    Console.WriteLine(“1. The number is {0}", val);
    Console.WriteLine(“2. The number is {0:F}", val); //Fixed point
    Console.WriteLine(“3. The number is {0:F1}", val); //Fixed-point
    Console.WriteLine(“4. The number is {0:F3}", val); //Fixed point 3 zeros
    Console.WriteLine(“5. The number is {0:E}", val); //Scientific (E)
    Console.WriteLine(“6. The number is {0:C}", val); //Currency
     val = 23456.78;
    Console.WriteLine(“7. The number is {0:C3}", val);
    Console.ReadLine();
   }
}
                                                                                 17
```

## PDF page 18

```text
Using the Standard Binary Arithmetic
             Operators

• Binary operators
   – Use two values (operands)
         int x = 8, y = 9, z;
       z = x + y;  // z would store 17

• Unary operators
   – Uses one operand
         int x = 8, z;
       z = -x;  // z would store -8





                                                                              19
```

## PDF page 19

```text
Using the Standard Binary Arithmetic
        Operators (cont'd.)





                                                                            20
```

## PDF page 20

```text
Using the Standard Binary Arithmetic
              Operators

• Operator precedence
   – Rules that determine the order in which parts of a
     mathematical expression are evaluated


   – (*, /, %) have higher priority compared to (+, -)


   – You can override normal operator precedence with
     parentheses





                                                                                21
```

## PDF page 21

```text
Using Shortcut Arithmetic Operators

• Add and assign operator
   – Example: total = total + val;

              total += val;
   – Variations: –=, *=, and /=
• Prefix increment operator
   – Example: someValue = someValue + 1;
           ++someValue;
• Postfix increment operator
   – Example: someValue = someValue + 1;
           someValue++;
• Decrement operator (--)


                                                                              22
```

## PDF page 22

```text
Microsoft Visual C# 2008, Third                           23
            Edition
```

## PDF page 23

```text
Understanding Numeric Type Conversion

•  Arithmetic with variables or constants of the same type
   – Result retains the same type
•  Arithmetic with operands of dissimilar types
   – C# chooses a unifying type for the result
   – Implicitly (or automatically) converts nonconforming
     operand(s) to the unifying type
          • Type with the higher type precedence
         – Can automatically convert Integral data types up the
             hierarchy to larger Integral and Floating Point types
              » Eg. int will convert to long, float, double or decimal.
         – For floating point data types, only float will
             automatically convert to double


                                                                                24
```

## PDF page 24

```text
25
```

## PDF page 25

```text
Understanding Numeric Type
        Conversion (cont'd.)


•  Implicit cast
   – Automatic transformation that occurs when a value
       is assigned to a type with higher precedence
•  Explicit cast
   – Placing the desired result type in parentheses
         • Followed by the variable or constant to be cast
            double result = 7 / 4;              // result = 1.0
            double result = 7 / (double) 4;   // result = 1.75




                                                                              26
```

## PDF page 26

```text
Using the bool Data Type


• Boolean variable
   – Can hold only one of two values—true or false
   – Declare a Boolean variable with type bool
     bool done = true;
• Comparison operator
   – Compares two items
   – An expression containing a comparison operator has
    a Boolean value





                                                                              27
```

## PDF page 27

```text
Using the bool Data Type (cont'd.)





                                                                          28
```

## PDF page 28

```text
Using the char Data Type

• char data type
   – Holds any single character
• Place constant character values within single
  quotation marks
           char letter = ‘r’;





                                                                              29
```

## PDF page 29

```text
Using the char Data Type (cont'd.)


• Escape sequence
   – Stores a pair of
      characters


   – Begins with a backslash


   – A pair of symbols
      represents a single
      character





                                                                                 30
```

## PDF page 30

```text
Using the string Data Type

• string data type
   – Holds a series of characters
      string name = “Richard”;

• Values are expressed within double quotation marks


• Comparing strings
   – Use == and !=
   – Methods Equals(), Compare(), CompareTo()



                                                                              31
```

## PDF page 31

```text
Using the string Data Type (cont'd.)





         Compare Amy to Amy: True
         Compare Amy to Matthew: False

                                                                             32
```

## PDF page 32

```text
String Comparison methods

• Equals()
   – Determines whether two String objects have the
    same value

         String.Equals(Str1, Str2)


   – And returns a Boolean





                                   Microsoft Visual C# 2008, Third                           33
                                                 Edition
```

## PDF page 33

```text
String Comparison methods


• Compare()
   – Compares two specified objects and returns an integer


• CompareTo()
   – Compares this instance with a specified object or String and
       returns an integer

Compare() and CompareTo() returns:
       • Negative value →   if the first substring precedes the second substring in the sort order.
       • Zero →                     if the substrings are in the same position, or the length is zero.
       • Positive Value→     if the first substring follows the second substring in the sort order.



                                   Microsoft Visual C# 2008, Third                           34
                                                 Edition
```

## PDF page 34

```text
String Comparison methods

Example


       String S1 = "Alaa";
       String S2 = "John";
       Console.WriteLine(S1.CompareTo(S2));
       Console.WriteLine(String.Compare(S1, S2));


                      -1
                      -1





                                   Microsoft Visual C# 2008, Third                           35
                                                 Edition
```

## PDF page 35

```text
Using the string Data Type (cont'd.)

• Use the length property of a string to determine its
  length
               Str.Length
   – E.g.,
         • The length of “water” is 5





                                                                                    36
```

## PDF page 36

```text
Using the string Data Type (cont’d.)


• Use the Substring() method to extract a portion of a
   string from a starting point for a specific length





                                                                                    37
```

## PDF page 37

```text
Accepting Console Input

•  Interactive program
   – A program that allows user input
• Console.ReadLine() method
   – Accepts user input from the keyboard
   – Accepts all of the characters entered by a user until
     the user presses Enter
   – Characters can be assigned to a string
         • i.e. all input is by default read as a string!!
   – Must use a conversion method to convert the input
      string to the proper type



                                                                              38
```

## PDF page 38

```text
Accepting Console Input
using System;
public static class InteractiveSalesTax
{
  public static void Main()
   {
     string name;
    Console.Write("Enter your name : ");
   name = Console.ReadLine();
    Console.WriteLine(“Your name is {0}, name);
    Console.ReadLine();
   }
}





                                                                               39
```

## PDF page 39

```text
Accepting Console Input (cont'd.)

using System;
public static class InteractiveSalesTax
{
  public static void Main()
   {
    const double TAX_RATE = 0.06;
     string itemPriceAsString;
    double itemPrice;
    double total;
    Console.Write("Enter the price of an item >> ");
    itemPriceAsString = Console.ReadLine();
    itemPrice = Convert.ToDouble(itemPriceAsString);
     total = itemPrice * TAX_RATE;
    Console.WriteLine("With a tax rate of {0}, a {1:C} item costs {2:C} more."
                  TAX_RATE, itemPrice, total);
    Console.ReadLine();
   }
}           Enter the price of an item >> 28.77
         With a tax rate of 0.06, a $28.77 item costs $1.73 more.

                                                                               40
```

## PDF page 40

```text
Accepting Console Input (more)

using System;
public static class InteractiveSalesTaxV2
{
  public static void Main()
   {
    const double TAX_RATE = 0.06;
    double itemPrice;
    double total;
    Console.Write("Enter the price of an item >> ");
       // Notice how the Console.ReadLine() is embedded in the Convert method
    itemPrice = Convert.ToDouble(Console.ReadLine());
     total = itemPrice * TAX_RATE;
    Console.WriteLine("With a tax rate of {0}, a {1:C} item costs {2:C} more."
                  TAX_RATE, itemPrice, total);
    Console.ReadLine();
   }
}
           Enter the price of an item >> 28.77
         With a tax rate of 0.06, a $28.77 item costs $1.73 more.

                                                                               41
```

## PDF page 41

```text
Accepting Console Input (cont'd.)





                                                                        42
```

## PDF page 42

```text
Defining Named Constants

• Named constant
   – Often simply called a constant
   – An identifier whose contents cannot change
   – Created using the keyword const
     const int INCHES_IN_A_FOOT = 12;


• Programmers usually name constants using all
  uppercase letters
   – Inserting underscores for readability





                                                                              43
```

## PDF page 43

```text
Self-documenting

• Self-documenting statement
   – Easy to understand even without program comments


   lengthInches = lengthFeet * INCHES_IN_A_FOOT;





                                                                              44
```

## PDF page 44

```text
Summary

• Constant: cannot be changed after compilation
• Can display variable values with Write() or
  WriteLine()
• Nine integral data types: byte, sbyte, short,
  ushort, int, uint, long, ulong, and char
• Three floating-point data types: float, double,
  and decimal
• Use the binary arithmetic operators +, –, *, /, and
  % to manipulate values in your programs
• Shortcut arithmetic operators



                                                                              45
```

## PDF page 45

```text
Summary (cont'd.)


• A bool variable can be true or false
•  Implicit cast versus explicit cast
• char data type holds any single character
• string data type holds a series of characters
• Named constants are program identifiers whose
  values cannot change.
• Console.ReadLine() method accepts user input





                                                                              46
```

## PDF page 46

```text
Knowledge Check

1. True or False: A data item is constant when it can
  be changed after a program is compiled.
2. What is the purpose of a placeholder?
3. A(n) _____ data type is a type that stores whole
   numbers.
4. True or False: A floating-point number is one that
   contains decimal positions.





                                   Microsoft Visual C# 2008, Third                           47
                                                 Edition
```

## PDF page 47

```text
Activity 1.2: Discussion Questions

• Should variables that contain numbers always be
  declared as integer or floating-point data types?
   – Why or why not?
   – Name potential examples.
• What is the difference between an implicit cast and an
   explicit cast?





                                       Microsoft Visual C# 2008, Third                           50
                                                     Edition
```

## PDF page 48

```text
Self-Assessment
• Why is using the right data types important in coding?


• Do you think the programming concepts covered thus
   far are easy to learn for beginner developers?


• What concepts may be more challenging?





                                        Microsoft Visual C# 2008, Third                           51
                                                     Edition
```

