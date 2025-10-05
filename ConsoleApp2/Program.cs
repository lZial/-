using System;
using System.Collections.Generic;

namespace ConsoleApp1
{
    internal class Program
    {
        static void Main(string[] args)
        {
            bool continueCalculations = true;
            Queue<string> history = new Queue<string>(5);

            Console.WriteLine("Простой калькулятор");

            while (continueCalculations)
            {
                // Ввод двух чисел
                Console.Write("Введите первое число: ");
                int num1 = Convert.ToInt32(Console.ReadLine());

                Console.Write("Введите второе число: ");
                int num2 = Convert.ToInt32(Console.ReadLine());

                // Меню операций
                Console.WriteLine("\nВыберите операцию:");
                Console.WriteLine("1. - Сложение");
                Console.WriteLine("2. - Вычитание");
                Console.WriteLine("3. - Умножение");
                Console.WriteLine("4. - Деление");
                Console.WriteLine("5. - Выход");
                Console.Write("\nВаш выбор: ");

                string choice = Console.ReadLine();
                Console.WriteLine();

                // Обработка выбора операции
                switch (choice)
                {
                    case "1": // Сложение
                        int result = num1 + num2;
                        string operation = $"{num1} + {num2} = {result}";
                        Console.WriteLine($"Результат: {operation}");
                        AddToHistory(history, operation);
                        break;

                    case "2": // Вычитание
                        result = num1 - num2;
                        operation = $"{num1} - {num2} = {result}";
                        Console.WriteLine($"Результат: {operation}");
                        AddToHistory(history, operation);
                        break;

                    case "3": // Умножение
                        result = num1 * num2;
                        operation = $"{num1} * {num2} = {result}";
                        Console.WriteLine($"Результат: {operation}");
                        AddToHistory(history, operation);
                        break;

                    case "4": // Деление
                        if (num2 != 0)
                        {
                            result = num1 / num2;
                            operation = $"{num1} / {num2} = {result}";
                            Console.WriteLine($"Результат: {operation}");
                            AddToHistory(history, operation);
                        }
                        else
                        {
                            Console.WriteLine("Ошибка: деление на ноль!");
                        }
                        break;

                    case "5": // Выход
                        continueCalculations = false;
                        Console.WriteLine("Выход из программы.");
                        break;

                    default:
                        Console.WriteLine("Неверный выбор операции.");
                        break;
                }

                // Вывод истории операций (как в калькуляторе телефона)
                if (history.Count > 0 && choice != "5")
                {
                    Console.WriteLine("\nИстория операций:");
                    foreach (string op in history)
                    {
                        Console.WriteLine(op);
                    }
                }

                if (choice != "5")
                {
                    Console.WriteLine("\n" + new string('-', 30));
                }
            }
        }

        static void AddToHistory(Queue<string> history, string operation)
        {
            if (history.Count >= 5)
            {
                history.Dequeue();
            }
            history.Enqueue(operation);
        }
    }
}
