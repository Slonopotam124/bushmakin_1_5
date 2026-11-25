from models import DepositType, PromoCondition, Client


def ask_yes_no(prompt):
    """Запрашивает ответ да/нет, принимает 'да'/'нет' (и англ. варианты)."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ('да','yes'):
            return True
        if answer in ('нет','no'):
            return False
        print("Ответьте 'да' или 'нет'.")


def ask_positive_float(prompt, allow_zero=False):
    """Запрашивает положительное число (или >= 0, если allow_zero)."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0 or (allow_zero and value == 0):
                return value
            print("Значение должно быть больше нуля." if not allow_zero else "Значение не может быть отрицательным.")
        except ValueError:
            print("Нужно число.")


def ask_positive_int(prompt):
    """Запрашивает положительное целое число."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Нужно целое число.")
            continue
        if value <= 0:
            print("Значение должно быть больше нуля.")
            continue
        return value


def ask_age():
    while True:
        try:
            age = int(input("Возраст клиента (14-120): "))
        except ValueError:
            print("Нужно целое число.")
            continue
        if age < 14 or age > 120:
            print("Возраст вне диапазона 14-120.")
            continue
        return age


def new_client():
    name = input("Имя клиента: ").strip() or "Клиент"
    return Client(name, ask_age())


def create_type():
    name = input("Название: ").strip()
    while not name:
        print("Название не может быть пустым.")
        name = input("Название: ").strip()

    rate = ask_positive_float("Ставка (%): ")
    min_sum = ask_positive_float("Мин. сумма: ")
    max_term = ask_positive_int("Макс. срок (мес.): ")

    while True:
        m = input("Метод (1-простой, 2-сложный): ").strip()
        if m in ("1", "2"):
            break
        print("Введите 1 или 2.")
    method = "simple" if m == "1" else "compound"
    
    bonus = [PromoCondition("Специальная", 1.0)] if ask_yes_no("Акция +1%? (да/нет): ") else []
    
    return DepositType(name, rate, min_sum, max_term, method, bonus)


def open_deposit(bank, client):
    if len(bank) == 0:
        print("Нет доступных вкладов.")
        return
    print("\nДоступные вклады:")
    for i in range(len(bank)):
        t = bank[i]
        print(f"  {i+1}. {t.name} (мин. {t.min_sum}, до {t.max_term} мес.)")

    try:
        idx = int(input("Номер вклада: "))
    except ValueError:
        print("Ошибка: нужно целое число.")
        return
    if idx < 1 or idx > len(bank):
        print("Ошибка: нет вклада с таким номером.")
        return

    t = bank[idx - 1]

    amount = ask_positive_float(f"Сумма (мин. {t.min_sum}): ")
    term = ask_positive_int(f"Срок (до {t.max_term} мес.): ")

    try:
        print(f"\nОткрыт вклад: {client.open(t, amount, term)}")
    except ValueError as e:
        print(f"Ошибка: {e}")