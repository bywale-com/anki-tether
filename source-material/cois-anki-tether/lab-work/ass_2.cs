using System;
public static class Assignment_2
{
    public static void Main()
    {

        int num=0, category;
        int[,] expenses = new int[100, 100];
        string[] expenseTitle = ["Groceries", "Entertainment", "Transportation"];
        double income, total, balance;
        Console.Clear();
        Console.WriteLine("Enter your monthly income: ");
        
        income = VerifyIncome(Convert.ToDouble(Console.ReadLine()));
        ExpenseEntry(expenses, expenseTitle, ref num);
        total = TotalExpenses(expenses, num);
        balance = income - total;
        Console.WriteLine("\nTotal Expenses: {0:C}\nRemaining Balance: {1:C}", total, balance);

        do
        {
            Console.WriteLine("Would you like to see the Expense per Category? ( Y/N)");
            string reply = Console.ReadLine();
        }while(reply != "Y" || reply != "N");

        if(reply = "Y")
        {
            do
            {
                Console.WriteLine("Enter a valid Category Code: ");
                int category = Console.ReadLine();
            }while(category != 1 || category != 2 || category != 3);
            categoryTotal = checkCategoryExpense(expenses, num, category);
        }

         Console.WriteLine("\n{0} Total: {1:C}",expenseTitle[category-1],  categorytotal);
        //test print
        //Console.WriteLine(income);
        
        
        //array test

        // expenses[0, 0] = 20;
        // expenses[1, 0] = 20;
    }

    public static double VerifyIncome(double incomePerM)
    {
        while(incomePerM < 0)
        {
            Console.WriteLine("You need to make a non-negative income entry\nTry Again: ");
            incomePerM = Convert.ToDouble(Console.ReadLine());
        }
        return incomePerM;
    }

    public static void ExpenseEntry(int[,] expensesPerM, string[] expenseName, ref int num)
    {
        do{
            Console.WriteLine("Enter the amount of entries:");
            num = Convert.ToInt32(Console.ReadLine());
        }while(num < 0);

            Console.WriteLine("selected option:\n1. Grocery Expenses\n2. Entertainment Expenses\n3. Transportation Expenses");

            for(int i=0, j=0; i < num; i++)
            {
                Console.WriteLine("\nEntry {0}", i+1);
                Console.Write("Expense Type:  "); 
                expensesPerM[0, i] = Convert.ToInt32(Console.ReadLine());
                
                Console.Write("Expense Cost:  "); 
                expensesPerM[1, j] = Convert.ToInt32(Console.ReadLine());
                j++;
                

            }
            for(int i=0,j=0; i < num; i++)
                {
                    Console.WriteLine("Entry {0}: {1} - {2:C} ", i, expenseName[expensesPerM[0, i]-1], expensesPerM[1, j]);
                    j++;
                }
    }

    public static double TotalExpenses(int[,] expensesPerM, int num)
    {
        double sum=0;
        for(int i=0; i < num; i++)
        {
            sum+=expensesPerM[1, i];
        }
            return sum;
    }
    public static double CheckCategoryExpense(int[,] expensesPerM, int num, int category)
    {
        double sum=0;
        for(int i=0; i < num; i++)
            {
                if(expensesPerM[0, i] = category)
                {
                    sum+=expensesPerM[1, i];
                }
            }
        return sum;
    }
}