from design import Window, App
from calc import logic_of_buttom


if __name__ == "__main__":
    app = App()
    w = Window(app, 5, 5)
    w.add_label("Цена S0:", 0, 0)
    w.add_label("Дивидендная доходность q:", 0, 1)
    w.add_label("Цена исполнения K:", 0, 2)
    w.add_label("Барьерный уровень H:", 0, 3)
    w.add_label("Волатильность сигма:", 0, 4)
    w.add_label("Срок исполнения T:", 0, 5)
    w.add_label("Безрисковая ставка r:", 0, 6)
    w.add_label("Тип опциона:", 0, 7, "'call', 'put' или 'all'")
    w.add_label("Тип барьера:", 0, 8,
                "'up-and-out', 'up-and-in', 'down-and-out', 'down-and-in' или 'all'. Можно несколько через ','.")
    w.input(1, 0, 'S0',110)
    w.input(1, 1, "q",0.01)
    w.input(1, 2, "K",100)
    w.input(1, 3, "H",120)
    w.input(1, 4, "sigma",0.25)
    w.input(1, 5, "T",0.25)
    w.input(1, 6, "r",0.03)
    w.input(1, 7, "option_type","call")
    w.input(1, 8, "barrier_type","up-and-out")
    w.add_button(0, 10, "Calculate", logic_of_buttom, w)

    app.mainloop()
