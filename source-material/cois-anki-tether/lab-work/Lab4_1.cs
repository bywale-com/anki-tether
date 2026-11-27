using System;
public static class Lab4_1
{
    public static void Main()
    {
        int value = 0;
        int count = 0;
        double average = 0.0;
        int sum = 0;

        Console.Clear();
        Console.WriteLine("Enter a positive integer (-1 to stop): ");
        value = Convert.ToInt32(Console.ReadLine());
        while(value >= 0){
            sum += value;
            count++;
            value = Convert.ToInt32(Console.ReadLine());
        }

        if(count > 0){
            average = sum / (double)count;
        }

        Console.WriteLine("sum = {0}, count = {1} \naverage = {2}", sum, count, average);
        
    }
}