using System;
public static class Lab3_2
{
    public static void Main()
    {
        const double FLAT = 1.25;
        double weight;
        double cost, pricePerKg = 0;

        Console.Clear();
        do{
        Console.WriteLine("Enter your package weight: \nNOTE: Ensure there are no hyphens(-) before your entry");
        weight = Convert.ToDouble(Console.ReadLine());
            if(weight <= 0){
            Console.WriteLine("*** Invalid Weight. \nYou enterered {0}", weight);
            cost = 0;

            }else if(weight > 0 && weight < 1){
                pricePerKg = .25;
                cost = weight * pricePerKg + FLAT; 
            }else if(weight >= 1 && weight <= 3.5){
                pricePerKg = .50;
                cost = weight * pricePerKg + FLAT; 
            }else{
                pricePerKg = 1;
                cost = weight * pricePerKg + FLAT; 
            }

            Console.WriteLine("The cost to send the package is {0:C}", cost);

            }
        while(weight <= 0);
    }
}