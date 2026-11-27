public static class Lab2
{
    public static void Main()
    {
        // initialize all variables to be used in this Calculation method.
        int idNum;
        double payRate, hours, grossPay, netPay, taxRate;
        string firstName, lastName;

        Console.Clear();
        Console.WriteLine("Enter Employee's First Name ==> ");
        firstName = Console.ReadLine();
        
        Console.WriteLine("Enter Employee's Last Name ==> ");
        lastName = Console.ReadLine();

        Console.WriteLine("Enter Employee's ID==> ");
        idNum = Convert.ToInt32(Console.ReadLine());
        // Because by default input is a string, we need to convert the input into other types where necessary i.e when the input is passed into an integer, double e.t.c
        
        Console.WriteLine("Enter Employee's Hours worked==> ");
        hours = Convert.ToDouble(Console.ReadLine());

        Console.WriteLine("Enter Employee's hourly rate ==> ");
        payRate = Convert.ToDouble(Console.ReadLine());
 
        Console.WriteLine("Enter Employee's tax rate ==> ");
        taxRate = Convert.ToDouble(Console.ReadLine());

        grossPay = hours * payRate; 
        // Because grosspay is a double it can accept the value.

        netPay = ((100 - taxRate) / 100) * grossPay;

        Console.WriteLine("Employee: {0} {1}, (ID: {2}) earned {3:C} ", firstName, lastName, idNum, netPay );
        // positiional placeholders reference method variables.




    }
}