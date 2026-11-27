using System;
public static class Lab7
{
    public static void Main()
    {
        string[]dataArray = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"];
        int n = 0;

        Console.Clear();
    
        Fill(dataArray, ref n);
        Dump(dataArray, n);
        ReverseDump(dataArray, n);

    
    }

    public static void Fill(string[] arrValues, ref int num)
    {
        Console.WriteLine("How many values are you entering? ");
        do{
            num = Convert.ToInt32(Console.ReadLine());
        }while(num < 1 || num > 10);

        for(int i = 0; i < num; i++)
        {
            Console.WriteLine("Enter name[{0}]", i);
            arrValues[i] = Console.ReadLine();
        }
    }
    

    public static void Dump(string[] arrVals, int num)
    {
        Console.WriteLine("The elements in the array are: ");
        for( int i = 0; i < (num - 3); i++){
            Console.WriteLine("[{0}]", arrVals[i]);
        }
    }

    public static void ReverseDump(string[] arrItems, int num)
    {
        Console.WriteLine("The elements in reverse are: ");
        for(int i = num-1; i >= 0; i--){
            Console.WriteLine("[{0}]", arrItems[i]);
        }
    }

    public static int FindName(string name, string[] arrItems, int num)
    {
        for(int i = 0; i < num; i++){
            string namep = arrItems[i];
            if(name = namep){
                return i;
            } else{
                return i;
            }
            Console.WriteLine("$ {namep}");

            // } else { 
            //     Console.WriteLine("does not exist");
            //     return i;
            // }
        }
    }
}