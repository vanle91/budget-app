class Category:

  def __init__(self, category):
    self.category = category
    self.ledger = list()
    self.balance = 0

  def __str__(self):
    output = ""
    category_len = len(self.category)
    stars = "*" * int((30 - category_len) / 2)
    output = f"{output}{stars}{self.category}{stars}\n"

    for item in self.ledger:
      description = item['description'][:23]
      amount = "{:.2f}".format(item['amount'])
      line = f"{description : <23}{amount : >7}\n"
      output += line

    output += f"Total: {self.balance}"
    return output
  
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount
    
  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.balance -= amount
      self.ledger.append({"amount": -amount, "description": description})
      return True
    
    return False
    
  def get_balance(self):
    return self.balance
    
  def transfer(self, amount, cls):
    if self.check_funds(amount):
      withdraw_amount = amount
      withdraw_description = f"Transfer to {cls.category}"
      self.withdraw(withdraw_amount, withdraw_description)
  
      deposit_amount = amount
      deposit_description = f"Transfer from {self.category}"
      cls.deposit(deposit_amount, deposit_description)
      return True
      
    return False

  def check_funds(self, amount):
    if amount > self.balance:
      return False
    else:
      return True

def create_spend_chart(categories):
  withdraws = dict()
  total = 0
  for category in categories:
    withdraw = 0;
    for ledger in category.ledger:
      if ledger['amount'] < 0:
        withdraw += -ledger['amount']
    total += withdraw
    withdraws[category.category] = withdraw
  
  chart = []
  max_key_len = 0
  for key in withdraws:
    percent = withdraws[key] / total * 100
    percent = round(int(percent - (percent % 10)), -1)
    withdraws[key] = percent
    max_key_len = max(max_key_len, len(key))
  
  i = 0
  spaces = " " * 4
  dash = "-" * (len(withdraws) * 3)
  output = f"{spaces}-{dash}"
  while i <= 100:
    line = ""
    for value in withdraws.values():
      if value >= i:
        line = line + 'o  '
      else:
        line = line + '   '
    
    line = f"{i : >3}| {line}\n"
    output = line + output
    i += 10
    
  output = output + "\n"
  i = 0
  while i < max_key_len:
    line = ""
    for key in withdraws.keys():
      if i < len(key):
        line = line + key[i] + '  '
      else:
        line = line + '   '
    
    line = f"{spaces} {line}"
    output = output + line
    i += 1
    if i != max_key_len:
      output += "\n"

  output = "Percentage spent by category\n" + output
  return output