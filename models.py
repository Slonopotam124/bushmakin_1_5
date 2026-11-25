class PromoCondition:
    def __init__(self, name, rate_bonus):
        self.name = name
        self.rate_bonus = rate_bonus

    def __str__(self):
        return f"{self.name} (+{self.rate_bonus}%)"


class AgePromoCondition(PromoCondition):
    def __init__(self, age):
        if age < 25:
            name, rate_bonus = "Молодежная надбавка", 1.0
        elif age >= 60:
            name, rate_bonus = "Пенсионная надбавка", 1.5
        else:
            name, rate_bonus = "Возрастная надбавка", 0.0
        super().__init__(name, rate_bonus)


class DepositType:
    def __init__(self, name, base_rate, min_sum, max_term, calc_method, promos=None):
        self.name = name
        self.base_rate = base_rate
        self.min_sum = min_sum
        self.max_term = max_term
        self.calc_method = calc_method
        self.promos = promos or []

    def rate(self, extra=None):
        promos = self.promos + (extra or [])
        return self.base_rate + sum(p.rate_bonus for p in promos)

    def income(self, amount, term, extra=None):
        r = self.rate(extra) / 100
        if self.calc_method == "simple":
            inc = amount * r * term / 12
        else:
            inc = amount * (1 + r / 12) ** term - amount
        return inc, amount + inc

    def __str__(self):
        method = "сложный" if self.calc_method == "compound" else "простой"
        promos = ", ".join(p.name for p in self.promos) or "нет"
        return (f"{self.name}: ставка {self.base_rate}%, мин. сумма {self.min_sum}, "
                f"срок до {self.max_term} мес., метод {method}, акции: {promos}")


class ClientDeposit:
    def __init__(self, deposit_type, amount, term, age):
        self.type = deposit_type
        self.amount = amount
        self.term = term
        self.age_promo = AgePromoCondition(age)
        self.check()

    def check(self):
        if self.amount < self.type.min_sum:
            raise ValueError(f"сумма меньше {self.type.min_sum}")
        if self.term > self.type.max_term:
            raise ValueError(f"срок больше {self.type.max_term} мес.")

    def __str__(self):
        inc, total = self.type.income(self.amount, self.term, [self.age_promo])
        rate = self.type.rate([self.age_promo])
        return (f"{self.type.name}: {self.amount} руб. на {self.term} мес., "
                f"ставка {rate:.2f}% ({self.age_promo}), "
                f"доход {inc:.2f}, итого {total:.2f}")


class Client:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.deposits = []

    def open(self, deposit_type, amount, term):
        dep = ClientDeposit(deposit_type, amount, term, self.age)
        self.deposits.append(dep)
        return dep

    def __str__(self):
        if not self.deposits:
            return f"{self.name} ({self.age} лет): вкладов нет"
        lines = [f"{self.name} ({self.age} лет):"]
        for i, d in enumerate(self.deposits, 1):
            lines.append(f"  {i}. {d}")
        return "\n".join(lines)