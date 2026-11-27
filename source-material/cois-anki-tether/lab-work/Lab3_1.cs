using System;
public static class Lab3_1
{
    public static void Main()
    {
        int numPens, numNicks, numDimes, numQuarts, numLoons, numTwoons;
        double amtInPiggyBank;
        string name;

        Console.Clear();
        Console.WriteLine("Enter your name: ");
        name = Console.ReadLine();
        
        Console.WriteLine("Enter your Pennies: ");
        numPens = Convert.ToInt32(Console.ReadLine());
        
        Console.WriteLine("Enter your Nickels: ");
        numNicks = Convert.ToInt32(Console.ReadLine());
        
        Console.WriteLine("Enter your Dimes: ");
        numDimes = Convert.ToInt32(Console.ReadLine());
       
        Console.WriteLine("Enter your Quarters: ");
        numQuarts = Convert.ToInt32(Console.ReadLine());
       
        Console.WriteLine("Enter your Loonies: ");
        numLoons = Convert.ToInt32(Console.ReadLine());
       
        Console.WriteLine("Enter your Twoonies: ");
        numTwoons = Convert.ToInt32(Console.ReadLine());

        amtInPiggyBank = Convert.ToDouble((numPens * 0.01) + (numNicks * 0.05) + (numDimes * 0.10) + (numQuarts * 0.25) + numLoons + (numTwoons * 2));
        Console.WriteLine("{0} has {1:C} in the Piggy Bank", name, amtInPiggyBank);
    }
}