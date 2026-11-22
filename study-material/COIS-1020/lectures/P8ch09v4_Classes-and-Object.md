# P8ch09v4_Classes and Object.pdf

Source: `source-material/P8ch09v4_Classes and Object.pdf`

Machine-extracted text; verify figures, tables and code against the original PDF.

## PDF page 1

```text
COIS1020H: Programming for
    Computing Systems



             Chapter 9
     Using Classes and Objects
```

## PDF page 2

```text
Understanding Class Concepts


• Classes are the basic building blocks of Object-
  Oriented programming
• Two Types of classes
   – Classes that are only application programs with a
    Main() method (usually declared as static)
   – Classes from which you instantiate objects
         • Can contain a Main() method, but it is not typical
• An object is an instantiation of a class





                                                                                 2
```

## PDF page 3

```text
Understanding Class Concepts
                  (cont'd.)

• Instance variables (also called fields)
   – Data components of a class
• State
   – Set of contents of an object’s instance variables
• Instance methods
   – Methods associated with objects
   – Every instance of the class has the same methods
• Class client or class user
   – Program or class that instantiates objects of another
      prewritten class (such as Console)


                                                                               3
```

## PDF page 4

```text
Creating a Class from Which Objects
       Can Be Instantiated

• Class header or class definition parts
   – An optional access modifier
   – The keyword class
   – Any legal identifier for the name of your class
• Class access modifiers
   – public
   – protected
  – internal
   – private




                                                                               4
```

## PDF page 5

```text
Creating a Class from Which Objects
   Can Be Instantiated (cont'd.)





   public class Employee
    {
            // Instance variables and methods go here
    }

    - Better to use a modifier as default is internal


                                                                              5
```

## PDF page 6

```text
Creating Instance Variables and
             Methods

• When creating a class, define both its fields and its
  methods


•  Field access modifiers
  – new, public, protected, internal, private,
    static, readonly, and volatile


• Most class fields are nonstatic and private
   – Provides the highest level of security




                                                                               6
```

## PDF page 7

```text
Creating Instance Variables and
         Methods (cont'd.)

• Using private fields within classes is an example
  of information hiding

• Most class methods are public

• private data / public method arrangement
   – Allows you to control outside access to your data
         • Like using a gas gauge to “see” the level of the gas
   – The private data fields are manipulated by well-
     defined (and programmer-defined) interfaces provided
     by the public methods

                                                                               7
```

## PDF page 8

```text
Creating Instance Variables and
        Methods (cont'd.)
                                  - Better to use a modifier as default is internalpublic class Employee
{
    private int idNumber;
    public void WelcomeMessage()
    {
       Console.WriteLine(“Welcome from Employee #{0}”, idNumber);
       Console.WriteLine(“How can I help you?”);
     }
}

Employee class with idNumber field and WelcomeMessage()method
 Notice how the method has access to the idNumber field without having to
 pass the information as a parameter
 – instance methods have direct access to instance variables



                                                                                 8
```

## PDF page 9

```text
Creating Objects

• Declaring a class does not create any actual objects
   – Just an abstraction (like a method until it is invoked)
• Two-step process to create an object
   – Supply a type and an identifier
     Employee bob;
   – Create the object, which allocates memory for it
     bob = new Employee();


• Reference type
   – Identifiers for objects are references to their memory
     addresses



                                                                               9
```

## PDF page 10

```text
Creating Objects (cont'd.)



using System;
public static class CreateEmployee                                                  Invoking constructor
{                                       When you create an object,
  public static void Main()                   you call its constructor
                                              Employee() is   {
                                                              a method call
    Employee myAssistant = new Employee();
    myAssistant.WelcomeMessage();
    Console.ReadLine();
   }                 Invoking an object’s method
}





                                                                            10
```

## PDF page 11

```text
Constructors





                                                       11
```

## PDF page 12

```text
Understanding Constructors

• Constructor
   – Method that instantiates an object
• Default constructor
   – Automatically supplied constructor without parameters
   – The only time that C# provides a default constructor is
    when there are no programmer-defined constructors
• Default value of the object
   – The value of an object initialized with a default constructor
         • Numeric fields are set to 0
         • Character fields are set to ‘\0’
         • Boolean fields are set to false
         • References (strings and objects) are set to null

                                                                                  12
```

## PDF page 13

```text
Overloading Constructors

• C# automatically provides a default constructor
   – Until you provide your own constructor

• Constructors can be overloaded
   – You can write as many constructors as you want
         • As long as their argument lists do not cause ambiguity
         • Chooses constructor based on the signature





                                                                              13
```

## PDF page 14

```text
Passing Parameters to Constructors


• You can create a constructor that receives arguments





• Using the constructor
      Employee partTimeWorker = new Employee(12.50);





                                                                                14
```

## PDF page 15

```text
Overloading Constructors (cont'd.)


public class Employee
{
    private int idNumber;
    private double salary;
    public Employee()
    {             1        IdNumber = 999;
        Salary = 0;
    }
    public Employee(int empId)
    {                2        IdNumber = empId;
        Salary = 0;
    }
    public Employee(int empId, double sal)
    {                     3
        IdNumber = empId;
        Salary = sal;
    }
    public Employee(char code)
    {                 4
        IdNumber = 111;
        Salary = 100000;
    }
}


                                                                             15
```

## PDF page 16

```text
Overloading Constructors (cont'd.)

using System;
public static class CreateSomeEmployees                                          999             $0.00{
    public static void Main()                 234             $0.00
    {
                                            111        $100,000.00
        Employee aWorker = new Employee();

        Employee anotherWorker = new Employee(234);

        Employee theBoss = new Employee('A');

        Console.WriteLine("{0}   {1:C}", aWorker.IdNumber, aWorker.Salary);

        Console.WriteLine("{0}   {1:C}", anotherWorker.IdNumber,

                         anotherWorker.Salary);

        Console.WriteLine("{0}   {1:C}", theBoss.IdNumber, theBoss.Salary);

        Console.ReadLine();
    }
}





                                                                                17
```

## PDF page 17

```text
Passing Objects to Methods

• You can pass objects to methods
   – Just as you can with simple data types

  using System;
                                                                  First employee's message  public class CreateEmployee
                                             Welcome from Employee #0
  {                                     How can I help you?
    public static void Main()
    {                                            Second employee's message
     Employee aWorker = new Employee();    Welcome from Employee #0
     Employee bWorker = new Employee();   How can I help you?
      DisplayMessage("First", aWorker);
      DisplayMessage("Second", bWorker);
    }
    public static void DisplayMessage(string mess, Employee emp)
    {
      Console.WriteLine("\n{0} employee's message", mess);
     emp.WelcomeMessage();
    }
  }

                                                                              18
```

## PDF page 18

```text
Accessors and Mutators





                                                               19
```

## PDF page 19

```text
Accessor and Mutator Methods

• Because of the concept of data hiding, fields in
  a class are private.
• The methods that retrieve the data of fields are
  called accessors.
   – Each field that the programmer wishes to be viewed by
     other classes needs an accessor.

• The methods that modify the data of fields are
  called mutators.
   – Each field that the programmer wishes to be modified by
     other classes needs a mutator.
```

## PDF page 20

```text
Properties


• C# has an alternative to using accessor and
  mutator methods, called properties.


• Properties allow us to modify and access
  private data members like accessor and
  mutator methods without using public
  methods.
```

## PDF page 21

```text
Creating Properties

• Property
   – A member of a class that provides access to a field of
    a class (very helpful for private fields)
   – Defines how fields will be set and retrieved
•  Properties have accessors
   – set accessors for setting an object’s fields
         • setters (also called mutators)
   – get accessors for retrieving the stored values
         • getters (or just accessors)
• Read-only property
   – Has only a get accessor

                                                                              22
```

## PDF page 22

```text
Properties
            Example

public double Length
{
   get
   {
      return length;
   }
   set
   {
    length = value;
   }
 }
```

## PDF page 23

```text
Properties


• key words get, set and value.


• The get and set blocks replace the function of the
  accessor and mutator methods.


• The get and set blocks use a variable named value
    –  Implicit Parameter:
             • one that is undeclared and that gets its value automatically
   – The get block uses the value to return the actual
     value of the instance field.
   – The set block uses the value to set the value of the
     instance field.
```

## PDF page 24

```text
Creating Properties (cont'd.)

public class Employee
{
  private int idNumber;
  public int IdNumber                          Notice
   {
     get
     {
       return idNumber;
     }
     set
     {
      idNumber = value;
     }
   }
  public void WelcomeMessage()
   {
  Console.WriteLine("Welcome from Employee #{0}", IdNumber);
  Console.WriteLine("How can I help you?");
   }
}


                                                                             25
```

## PDF page 25

```text
Creating Properties (cont'd.)

    using System;
    public class UseEmployeeProperties                                                 ID number is 9
    {                                                 Welcome from Employee #9
      public static void Main()                 How can I help you?
       {
       Employee myEmployee = new Employee();                                      value becomes 9
       myEmployee.IdNumber = 9;

        Console.WriteLine(“ID number is {0}”, myEmp.IdNumber);

       myEmployee.WelcomeMessage();
       }
    }
•  Notice how the property is used by an object


   myEmployee.idNumber = 9; // this would result in an error



                                                                                 26
```

## PDF page 26

```text
Using Auto-Implemented Properties


• Auto-implemented property
   – The property’s implementation is created for you
     automatically with the assumption that:
         • The set accessor should simply assign a value to the
         appropriate field
         • The get accessor should simply return the field
• When you use an auto-implemented property:
   – You do not need to declare the field that corresponds
      to the property





                                                                              27
```

## PDF page 27

```text
Using Auto-Implemented Properties
                 (cont'd.)

using System;
public static class CreateEmployee3
{
  public static void Main()
   {
    Employee aWorker = new Employee();
    aWorker.IdNumber = 3872;
    aWorker.Salary = 22.11;
    Console.WriteLine("Employee #{0} makes {1:C}", aWorker.IdNumber, aWorker.Salary);
    Console.ReadLine();
   }
}
public class Employee
{
                                       Notice no private fields  public int IdNumber { get; set; }
  public double Salary { get; set; }
}



                                                                                 28
```

## PDF page 28

```text
More about classes





                                                          29
```

## PDF page 29

```text
More About public, private,
   and static Access Modifiers

public class Carpet
{
    public static string MOTTO = "Our carpets are quality-made";
    private int length;
    private int width;
    private int area;                          A static data field belongs to
    public int Length
                                             the entire class, not to any
    {
                                                particular instance.        get
        { return length; }
        set
        {
            length = value;
            CalcArea();
        }
    }

                                                                             31
```

## PDF page 30

```text
More About public, private,
 and static Access Modifiers

public int Width
    {
        get { return width; }
        set
        {
            width = value;
            CalcArea();
        }
    }

    public int Area
    {
        get
        {
            return area;
        }
    }
    private void CalcArea()
    {
        area = Length * Width;
    }
}
//Figure 9-13 The Carpet class

                                                                       32
```

## PDF page 31

```text
More About public, private,
 and static Access Modifiers




                                    The 12 X 14 carpet has an area of 164
                                    Our motto is: Our carpets are quality-made





                                 Notice how the static
                     MOTTO is accessed


                                                                         33
```

## PDF page 32

```text
Classes and Instances

• Recall
   – Classes are defined to represent a single concept or
      service.


   – Each instance of the class contains different data
     (stored in the instance variables or fields)


   – The instances all share the same design and have
     access to the same properties and instance methods
```

## PDF page 33

```text
The this Reference


• You might eventually create thousands of objects
  from a class
   – Each object does not need to store its own copy of
     each property and method

• this reference
   – Implicitly passed reference

• When you call a method, you automatically pass the
  this reference to the method
   – Tells the method which instance of the class to use


                                                                              35
```

## PDF page 34

```text
Overloading Operators





                                                             36
```

## PDF page 35

```text
Overloading Operators

•  Overload operators
   – Enable you to use arithmetic symbols with your own objects
•  Overloadable unary operators:
    + - ! ~ ++ -- true false
• Overloadable binary operators:
    + - * / % & | ^ == != > < >= <=
• Cannot overload the following operators:
     = && || ?? ?: checked unchecked new typeof as is
• Cannot overload an operator for a built-in data type
   – E.g., cannot change the meaning of + for int





                                                                               37
```

## PDF page 36

```text
Overloading Operators (cont'd.)

• Syntax to overload unary operators:


      type operator overloadable-operator (type identifier)

• Syntax to overload binary operators:


      type operator overloadable-operator (type identifier, type
      operand)


   public static Book operator +(Employee E1, Employee E2)
   {
         Body…
   }


                                                                               38
```

## PDF page 37

```text
Overloading Operators (cont'd.)

• When a binary operator is overloaded and has a
  corresponding assignment operator:
   – It is also overloaded
         • e.g. + and +=


• Some operators must be overloaded in pairs:
    == with !=, and < with >





                                                                               39
```

## PDF page 38

```text
Overloading Operators (Class)

public class Book                                           public Book(){                                                   {  private string title;                                                     Title = "";  private int numPages;                                     NumPages = 0;  private double price;                                                Price = 0;
                                                   }  public string Title                                             public Book(string title, int pages, double price)   {                                                   {     get                                                     Title = title;     { return title; }                                     NumPages = pages;     set                                                Price = price;     { title = value; }                                                   }   }                                             public static Book operator +(Book first, Book second)  public int NumPages
                                                   {   {
                                                const double EXTRA = 10.00;     get
                                      Book third = new Book();     { return numPages; }
                                                     third.Title = first.Title + " and " + second.Title;     set
     { numPages = value; }                    third.numPages = first.NumPages + second.NumPages;
   }                                                                 if (first.Price > second.Price)
  public double Price                               third.Price = first.Price + EXTRA;
   {                                                   else
     get                                             third.Price = second.Price + EXTRA;
     { return price; }                           return third;
     set                                           }
     { price = value; }                          }
   }

                                                                                40
```

## PDF page 39

```text
Overloading Operators (Driver)

using System;
public static class Addßooks
{
  public static void Main()
   {
    Book book1 = new Book("Visual C#", 840, 75.00);
    Book book2 = new Book("Moby Dick", 250, 16.00);
    Book book3;
    book3 = book1 + book2;
    Console.WriteLine("The new book is \"{0}\"", book3.Title);
    Console.WriteLine("It has {0} pages and costs {1:C}", book3.NumPages, book3.Price);
    Console.ReadLine();
   }
}


                The new book is "Visual C# and Moby Dick"
                            It has 1090 pages and costs $85.00




                                                                             41
```

## PDF page 40

```text
Overloading Operators (more)

•  Let’s add a unary operator (-) to the Book class
   – Assume we define this operator to cut the title and number
      of pages in half and reduce the price to 75% of the original
   – We have complete control over how the operators behave


      public static Book operator -(Book tome)
      {
      Book newBook = new Book();
       newBook.Title = tome.Title.Substring(0,tome.Title.Length/2);
      newBook.NumPages = tome.NumPages/2;
       newBook.Price = tome.Price * 0.75;
        return newBook;
      }





                                                                               45
```

## PDF page 41

```text
Overloading Operators (one more)
• Add relational operators (>= and <=) to the Book class
   – They have to be added in pairs and unlike the first two
     which create a new Book, these return true or false
   – Notice that we can define the operators anyway we want


       public static bool operator <=(Book b1, Book b2)
        {
              if ((b1.NumPages / b1.Price) <= (b2.NumPages / b2.Price))
           return true;
           else
           return false;
        }
       public static bool operator >=(Book b1, Book b2)
        {
              if ((b1.Title.Length > b2.Title.Length)
           return true;
           else
           return false;
        }


                                                                             46
```

## PDF page 42

```text
Overloading Operators (Driver)

using System;
public static class Addßooks3
{
  public static void Main()
   {
    Book book1 = new Book("Visual C#: For Fun and Profit", 840, 75.00);
    Book book2 = new Book("Moby Dick", 250, 16.00);
       if (book1 >= book2)
      Console.WriteLine("Purchase Book 1");
     else
      Console.WriteLine("Purchase Book 2");
       if (book1 <= book2)
      Console.WriteLine("Purchase Book 1");
     else
      Console.WriteLine("Purchase Book 2");
    Console.ReadLine();
   }                                               Purchase Book1
}                                                 Purchase Book 1





                                                                             47
```

## PDF page 43

```text
Declaring an Array of Objects

• You can declare arrays that hold elements of any type
   – Including objects
• Example
   Employee[] empArray = new Employee[7];


   for(int x = 0; x < empArray.Length; ++x)
      empArray[x] = new Employee();





                                                                               48
```

## PDF page 44

```text
Destructors





                                                  49
```

## PDF page 45

```text
Understanding Destructors

 • Destructor
   – Contains the actions you require when an instance of
     a class (object) is destroyed
 • Most often, an instance of a class is destroyed when
     it goes out of scope (program terminates)
   – Can be used to clean up when the object is destroyed
      (release memory)
•  Explicitly declare a destructor
   – Identifier consists of a tilde (~)    ~ClassName()
                                       {     followed by the class name
                                             ...Body...
                                       }

                                                                               50
```

## PDF page 46

```text
Understanding Destructors (cont'd.)


public class Employee
{
  public int IdNumber {get; set;}

  public Employee(int empId)
   {
    IdNumber = empId;
    Console.WriteLine("Employee object {0} created", IdNumber);
   }
  ~Employee()
   {
      Console.WriteLine("Employee object {0} destroyed!", IdNumber);
   }
}



                                                                                51
```

## PDF page 47

```text
Understanding Destructors (cont'd.)




                                             Employee object 101 created
using System;                                Employee object 202 created
public static class DemoEmployeeDestructor   Employee object 202 destroyed
{                                            Employee object 101 destroyed
  public static void Main()
   {
    Employee aWorker = new Employee(101);
    Employee anotherWorker = new Employee(202);
   }
}





                                                                                52
```

## PDF page 48

```text
Summary

• You can create classes that are only programs with
  a Main() method and classes from which you
  instantiate objects
• When creating a class:
   – Must assign a name to it and determine what data
    and methods will be part of the class
   – Usually declare instance variables to be private
    and instance methods to be public
• When creating an object:
   – Supply a type and an identifier, and you allocate
     computer memory for that object




                                                                              66
```

## PDF page 49

```text
Summary (cont'd.)

• A property is a member of a class that provides
  access to a field of a class
• Class organization within a single file or separate
   files
• Each instantiation of a class accesses the same
  copy of its methods
• A constructor is a method that instantiates (creates
  an instance of) an object
• You can pass one or more arguments to a
  constructor




                                                                              67
```

## PDF page 50

```text
Summary (cont'd.)


• Constructors can be overloaded
• You can pass objects to methods just as you can
  simple data types
• You can overload operators to use with objects
• You can declare arrays that hold elements of any
  type, including objects
• A destructor contains the actions you require when
  an instance of a class is destroyed





                                                                              68
```

