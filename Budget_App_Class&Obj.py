class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def transfer(self, amount, destination):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {destination.name}")
            destination.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def __str__(self):
        title = f'{self.name:*^30}\n'
    
        items = ''
        for item in self.ledger:
            desc = item['description'][:23]       # max 23 chars
            amount = f"{item['amount']:.2f}"       # 2 decimal places
            items += f'{desc:<23}{amount:>7}\n'    # left + right aligned in 30 chars
    
            total = f'Total: {self.get_balance():.2f}'
        return title + items + total

def create_spend_chart(categories):
    # 1. Calculate total withdrawals per category
    spent = []
    for cat in categories:
        total = sum(-item['amount'] for item in cat.ledger if item['amount'] < 0)
        spent.append(total)
    
    grand_total = sum(spent)
    
    # 2. Round DOWN to nearest 10
    percentages = [int((s / grand_total) * 100) // 10 * 10 for s in spent]
    
    # 3. Build the chart rows (100 down to 0)
    chart = 'Percentage spent by category\n'
    for level in range(100, -1, -10):
        row = f'{level:>3}|'
        for pct in percentages:
            row += ' o ' if pct >= level else '   '
        row += ' \n'
        chart += row
    
    # 4. Horizontal line
    chart += '    ' + '-' * (len(categories) * 3 + 1) + '\n'
    
    # 5. Category names vertically
    names = [cat.name for cat in categories]
    max_len = max(len(n) for n in names)
    for i in range(max_len):
        row = '    '
        for name in names:
            row += f' {name[i]} ' if i < len(name) else '   '
        row += ' \n'
        chart += row
    
    return chart.rstrip('\n')
