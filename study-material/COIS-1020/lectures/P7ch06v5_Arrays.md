# P7ch06v5_Arrays.pdf

Source: `source-material/P7ch06v5_Arrays.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H: Programming for
    Computing Systems



             Chapter 6
            Using Arrays
```

## PDF page 2

```text
Declaring an Array


• Array
   – List of data items that all have the same data type and
     the same name
   – Each item is distinguished from the others by an index
• Declaring and creating an array
    double[] sales;
    sales = new double[20];


• new operator
   – Used to create objects



                                                                                       2
```

## PDF page 3

```text
Assigning Values to Array Elements

• Array element
   – Each object in an array

• Subscript (or index)
   – Integer contained within square brackets that
      indicates the position of one of an array’s elements

   – Array’s elements are numbered beginning with 0





                                                                                      3
```

## PDF page 4

```text
Assigning Values to Array Elements





                                    “Off by one” error
                                 Occurs when you forget that
                                      the first element in an array is
                                   element 0





                                                                                     4
```

## PDF page 5

```text
Assigning Values to Array Elements


• Assigning a value to an array element
     sales[0] = 2100.00;
      sales[5] = Convert.ToDouble(Console.ReadLine());
•  Printing an element value
     Console.WriteLine(sales[19]);
•  Using an array element in an equation
     sales[7] = sales[6] + 1;
     sales[i]++;





                                                                                        5
```

## PDF page 6

```text
Initializing an Array

•  In C#, arrays are objects
   – Arrays are instances of a class named
    System.Array


•  Initializing objects (default values)
   – Numeric fields: 0
   – Character fields: ‘\u0000’ or null
   – bool fields: false





                                                                                      6
```

## PDF page 7

```text
Initializing an Array

•  Initializer list
   – The list of values provided for an array


•  Initializer list examples
      int[] myScores = new int[5] {100, 76, 88, 100, 90};
      int[] myScores = new int[] {100, 76, 88, 100, 90};
      int[] myScores = {100, 76, 88, 100, 90};

• C# is smart enough to determine the size of the array
  based on the initializer


                                                                                          7
```

## PDF page 8

```text
Accessing Array Elements

• The power of arrays becomes apparent when you
  use subscripts
      Console.Write(myArray[2]);


   – Can be variables rather than constant values
      Console.Write(myArray[i]);


• Using a loop to perform arithmetic on each element
    for (int i = 0; i < 5; ++i)
      myScores[i] += 3;

                                                                                      8
```

## PDF page 9

```text
Using the Length Property

• Length property
   – Member of the System.Array class
   – Array automatically has access to its length

• Examples


    int[] myScores = {100, 76, 88, 100, 90};

    Console.WriteLine(“Array size is {0}”, myScores.Length);

    for (int i = 0; i < myScores.Length; ++i)

        Console.WriteLine(myScores[i]);


                                                                                            9
```

## PDF page 10

```text
Complete Example

using System;
public static class SimpleArray
{
  public static void Main()
   {
      int[] numbers = new int[5] {4, 6, 8, 10, 12};
        // Display the contents of the array.
    Console.WriteLine("Here are the values in the array.");
     for (int i = 0; i < numbers.Length; ++i)
       Console.Write("{0} ", numbers[i]);
     Console.WriteLine();
        // User input data into the array.
     for (int i = 0; i < numbers.Length; ++i)
      {
       Console.Write("Enter an integer +> ");
      numbers[i] = Convert.ToInt32(Console.ReadLine());
      }
                                                                                    10
```

## PDF page 11

```text
Complete Example

// Display the contents of the array again.
    Console.WriteLine("Here are the new values in the array.");
     for (int i = 0; i < numbers.Length; ++i)
       Console.Write("{0}  ", numbers[i]);
     Console.WriteLine();
    Console.ReadLine();
                               Here are the values in the array.
   }                              4 6 8 10 12
 }                                   Enter an integer => 3
                                   Enter an integer => 5
                                   Enter an integer => 7
                                   Enter an integer => 9
                                  Enter an integer => 11
                               Here are the new values in the array.
                              3 5 7 9 11


                                                                                        11
```

## PDF page 12

```text
Using foreach

• foreach statement
   – Cycles through every array element without using a subscript
   – Uses a temporary iteration variable
         • Automatically holds each array value in turn


• Example


    double[] payRate = {6.00, 7.35, 8.12, 12.45, 22.22};

    foreach(double money in payRate)

           Console.WriteLine(money);





                                                                                        12
```

## PDF page 13

```text
Using foreach

• foreach statement
         • Cannot change the value in the array with foreach





    double[] payRate = {6.00, 7.35, 8.12, 12.45, 22.22};

    foreach(double money in payRate)

        money = 0;


                    Illegal

                                                                                        13
```

## PDF page 14

```text
Using foreach


• To Summarize:
   – Use foreach When you want to access every array
     element


   – Since the iteration variable is read-only
         • You cannot assign a value to it





                                                                                    14
```

## PDF page 15

```text
Searching an Array Using a Loop

• Searching options
   – Using a for loop
   – Using a while loop





                                                                                    15
```

## PDF page 16

```text
Using a for Loop to Search an Array

• Use a for statement to loop through the array
   – Set a Boolean variable to true when match is found


    int [] intList = new int[6] {23, 45, 98, 12, 45, 77};
    int location;
   bool found = false;
    int searchItem = 98;
    for (int i = 0; i < intList.Length; ++i)
            if (searchItem == intList[i])
         {
        found = true;
         location = i;
         }

                                                                                       16
```

## PDF page 17

```text
Using a while Loop to Search an Array

  • Use a while statement to loop through the array
    – Set a Boolean variable to true when match is found


             int [] intList = new int[6] {23, 45, 98, 12, 45, 77};
             int location, i = 0;
          bool found = false;
             int searchItem = 98;
           while ((i < intList.Length) && !found)
              {
                     if (searchItem == intList[i])
                         {
                 found = true;
                    location = i;
                         }
              ++i;
              }

                                                                                          17
```

## PDF page 18

```text
Using a for Loop to Search an Array II

• Can we use a compound condition with a for loop?


    int [] intList = new int[6] {23, 45, 98, 12, 45, 77};
    int location;
    bool found = false;
    int searchItem = 98;
    for (int i = 0; (i < intList.Length && !found); ++i)
        if (searchItem == intList[i])
        {
           found = true;
           location = i;
        }

• YES



                                                                                        18
```

## PDF page 19

```text
Parallel Arrays

•  Parallel arrays: arrays with the same number of elements and
   corresponding data where the same subscript could access additional
   information
        string [] name = {“Rich”, “Mary”, “Phil”, Bob”};
         int [] id = {1234, 4321, 3465, 2346};
       double [] wage = {12.34, 10.76, 20.98, 13.87};

•  name[1], id[1] and wage[1] hold information about Mary
     for(int i = 0; i < name.Length; ++i)
       Console.WriteLine(“{0}’s id is {1} and earns {2:C}”,
                  name[i], id[i], wage[i]);

Rich's id is 1234 and earns $12.34
Mary's id is 4321 and earns $10.76
Phil's id is 3465 and earns $20.98
                                                                                         19
Bob's id is 2346 and earns $13.87
```

## PDF page 20

```text
Passing an Array to a Method

• You can pass a single array element to a method
   – In same manner as you would pass a variable
   – Variables are passed by value
         • Local variables store a local copy of the value so the
          original array element can not be changed

• You can pass an entire array as a parameter
   – Arrays, like all objects but unlike built-in types, are
    passed by reference
   – Method receives actual memory address of the array
         • Thus, the method has access to the actual values in
         the array elements and can change them

                                                                                    24
```

## PDF page 21

```text
Pass A Single Element to a Method


using System;
public static class PassArrayElement
{
  public static void Main()
   {
      int[] someNums = { 10, 12, 22, 35 };
     int x;
    Console.Write("\nAt beginning of Main() method...");
     for (x = 0; x < someNums.Length; ++x)
       Console.Write("{0,6}", someNums[x]);
     Console.WriteLine();
     for (x = 0; x < someNums.Length; ++x)
      MethodGetsOnelnt(someNums[x]);
    Console.Write("At end of Main() method ");
     for (x = 0; x < someNums.Length; ++x)
       Console.Write("{0,6}", someNums[x]);
    Console.ReadLine();
   }

                                                                                      25
```

## PDF page 22

```text
Pass A Single Element to a Method



  public static void MethodGetsOnelnt(int oneVal)
   {
    Console.Write("In MethodGetsOnelnt() {0}", oneVal);
    oneVal = 999;
    Console.WriteLine("   After change {0}", oneVal);
   }
}


                       At beginning of Main() method…  10  12  22  35
                            In MethodGetsOneInt() 10     After change 999
                            In MethodGetsOneInt() 12     After change 999
                            In MethodGetsOneInt() 22     After change 999
                            In MethodGetsOneInt() 35     After change 999
                       At end of Main() method…       10  12  22  35



                                                                                    26
```

## PDF page 23

```text
Pass Entire Array to a Method

using System;
public static class PassEntireArray
{
  public static void Main()
   {
      int[] someNums = { 10, 12, 22, 35 };
     int x;
    Console.Write("\nAt beginning of Main() method...");
     for (x = 0; x < someNums.Length; ++x)
       Console.Write("{0, 6}", someNums[x]);
     Console.WriteLine();
    MethodGetsArray(someNums);
    Console.Write("At end of Main method.......... ");
     for (x = 0; x < someNums.Length; ++x)
       Console.Write("{0, 6}", someNums[x]);
    Console.ReadLine();
   }



                                                                                 27
```

## PDF page 24

```text
Pass Entire Array to a Method

  public static void MethodGetsArray(int[] vals)
   {
     int x;
    Console.Write("In MethodGetsArray()) ");
     for (x = 0; x < vals.Length; ++x)
       Console.Write(" {0}", vals[x]);
     Console.WriteLine();
     for (x = 0; x < vals.Length; ++x)
       vals[x] = 888;
    Console.Write("After change");
     for (x = 0; x < vals.Length; ++x)
       Console.Write(" {0}", vals[x]);
     Console.WriteLine();
   }
                        At beginning of Main() method…  10  12  22  35
}
                            In MethodGetsArray() 10 12 22 35
                            After change 888 888 888 888
                        At end of Main() method…       888  888 888  888


                                                                                 28
```

## PDF page 25

```text
Passing Arrays as Arguments (more)

  • Arrays are objects.
  •  Their references can be passed to methods like
   any other object reference variable.


   ShowArray(numbers);                                      5  10 15 20 25 30 35 40


                 Address


     public static void ShowArray(int[] array)
     {
         for (int i = 0; i < array.Length; i++)
             Console.Write("{0} ",array[i]);
     }

                                                                                     29
```

## PDF page 26

```text
PassArray.cs


// This program demonstrates a more complete example where arrays are
// passed between methods

using System;

 public static class PassArray
 {
  public static void Main()
   {
      int[] numbers = new int[4];
    GetValues(numbers);
    Console.WriteLine("Here are the numbers that you entered:");
    ShowArray(numbers);
    Console.ReadLine();
   }





                                                                                    30
```

## PDF page 27

```text
PassArray.cs (cont’d)

    // The GetValues method accepts a reference to an array as its parameter.
    // The user is asked to enter a value for each element.
    public static void GetValues(int[] arrVals)
    {
        Console.WriteLine("Enter a series of {0} numbers", arrVals.Length);
        for (int i = 0; i < arrVals.Length; i++)
        {
            Console.Write("Enter a number => " );
            arrVals[i] = Convert.ToInt32(Console.ReadLine());
        }
    }

    // The ShowArray method accepts an array as a parameter and displays
    // its contents.
    public static void ShowArray(int[] list)
                                              Output:    {
                                                     Enter a series of 4 numbers        for (int i = 0; i < list.Length; i++)
                                                     Enter a number => 5            Console.Write("{0} ", list[i]);
        Console.WriteLine();                     Enter a number => 9
    }                                               Enter a number => 23
}                                                    Enter a number => 12
                                               Here are the numbers that you entered:
                                                                                          31                                              5 9 23 12
```

## PDF page 28

```text
Returning an Array Reference

• A method can return a reference to an array.
• The return type of the method must be
  declared as an array of the right type.
   public static double[] GetArray()
   {
     double[] array = { 1.2, 2.3, 4.5, 6.7, 8.9 };
     return array;
   }
• The GetArray method is a public static method
  that returns an array of doubles.
```

## PDF page 29

```text
ReturnArray.cs

// This program demonstrates how an array can be returned from a method.
using System;

public static class ReturnArray
{
  public static void Main()                       Output:
   {                                                 1.2
     double[] values;
                                                    2.3    values = GetArray();
                                                    4.5     for (int i = 0; i < values.Length; i++)
      Console.WriteLine("{0} ",values[i]);              6.7
    Console.ReadLine();                             8.9
   }

 // GetArray method
public static double[] GetArray()
   {
     double[] array = {1.2, 2.3, 4.5, 6.7, 8.9};
     return array;
   }
}

                                                                                    33
```

## PDF page 30

```text
Searching and Sorting Arrays





                                                                                34
```

## PDF page 31

```text
Searching Arrays


• A search algorithm is a method of locating a
  specific item in a larger collection of data.
• The sequential search algorithm uses a loop to:
   – sequentially step through an array,
   – compare each element with the search value, and
   – stop when
         • the value is found or
         • the end of the array is reached





                                                                                    35
```

## PDF page 32

```text
SeqSearchDemo.cs

// This program sequentially searches an int array for a specified value.

using System;
public static class SeqSearchDemo
{
  public static void Main()
   {
      int[] numbers = new int [15] { 87, 75, 98, 100, 82, 14, 76, 3, 91, 34,
                                    27, 4, 63, 12, 88 };
     int result, searchValue;
    char input;
    do
      {
            // Get a value to search for.
       Console.Write("Enter a value to search for: ");
      searchValue = Convert.ToInt32(Console.ReadLine());
            // Search for the value
       result = SequentialSearch(numbers, searchValue);


                                                                                    36
```

## PDF page 33

```text
SeqSearchDemo.cs


       // Display the results
       if (result == -1)
       Console.WriteLine("{0} was not found.", searchValue);
     else
       Console.WriteLine("{0} was found at position {1}", searchValue, result);
        // Does the user want to search again?
    Console.WriteLine("Do you want to search again? (Y or N): ");
     input = Convert.ToChar(Console.ReadLine());
   } while (char.ToUpper(input) == 'Y');
  Console.ReadLine();
}





                                                                                       37
```

## PDF page 34

```text
SeqSearchDemo.cs


// The SequentialSearch method searches array for value.
// If value is found in array, the element's subscript is returned.
// Otherwise, -1 is returned.
public static int SequentialSearch(int[] numList, int value)
{
   int i,              // Loop control variable
     pos;        // Index the value is found at
  bool found;       // Flag indicating search results
    i = 0;              // Element 0 is the starting point of the search.
     // Store the default values element and found.
  pos = -1;
  found = false;





                                                                                     38
```

## PDF page 35

```text
SeqSearchDemo.cs

        // Search the array.
    while (!found && i <numList.Length)
      {
           if (numList[i] == value)
         {
                                     Output:        found = true;
                                               Enter a value to search for: 75       pos = i;
                                         75 was found at index 1         }
                                 Do you want to search again? (Y or N):       i++;
                                         y      }
                                               Enter a value to search for: 99     return pos;
                                         99 was not found.   }
                                 Do you want to search again? (Y or N):}
                            Y
                                               Enter a value to search for: 63
                                         63 was found at index 12
                                 Do you want to search again? (Y or N):
                                         n


                                                                                        39
```

## PDF page 36

```text
Binary Search





Image source: https://skilled.dev/course/searching-and-binary-search

                                          Microsoft Visual C# 2010, Fourth                           40
                                                        Edition
```

## PDF page 37

```text
BinarySearch Operation - Success

• Given the following array:

           0   1   2   3   4   5   6   7   8   9

         A:  12  34  37  42  56  63  69  71  82  94


  Assume we are searching for 69 (target)

                                               target ? A[mid]
      bot      top     mid    A[mid]
                                                      (>, <, or =)
       0        9        4       56          >
       5        9        7       71          <
       5        6        5       63          >
       6        6        6       69        = STOP




                                                                                        41
```

## PDF page 38

```text
BinarySearch Operation - Fail

• Using the same array:

           0   1   2   3   4   5   6   7   8   9

        A:  12  34  37  42  56  63  69  71  82  94


  Assume we are searching for 40 (target)

                                               target ? A[mid]
      bot      top     mid    A[mid]
                                                      (>, <, or =)
       0        9        4       56          <
       0        3        1       34          >
       2        3        2       37          >
       3        3        3       42          <
      3       2              STOP as bot > top

                                                                                      42
```

## PDF page 39

```text
BinarySearchDemo.cs


// This program demonstrates the binary search method

using System;
public static class BinarySearchDemo
{
    public static void Main()
    {
        // The values in the following array are sorted in ascending order
        int[] numbers = new int [15] {101, 142, 147, 189, 199, 207, 222,
                                 234, 289, 296, 310, 319, 388, 400, 478};
        int result, searchValue;
        char input;





                                                                                      43
```

## PDF page 40

```text
BinarySearchDemo.cs


    do
    {
        // Get a value to search for.
        Console.Write("Enter a value to search for: ");
        searchValue = Convert.ToInt32(Console.ReadLine());
        // Search for the value
        result = BinarySearch(numbers, searchValue);
        // Display the results.
        if (result == -1)
            Console.WriteLine("{0} was not found.", searchValue);
        else
            Console.WriteLine("{0} was found at position {1}",
                             searchValue, result);
        // Does the user want to search again?
        Console.WriteLine("Do you want to search again? (Y or N): ");
        input = Convert.ToChar(Console.ReadLine());
    } while (char.ToUpper(input) == 'Y');
    Console.ReadLine();
}



                                                                                    44
```

## PDF page 41

```text
BinarySearchDemo.cs (cont’d)


// The BinarySearch method performs a binary search on an
// integer array. The array is searched for the number passed
// to value. If the number is found, its array subscript is
// returned. Otherwise, -1 is returned indicating the value was
// not found in the array.
public static int BinarySearch(int[] numList, int value)
{
    int bot,         // First array element
        top,         // Last array element
        mid,         // Mid point of search
        pos;         // Position of search value
    bool found;      // Flag
    // Set the inital values.
    bot = 0;
    top = numList.Length - 1;
    pos = -1;
    found = false;





                                                                                  45
```

## PDF page 42

```text
BinarySearchDemo.cs (cont’d)

      // Search for the value.
                                            Output:        while (!found && bot <= top)
        {                                              Enter a value to search for: 142
            // Calculate mid point               142 was found at index 1
            mid = (bot + top) / 2;             Do you want to search again? (Y or N):
            // If value is found at midpoint...   y
            if (numList[mid] == value)                                                        Enter a value to search for: 123
            {
                                                123 was not found.                found = true;
                                        Do you want to search again? (Y or N):                pos = mid;
            }                                    y
            // is value in bottom half...          Enter a value to search for: 388
            else if (value < numList[mid])        388 was found at index 12
                top = mid - 1;                Do you want to search again? (Y or N):
            // is value in top half....                                                n
            else
                bot = mid + 1;
        }
        // Return the position of the item, or -1 if it was not found.
        return pos;
    }
}



                                                                                     46
```

## PDF page 43

```text
Using the BinarySearch() Method

• BinarySearch() method
   – Search a target value in a sorted array
   – Member of the System.Array class
   – Returns:
         • The value index, if found
         • A negative value, otherwise.





                                                                                     47
```

## PDF page 44

```text
Using the BinarySearch() Method





                                               Enter an Employee ID 219
                                       ID 219 found at position 3


                                                Enter an Employee ID 220
                                       ID 220 not found





                                                                                      48
```

## PDF page 45

```text
Using the BinarySearch() Method

• Do not use BinarySearch() under these
  circumstances
   – If your array items are not arranged in ascending order
   – If your array holds duplicate values and you want to
      find all of them
   – If you want to find a range match rather than an exact
    match





                                                                                     49
```

## PDF page 46

```text
Sorting Arrays





         Microsoft Visual C# 2010, Fourth                           50
                      Edition
```

## PDF page 47

```text
Selection Sort


• In a selection sort:
   – The smallest value in the array is located and moved to
     element 0.


   – Then the next smallest value is located and moved to
     element 1.


   – This process continues until all of the elements have
     been placed in their proper order.




                                                                                    51
```

## PDF page 48

```text
SelectionSortDemo.cs

// This program demonstrates the SelectionSort method in the ArrayTools class.
using System;
public static class SelectionSortDemo
{
  public static void Main()
   {
      int[] values = {5, 7, 2, 8, 9, 1};
        // Display the unsorted array.
    Console.WriteLine("The unsorted values are:");
     for (int i = 0; i < values.Length; i++)
       Console.Write("{0} ", values[i]);
     Console.WriteLine();
        // Sort the array.
     SelectionSort(values);
        // Display the sorted array.
    Console.WriteLine("The sorted values are:");
     for (int i = 0; i < values.Length; i++)
       Console.Write("{0} ", values[i]);
     Console.WriteLine();
    Console.ReadLine();
  }

                                                                                    52
```

## PDF page 49

```text
SelectionSortDemo.cs (cont’d)

    // The SelectionSort method performs a selection sort on an
    // int array. The array is sorted in ascending order.
    //  **param array The array to sort.
  public static void SelectionSort(int[] array)
   {
      int startScan, index, minIndex, minValue;
     for (startScan = 0; startScan < (array.Length - 1); startScan++)
      {
      minIndex = startScan;
      minValue = array[startScan];
       for(index = startScan + 1; index < array.Length; index++)
         {
               if (array[index] < minValue)
            {
          minValue = array[index];              Output:
          minIndex = index;                                        The unsorted values are:            }
                                         5 7 2 8 9 1         }
       array[minIndex] = array[startScan];         The sorted values are:
       array[startScan] = minValue;              1 2 5 7 8 9
      }
   }
}                                                                                       53
```

## PDF page 50

```text
Using the Sort() Method

• Sort() method
   – Arranges array items in ascending order
   – Use it by passing the array name to Array.Sort()



                                            Mindy
                                           Ned
                                                     Olive
                                                          Patty
                                                    Richard





                                                                                     54
```

## PDF page 51

```text
Using the Reverse() Method

• Reverse() method
   – Reverses the order of items in an array
   – Element that starts in position 0 is relocated to
      position Length – 1
   – Use it by passing the array name to the method


                                                   Marcia
                                          Wendy
                                                Rose
                                                Zach





                                                                                     55
```

## PDF page 52

```text
Multidimensional Array





                            Microsoft Visual C# 2010, Fourth                           56
                                         Edition
```

## PDF page 53

```text
Using Multidimensional Arrays

• One-dimensional or single-dimensional array
   – Picture as a column of values
   – Elements can be accessed using a single subscript


• Multidimensional arrays
   – Require multiple subscripts to access the array elements
   – Two-dimensional arrays
         • Have two or more columns of values for each row
         • Also called rectangular array, matrix, or a table





                                                                                      57
```

## PDF page 54

```text
Using Multidimensional Arrays





• Declaring a Two-Dimensional Array
   – Very similar to a one-dimensional array except that you
    now have to specify the size of each dimension
   – Eg., for the above array

     double[,] sales = new double[3,4];

                                                                                      58
```

## PDF page 55

```text
Example: rent array





• Created using the following


    int[,] rent = new int[4,3] {{400, 450, 510}, {500, 560, 630},
                      {625, 676, 740}, {1000, 1250, 1600}};





                                                                                      59
```

## PDF page 56

```text
Using Multidimensional Arrays

using System;
public static class RentFinder
{
  public static void Main()
   {
      int[,] rents = { {400, 450, 510},
              {500, 560, 630},
              {625, 676, 740},
              {1000, 1250, 1600} };
     int floor;
     int bedrooms;
    Console.Write("Enter the floor on which you want to live ");
     floor = Convert.ToInt32(Console.ReadLine());
    Console.Write("Enter the number of bedrooms you need ");
    bedrooms = Convert.ToInt32(Console.ReadLine());
    Console.WriteLine("The rent is {0}", rents[floor, bedrooms]);
    Console.ReadLine();
                                    Enter the floor on which you want to live 2   }
                                    Enter the number of bedrooms you need 1}
                              The rent is 676

                                                                                     60
```

## PDF page 57

```text
Using Multidimensional Arrays

• Jagged array
   – When the rows of a two-dimensional array are of different
      lengths, the array is known as a jagged array.
   – You can create a jagged array by creating a two-
     dimensional array with a specific number of rows and a
     varying number of columns.
       int[][] ragged = new int[4][];
   – Then create the individual rows.
       ragged[0] = new int[3];
       ragged[1] = new int[4];
       ragged[2] = new int[5];
       ragged[3] = new int[6];


                                                                                        61
```

## PDF page 58

```text
Passing an Array to a Method (more)

• You can pass a multidimensional array to a method
   – By indicating the appropriate number of dimensions after
     the data type in the method header
   – Example
        public static void displaySales(int[,] sales)

• Jagged arrays
   – Insert the appropriate number of square brackets after the
     data type in the method header
   – Example
      public static void displayInfo(int[][] ragged)


                                                                                        62
```

## PDF page 59

```text
Pass2DArray.cs
// This program demonstrates methods that accept 2D array as arguments.


using System;
public static class Pass2Darray
{
    public static void Main()
    {

        int[,] numbers = { { 1,  2,  3,  4  }, { 5,  6,  7,  8  },

                           { 9, 10, 11, 12  } };

        int total = 0;

        // Display the contents of the array.

        Console.WriteLine("Here are the values in the array.");

        ShowArray(numbers);

        // Compute and display the sum of the array's values.

        total = ArraySum(numbers);

        Console.WriteLine("The sum of the values is {0} ", total);

        Console.ReadLine();
                                                                                        63    }
```

## PDF page 60

```text
Pass2DArray.cs



 // The ShowArray method displays the contents
  // of a two-dimensional int array.
public static void ShowArray(int[,]  numList)
  {
      for (int i = 0; i < numList.GetLength(0); i++)
      {
          for (int j = 0; j < numList.GetLength(1); j++)
              Console.Write("{0} ", numList[i, j]);
          Console.WriteLine();
      }
  }





                                                                                    64
```

## PDF page 61

```text
Pass2DArray.cs


  // The ArraySum method returns the sum of the
  // values in a two-dimensional int array.
    public static int ArraySum(int[,] sumList)
    {
        int total = 0;   // Accumulator

        for (int i = 0; i < sumList.GetLength(0); i++)
            for (int j = 0; j < sumList.GetLength(1); j++)
                total += sumList[i, j];

        return total;                                       Output:
    }
                                        Here are the values in the array.
}
                                       1 2 3 4
                                       5 6 7 8
                                       9 10 11 12
                                      The sum of the values is 78

                                                                                       65
```

## PDF page 62

```text
Summary

• An array is a list of data items
   – All of which have the same type and the same name
   – Items are distinguished using a subscript or index
•  In C#, arrays are objects of a class named
  System.Array
• The power of arrays becomes apparent when you
  begin to use subscripts
• Subscript you use remains in the range of 0
  through length -1





                                                                                    66
```

## PDF page 63

```text
Summary (cont'd.)

• foreach statement cycles through every array
  element without using subscripts
• You can compare a variable to a list of values in an
  array
• You can create parallel arrays to more easily
  perform a range match
• The BinarySearch() method finds a requested
  value in a sorted array
• The Sort() method arranges array items in
  ascending order




                                                                                      67
```

## PDF page 64

```text
Summary (cont'd.)

• The Reverse() method reverses the order of
  items in an array
• You can pass an array as a parameter to a method
• Multidimensional arrays require multiple subscripts
  to access the array elements
• Types of multidimensional arrays
   – Two-dimensional arrays (rectangular arrays)
   – Jagged arrays





                                                                                    68
```

