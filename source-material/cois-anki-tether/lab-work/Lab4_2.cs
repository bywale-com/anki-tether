using System;
public static class Lab4_2
{
    public static void Main()
    {
        const int PASS = 50;
        int numPass=0, numFail=0, totalMarks=0;
        double mark, perPass=0, perFail=0;

        Console.WriteLine("Enter your marks \n NOTE: Numeric marks from 0 through 100 only");
        do{
            mark = Convert.ToDouble(Console.ReadLine());
            while(mark > 100){
                mark = 0;
            }

            totalMarks += mark;

    
        } while(mark >= 0);

    }
}