from bank import Bank
from interface import new_client, create_type, open_deposit


def main():
    bank = Bank()
    client = new_client()
    print(f"Клиент {client.name} ({client.age} лет) создан.\n")

    while True:
        print("\n--- МЕНЮ ---")
        print("1. Предложения банка")
        print("2. Создать вид вклада")
        print("3. Открыть вклад")
        print("4. Вклады клиента")
        print("5. Сменить клиента")
        print("6. Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            print(bank)
        elif choice == "2":
            try:
                bank.add(create_type())
                print("Вид вклада добавлен.")
            except ValueError:
                print("Ошибка ввода чисел.")
        elif choice == "3":
            open_deposit(bank, client)
        elif choice == "4":
            print(client)
        elif choice == "5":
            client = new_client()
            print(f"Теперь клиент {client.name} ({client.age} лет).")
        elif choice == "6":
            print("Выход.")
            break
        else:
            print("Неверный пункт.")


if __name__ == "__main__":
    main()