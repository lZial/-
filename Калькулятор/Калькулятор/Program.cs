using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Калькулятор
/*Шистерин Егор Дмитриевич, К-ИСП-29-1
  Начало работы - 05.10.25. 00:30 AM | Окончание работы - 05.10.25. 03:40 AM */
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Queue<string> history = new Queue<string>();

            while (true)
            {

                Console.WriteLine("Простой калькулятор");

                Console.WriteLine("\nПервое число: ");
                var num1 = double.Parse(Console.ReadLine());
                Console.WriteLine("Второе число: ");
                var num2 = double.Parse(Console.ReadLine());

                Console.WriteLine("\nВыберите операцию: ");
                Console.WriteLine("1-Сложение\n2-Вычитание\n3-Умножение\n4-Деление\n5-Выход");
                Console.WriteLine("\nВаш выбор: ");
                var operation = int.Parse(Console.ReadLine());

                string answer = string.Empty;
                switch (operation)
                {
                    case 1:

                        answer = $"{num1} + {num2} = {num1 + num2}";
                        Console.WriteLine($"Ответ:\n{answer}");
                        break;

                    case 2:

                        answer = $"{num1} - {num2} = {num1 - num2}";
                        Console.WriteLine($"Ответ:\n{answer}");
                        history.Enqueue(answer);
                        break;

                    case 3:

                        answer = $"{num1} * {num2} = {num1 * num2}";
                        Console.WriteLine($"Ответ:\n{answer}");
                        history.Enqueue(answer);
                        break;

                    case 4:

                        answer = $"{num1} / {num2} = {num1 / num2}";
                        if (num2 == 0) Console.WriteLine("Ошибка, деление на ноль невозможно");
                        else
                            Console.WriteLine($"Ответ:\n{answer}");
                        history.Enqueue(answer);
                        break;

                    case 5:

                        Environment.Exit(1);
                        break;

                }

                if (history.Count > 5)
                    history.Dequeue();

                Console.WriteLine("\nИстория:");

                foreach (var historyElement in history)
                    Console.WriteLine(historyElement);

                Console.WriteLine("Нажмите любую клавишу, чтобы продолжить...");
                Console.ReadKey();
                Console.Clear();

            }
        }
    }
}
