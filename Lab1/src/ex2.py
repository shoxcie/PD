print("Общество в начале XXI века\n")

age = int(input("Введите Ваш возраст: "))

if age in range(0, 8):
	print("Вам в детский сад")

elif age in range(7, 18):
	print("Вам в школу")

elif age in range(18, 26):
	print("Вам в профессиональное учебное заведение")

elif age in range(25, 61):
	print("Вам на работу")

elif age in range(60, 121):
	print("Вам предоставляется выбор")

else:
	print("Ошибка! Это программа для людей!")