x = int(input("Введите число [1..9]: "))

while x not in range(1, 10):
	x = int(input("Ошибка ввода! Попробуйте ещё раз: "))

if (x < 4):
	s = str(input("Введите строку: "))
	n = int(input("Введите количество повторов: "))
	for i in range(1, n):
		s += s
	print(s)

elif (x < 7):
	m = int(input("Введите степень: "))
	x **= m
	print(x)
	
else:
	for i in range(0, 10):
		x += 1
		print(x)