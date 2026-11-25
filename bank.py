from models import DepositType, PromoCondition


class Bank:
    def __init__(self):
        self.types = [
            DepositType("Классический", 7.5, 10000, 36, "simple"),
            DepositType("Выгодный", 8.0, 50000, 24, "compound",
                        [PromoCondition("Приветственная", 1.5),
                         PromoCondition("Онлайн", 0.5)]),
            DepositType("Накопительный", 6.5, 1000, 12, "simple"),
        ]

    def add(self, t):
        self.types.append(t)

    def __str__(self):
        return "\n".join(f"{i}. {t}" for i, t in enumerate(self.types, 1))

    def __len__(self):
        return len(self.types)

    def __getitem__(self, i):
        return self.types[i]