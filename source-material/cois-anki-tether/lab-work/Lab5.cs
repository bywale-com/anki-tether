using System;
public static class Lab5
{
    public static void Main()
    {
        int inpMark;
        string lastName;
        char grade = ' ';

        Console.Clear();
        Console.WriteLine("Enter your lastname: ");
        lastName = Console.ReadLine();
        
        Console.WriteLine("Enter your lastname: ");
        do{
            inpMark= Convert.ToInt32(Console.ReadLine());
        } while(inpMark < 0 || inpMark > 100);

        grade = MarkToGrade(inpMark);
        Console.WriteLine("{0}'s grade is {1}", lastName, grade);


    }

    public static char MarkToGrade(int inpMark)
    {
        char grade = ' ';
        if(inpMark >= 0 && inpMark <= 49){
            grade = 'F';
        } else if(inpMark >= 50 && inpMark <= 59){
            grade = 'D';
        }
        else if(inpMark >= 60 && inpMark <= 74){
            grade = 'C';
        } else if(inpMark >= 75 && inpMark <= 84){
            grade = 'B';
        }
        else if(inpMark >= 85 && inpMark <= 100){
            grade = 'A';
        } else{
            Console.WriteLine("Invalid entry");
            grade = 'X';
        }
        return grade;
    }
}