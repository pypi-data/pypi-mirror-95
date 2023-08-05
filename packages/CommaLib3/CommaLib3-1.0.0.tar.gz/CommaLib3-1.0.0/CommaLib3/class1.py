
class comma():
  
  def COMA(num):
    number_with_commas = "{:,}".format(num)
    return number_with_commas

  def help():
    print("""

Usage:
>>> num = 1000
>>> num_formated = comma.COMA(num)
>>> print(num_formated)

result:
>>> 1,000
""")
