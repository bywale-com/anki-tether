using System;
public static class Lab8
{
    public static void Main()
    {
        int[] compStats = new int[25];
        int n=0, large, small;
        double avg=0;
    
        InpArray(compStats, ref n);
        avg = FindAverage(compStats, n);
        large = FindLarge(compStats, n);
        small = FindSmall(compStats, n);

        Console.WriteLine("average: {0}, largest: {1}, smallest: {2}", avg, large, small);
    }
    // FindSmall();

    public static void InpArray(int[] arrValues, ref int num )
    {
        Console.WriteLine("How many values are entering?: ");
        do{
            num = Convert.ToInt32(Console.ReadLine());
        }while ( num < 0 || num > 25);
        
        Console.WriteLine("Enter the values: \nEnsure you enter any negative values, letters or symbols.\nJust positive numbers");
        for(int i = 0; i < num; i++)
        {
            do{
                arrValues[i] = Convert.ToInt32(Console.ReadLine());
            } while (arrValues[i] > 25);
        }
        //test function to ensure the array is working properly.
        // foreach(int value in arrValues){
        //     Console.WriteLine(value);
        // }
        //test
    }

    public static double FindAverage(int[] arrVals, int num)
    {   
        double sum=0;
        for(int i = 0; i < num; i++)
        {   
            sum += arrVals[i];
        }
        double average = sum / (double)num;
        return average;

    }

    public static int FindLarge(int[] arrVals, int num)
    {   
        int largest = arrVals[0];
        foreach (int value in arrVals)
        {
            if(value <= largest)
            {
                largest = value;
            }

            //test code
        // Console.WriteLine(value);
        // Console.WriteLine(largest);
        }
        return largest;
    }
    public static int FindSmall(int[] arrVals, int num)
    {   
        int smallest = arrVals[0];
        foreach (int value in arrVals)
        {
            if(value >= smallest)
            {
                smallest = value;
            }

            //test code
        // Console.WriteLine(value);
        // Console.WriteLine(largest);
        }
        return smallest;
    }

}