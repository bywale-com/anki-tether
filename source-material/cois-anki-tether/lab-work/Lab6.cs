using System;
public static class Lab6
{
    public static void Main()
    {
        double ratePay, taxRate, grossPay, netPay=0, hrsWrked, overtime; 
        string lastName;

        Console.Clear();
        Console.WriteLine("Enter your lastname: ");
        lastName = Console.ReadLine();
        
        Console.WriteLine("Enter your hours worked: ");
        do{
            hrsWrked = Convert.ToDouble(Console.ReadLine());
        } while (hrsWrked <= 0.0);
        
        Console.WriteLine("Enter your hourly rate: ");
        do{
            ratePay= Convert.ToDouble(Console.ReadLine());
        } while (ratePay < 10);
        
        Console.WriteLine("Enter your tax rate: ");
        do{
            taxRate = Convert.ToDouble(Console.ReadLine());
        } while (taxRate < 0.0 || taxRate > 1.0);

        grossPay = CalculateGross(hrsWrked, ratePay);
        if(hrsWrked > 40){
            overtime = CalculatorOT(hrsWrked, ratePay);
        } else { overtime = 0;}

        CalculateNet (grossPay, taxRate, ref netPay);
        netPay += overtime;

        Console.WriteLine("{0}, Hours: {1}, Rate: {2}, Net Pay: {3}, Gross Pay{4}", lastName, hrsWrked, ratePay, netPay, grossPay);
        

    }

    public static double CalculateGross(double hours, double rate)
    {
        double gross = hours * rate;
        return gross;
    }

    public static void CalculateNet(double grossP, double tax, ref double netP)
    {
        netP = grossP - (grossP * tax);
    }

    public static double CalculatorOT(double hours, double rate)
    {
        double overtime = (hours - 40) * (rate * .5);
        return overtime;
    }
}