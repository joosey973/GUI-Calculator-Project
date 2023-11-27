from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QStackedWidget
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import pyqtSignal
from pycbrf import ExchangeRates
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
import pyqtgraph as pg
from PyQt5 import uic
import numpy as np
import datetime
import sqlite3
import mpmath
import sys
import os


default_font_size = 16
default_entry_font_size = 75


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(r"picture/new_calc_icon.png"))
        self.setWindowTitle("Multy Calculator")
        self.stacked_widget = QStackedWidget(self)
        self.window1 = SimpleCalc()
        self.window2 = EngineeringCalc()
        self.window3 = FuncCalc()
        self.window4 = CreateGraph()
        self.window5 = CurrencyConvert()
        self.window6 = Volume()
        self.window7 = Length()
        self.window8 = Temperature()
        self.window9 = Speed()
        self.window10 = Corner()
        self.stacked_widget.addWidget(self.window1)
        self.stacked_widget.addWidget(self.window2)
        self.stacked_widget.addWidget(self.window3)
        self.stacked_widget.addWidget(self.window4)
        self.stacked_widget.addWidget(self.window5)
        self.stacked_widget.addWidget(self.window6)
        self.stacked_widget.addWidget(self.window7)
        self.stacked_widget.addWidget(self.window8)
        self.stacked_widget.addWidget(self.window9)
        self.stacked_widget.addWidget(self.window10)
        self.setCentralWidget(self.stacked_widget)
        self.setFixedSize(self.stacked_widget.currentWidget().width(), self.stacked_widget.currentWidget().height())
        self.current_index = 0
        self.animation = QPropertyAnimation(self.stacked_widget, b'currentIndex', self)
        self.animation.setDuration(0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.show_window()

    def switch_window(self, index):
        if index != self.current_index:
            self.current_index = index
            self.animation.setStartValue(self.stacked_widget.currentIndex())
            self.animation.setEndValue(index)
            self.animation.start()

    def show_window(self):
        self.show()


class EngineeringCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uics/cal2.ui', self)
        self.statusBar().showMessage("Engineering")
        self.engineer_calc = None
        self.simple_calc = None
        self.flag = None
        self.func_calc = None
        self.date_calc = None
        self.eng_calc = None
        self.ans_width = None
        self.digits_group = None
        self.calculator = True
        self.count = 0
        self.start = 0
        self.new_text = "0"
        self.text = ''
        self.counter = 0
        self.zero_del = 0
        self.is_engineering = True
        self.statusbar.showMessage("Engineering")
        self.main_func()

    def main_func(self):
        self.setWindowIcon((QtGui.QIcon("new_calc_icon.png")))
        [i.clicked.connect(self.numbers_in_calc) for i in self.numsButtonsGroup.buttons()]
        [i.clicked.connect(self.simple_signs) for i in self.simpleSignButtonsGroup.buttons()]
        [i.clicked.connect(self.complex_signs) for i in self.complexSignButtonsGroup.buttons()]
        self.eq_btn.clicked.connect(self.response)
        self.del_btn.clicked.connect(self.erase)
        self.clear_btn.clicked.connect(self.full_clear)
        self.dot_btn.clicked.connect(self.dot)
        self.clear_btn.clicked.connect(self.full_clear)
        self.pl_min_btn.clicked.connect(self.pl_min)
        if self.is_engineering:
            self.btn_2nd.setCheckable(True)
            self.flag = True
            [i.clicked.connect(self.con_signs) for i in self.const_btns.buttons()]
            self.btn_2nd.clicked.connect(self.is_pressed)
        self.Simple.triggered.connect(self.other_calculators)
        self.Engineering.triggered.connect(self.other_calculators)
        self.Function_graphs.triggered.connect(self.other_calculators)
        self.Currency.triggered.connect(self.other_calculators)
        self.Volume.triggered.connect(self.other_calculators)
        self.Length.triggered.connect(self.other_calculators)
        self.Temperature.triggered.connect(self.other_calculators)
        self.Speed.triggered.connect(self.other_calculators)
        self.Corner.triggered.connect(self.other_calculators)

    def con_signs(self):
        if "e+" in self.new_text or "j" in self.new_text:
            return
        btn = self.sender()
        if self.new_text[-1] == ".":
            self.new_text = self.new_text[:-1]
            self.ans_space.setText(self.new_text)
        if btn == self.e_num_but:
            if self.new_text == "0":
                self.new_text = "1"
            if self.new_text[-1].isdigit() or self.new_text[-1] == "." or self.new_text[-1] == "π":
                self.new_text += "*е"
            else:
                self.new_text += "е"
            self.calc()
            self.new_text = str(eval(self.new_text))
            self.checker()
            self.resol.setText(self.new_text)
            self.adjusts()
        elif btn == self.pi_btn:
            if self.new_text == "0":
                self.new_text = "1"
            if self.new_text[-1].isdigit() or self.new_text[-1] == "." or self.new_text[-1] == "e":
                self.new_text += "*π"
            else:
                self.new_text += "π"
            self.calc()
            self.new_text = str(eval(self.new_text))
            self.checker()
            self.resol.setText(self.new_text)
            self.adjusts()

    def is_pressed(self):
        if "j" in self.new_text:
            return
        if self.flag and self.btn_2nd.isChecked():
            self.ctg_btn.setText("arcctg")
            self.square_btn.setText("x³")
            self.root_2_btn.setText("∜x")
            self.log_btn.setText("2^x")
            self.ln2_btn.setText("e^x")
            self.sin_btn.setText("arcsin")
            self.cos_btn.setText("arccos")
            self.tg_btn.setText("arctg")
            self.btn_2nd.setStyleSheet(
                'QPushButton{font: 15pt "MS Shell Dlg 2";background-color: #01d1ff;border: 0px;' +
                'border-radius: 35px;border-style: outset;}')
        else:
            self.ctg_btn.setText("ctg")
            self.square_btn.setText("x²")
            self.root_2_btn.setText("√x")
            self.log_btn.setText("log")
            self.ln2_btn.setText("ln(2)")
            self.sin_btn.setText("sin")
            self.cos_btn.setText("cos")
            self.tg_btn.setText("tg")
            self.btn_2nd.setStyleSheet('QPushButton{font: 15pt "MS Shell Dlg 2";background-color:#0f2b50;border: 0px;' +
                                       'border-radius: 35px;border-style: outset; color: rgb(255, 255, 255);}')

    def numbers_in_calc(self):
        if "e" in self.new_text or "j" in self.new_text:
            return
        if self.count == 0 and self.start == 0 and self.zero_del == 0:
            self.new_text = ""
            self.zero_del += 1
            self.adjusts()
        if self.count == 0 and self.start == 0 and self.zero_del != 0:
            self.text = self.sender().text()
            if self.text == "0" and self.counter == 0:
                return
            else:
                self.new_text += self.text
                self.ans_space.setText(self.new_text)
                self.resol.setText(self.new_text)
                self.calc()
                self.counter += 1
                self.adjusts()
        elif self.count == 0 and self.start == 1:
            self.new_text += self.sender().text()
            self.ans_space.setText(str(self.new_text))
            self.resol.setText(self.new_text)
            self.adjusts()
        else:
            text = self.sender().text()
            finder = "".join(list(filter(lambda x: x in ["+", "-", "*", "/"], self.new_text)))
            finder = self.new_text.find(finder)
            if (self.new_text[-1] in ["+", "-", "*", "/"] or self.new_text[finder + 1] != "0"
                    or self.new_text[finder + 1:finder + 3] == "0."):
                self.new_text += text
                self.calc()
                self.resol.setText(f"{self.new_text}")
                self.adjusts()

    def adjusts(self):
        self.adjust_entry_font_size()
        self.adjust_resol_font_size()

    def simple_signs(self):
        if self.is_engineering:
            self.flag = True
            self.btn_2nd.setCheckable(True)
            self.is_pressed()
        if "j" in self.new_text:
            return
        try:
            if self.new_text[-1] == ".":
                self.new_text = self.new_text[:-1]
        except IndexError:
            return
        if self.start == 1:
            self.calc()
            text = self.sender().text()
            text = self.calc(text)
            if self.new_text[-1] in ["+", "*", "/", "-"]:
                self.start = 0
                return
            self.new_text = str(eval(self.new_text))
            self.checker()
            self.ans_space.setText(self.new_text)
            self.resol.setText(self.new_text)
            if self.new_text[-1] != text and self.new_text[-1] not in ["+", "-", "*", "/"]:
                self.new_text += text
                self.calc()
                self.resol.setText(self.new_text)
                self.ans_space.setText(self.new_text[:-1])
                self.start += 1
                self.count += 1
                self.adjusts()
        else:
            if "e" in self.new_text:
                self.ans_space.setText(self.new_text)
                self.new_text += self.sender().text()
                self.calc()
                self.resol.setText(self.new_text)
            else:
                self.calc()
                text = self.sender().text()
                text = self.calc(text)
                if self.new_text[-1] in ["+", "-", "*", "/"]:
                    return
                self.new_text = str(eval(self.new_text))
                self.ans_space.setText(self.new_text)
                self.resol.setText(self.new_text)
                if self.new_text[-1] != text:
                    self.new_text += text
                    self.calc()
                    self.resol.setText(f"{self.new_text}")
                    self.count += 1
                    self.start += 1
                    self.adjusts()

    def for_compl_signs(self):
        self.checker()
        self.ans_space.setText(self.new_text)

    def complex_signs(self):
        btn = self.sender()
        if "j" in self.new_text:
            return
        if btn == self.square_btn and self.square_btn.text() == "x²":
            self.resol.setText(f"({self.new_text})²=")
            self.new_text = str(mpmath.mpf(eval(self.new_text) ** 2))
            if "e" in self.new_text:
                self.ans_space.setText(self.new_text)
            else:
                self.for_compl_signs()
            self.adjusts()
        elif btn == self.root_3_btn:
            self.resol.setText(f"∛({self.new_text})=")
            self.new_text = str(mpmath.root(mpmath.mpf(eval(self.new_text)), 3))
            if "e" in self.new_text:
                self.ans_space.setText(self.new_text)
            else:
                self.for_compl_signs()
            self.adjusts()
        elif btn == self.root_2_btn and self.root_2_btn.text() == "√x":
            self.resol.setText(f"√({self.new_text})=")
            if str(eval(self.new_text)).startswith("-"):
                self.incorrect_input_err()
            else:
                self.new_text = str(mpmath.sqrt(mpmath.mpf(eval(self.new_text))))
                if "e" in self.new_text:
                    self.ans_space.setText(self.new_text)
                    self.adjusts()
                else:
                    self.for_compl_signs()
                    self.adjusts()
        elif btn == self.fact_btn:
            try:
                if str(eval(self.new_text))[1:].isdigit() and str(eval(self.new_text)).startswith("-"):
                    raise ValueError
            except ValueError:
                self.incorrect_input_err()
                return
            except SyntaxError:
                self.new_text = "0"
            if "e" in self.new_text:
                self.overflow_err()
            else:
                self.resol.setText(f"({self.new_text})!=")
                mpmath.mp.dps = 32  # Set the number of decimal places for the result
                text = str(mpmath.factorial(eval(self.new_text)))
                if eval(self.new_text) < 30:
                    self.new_text = text
                    self.checker()
                else:
                    self.new_text = text
                self.ans_space.setText(self.new_text)
                self.adjusts()
        elif btn == self.rev_btn:
            self.resol.setText(f"1/({self.new_text})=")
            if self.new_text == "0":
                self.div_zero_err()
            else:
                self.new_text = str(1 / mpmath.mpf(self.new_text))
                if "e" in self.new_text:
                    self.ans_space.setText(self.new_text)
                else:
                    self.checker()
                self.adjusts()
        elif btn == self.ctg_btn and self.ctg_btn.text() == "ctg":
            self.resol.setText(f"ctg({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                try:
                    self.new_text = str(1 / mpmath.tan(mpmath.radians(eval(self.new_text))))
                except ZeroDivisionError:
                    self.div_zero_err()
                    return
                self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.log_btn and self.log_btn.text() == "log":
            self.resol.setText(f"log({self.new_text})=")
            text = mpmath.log(mpmath.mpf(eval(self.new_text)))
            if eval(self.new_text) > 0:
                self.new_text = str(text)
                self.checker()
            else:
                self.new_text = str(text)
            self.ans_space.setText(self.new_text)
            self.adjusts()
        elif btn == self.ln2_btn and self.ln2_btn.text() == "ln(2)":
            self.resol.setText(f"ln(2)({self.new_text})=")
            try:
                self.new_text = str(eval(self.new_text))
                self.checker()
                if eval(self.new_text) < 0:
                    raise TypeError
                if eval(self.new_text) > 99999:
                    raise OverflowError
                self.new_text = str(mpmath.ln2(eval(self.new_text)))
            except TypeError:
                self.resol.setText(f"log({self.new_text})=")
                self.ans_space.setText("Нельзя вычислить двоичный логарифм для нецелого или неотрицательного числа")
                self.adjusts()
                self.stop(False)
                return
            except OverflowError:
                self.resol.setText(f"log({self.new_text})=")
                self.ans_space.setText("Нельзя вычислить двоичный логарифм для такого большого числа")
                self.adjusts()
                self.stop(False)
                return
            self.ans_space.setText(self.new_text)
            self.adjusts()
        elif btn == self.ln2_btn and self.ln2_btn.text() == "e^x":
            self.resol.setText(f"e^({self.new_text})=")
            self.new_text = str(mpmath.power(mpmath.e, eval(self.new_text)))
            if "".join(set(self.new_text[self.new_text.find(".") + 1:])) == "0":
                self.new_text = str(int(float(self.new_text)))
            self.ans_space.setText(self.new_text)
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.log_btn and self.log_btn.text() == "2^x":
            self.resol.setText(f"2^({self.new_text})=")
            self.new_text = str(mpmath.power(2, eval(self.new_text)))
            self.ans_space.setText(self.new_text)
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.ctg_btn and self.ctg_btn.text() == "arcctg":
            self.resol.setText(f"arcctg({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.degrees((mpmath.pi / 2) - mpmath.atan(mpmath.mpf(eval(self.new_text)))))
                if "j" in self.new_text:
                    self.ans_space.setText(self.new_text)
                    self.adjusts()
                    return
                if round(float(eval(self.new_text))) in [30, 45, 90, 150, 120, 60, 135]:
                    self.ans_space.setText(str(round(float(self.new_text))))
                else:
                    self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.root_2_btn and self.root_2_btn.text() == "∜x":
            self.resol.setText(f"∜({self.new_text})=")
            if str(eval(self.new_text)).startswith("-"):
                self.incorrect_input_err()
            else:
                self.new_text = str(mpmath.root(mpmath.mpf(eval(self.new_text)), 4))
                if "e" in self.new_text:
                    self.ans_space.setText(self.new_text)
                    self.adjusts()
                else:
                    self.for_compl_signs()
                    self.adjusts()
                self.is_pressed_unpressed()
        elif btn == self.square_btn and self.square_btn.text() == "x³":
            self.resol.setText(f"({self.new_text})³=")
            self.new_text = str(mpmath.mpf(eval(self.new_text)) ** 3)
            if "e+" in self.new_text:
                self.overflow_err()
            else:
                self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.sin_btn and self.sin_btn.text() == "sin":
            self.resol.setText(f"sin({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.sin(mpmath.radians(eval(self.new_text))))
                self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.cos_btn and self.cos_btn.text() == "cos":
            self.resol.setText(f"cos({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.cos(mpmath.radians(mpmath.mpf(eval(self.new_text)))))
                self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.tg_btn and self.tg_btn.text() == "tg":
            self.resol.setText(f"tg({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.tan(mpmath.radians(mpmath.mpf(eval(self.new_text)))))
                self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.sin_btn and self.sin_btn.text() == "arcsin":
            self.resol.setText(f"arcsin({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.degrees(mpmath.asin(mpmath.mpf(eval(self.new_text)))))
                if "j" in self.new_text:
                    self.ans_space.setText(self.new_text)
                    self.adjusts()
                    return
                if round(float(eval(self.new_text))) in [30, 45, 90, 150, 120, 60, 135]:
                    self.ans_space.setText(str(round(float(self.new_text))))
                else:
                    self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.cos_btn and self.cos_btn.text() == "arccos":
            self.resol.setText(f"arccos({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.degrees(mpmath.acos(mpmath.mpf(eval(self.new_text)))))
                if "j" in self.new_text:
                    self.ans_space.setText(self.new_text)
                    self.adjusts()
                    self.adjust_resol_font_size()
                    return
                if round(float(eval(self.new_text))) in [30, 45, 90, 150, 120, 60, 135]:
                    self.ans_space.setText(str(round(float(self.new_text))))
                else:
                    self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.tg_btn and self.tg_btn.text() == "arctg":
            self.resol.setText(f"arctg({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.degrees(mpmath.atan(mpmath.mpf(eval(self.new_text)))))
                if "j" in self.new_text:
                    self.ans_space.setText(self.new_text)
                    self.adjusts()
                    return
                if round(float(eval(self.new_text))) in [30, 45, 90, 150, 120, 60, 135]:
                    self.ans_space.setText(str(round(float(self.new_text))))
                else:
                    self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.sec_btn:
            self.resol.setText(f"sec({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                self.new_text = str(mpmath.sec(mpmath.radians(mpmath.mpf(eval(self.new_text)))))
                self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.module_btn:
            self.resol.setText(f"|{self.new_text}|=")
            self.new_text = str(mpmath.mpf(abs(mpmath.mpf(eval(self.new_text)))))
            self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()
        elif btn == self.csc_btn:
            self.resol.setText(f"csc({self.new_text})=")
            if "e+" in self.new_text:
                self.cannnot_do_this_operation()
            else:
                try:
                    self.new_text = str(mpmath.csc(mpmath.radians(mpmath.mpf(eval(self.new_text)))))
                except ZeroDivisionError:
                    self.div_zero_err()
                    return
                self.for_compl_signs()
            self.adjusts()
            self.is_pressed_unpressed()

    def is_pressed_unpressed(self):
        if self.is_engineering:
            self.flag = False
            self.btn_2nd.setCheckable(False)
            self.is_pressed()
            self.flag = True
            self.btn_2nd.setCheckable(True)

    def div_zero_err(self):
        self.ans_space.setText("Деление на ноль невозможно")
        self.adjusts()
        self.stop(False)

    def incorrect_input_err(self):
        self.stop(False)
        self.ans_space.setText("Неверный ввод")
        self.adjusts()

    def overflow_err(self):
        self.ans_space.setText("Переполнение")
        self.adjusts()
        self.stop(False)

    def cannnot_do_this_operation(self):
        self.ans_space.setText("Невозможно вычислить")
        self.adjusts()
        self.stop(False)

    def calc(self, text=''):
        if '^' in self.new_text or '^' in text:
            self.new_text = self.new_text.replace("^", "**")
            text = text.replace("^", "**")
        if "×" in self.new_text or '×' in text:
            self.new_text = self.new_text.replace("X", "*")
            text = text.replace("×", "*")
        if "÷" in self.new_text or '÷' in text:
            self.new_text = self.new_text.replace("÷", "/")
            text = text.replace("÷", "/")
        if "е" in self.new_text or "е" in text:
            self.new_text = self.new_text.replace("е", str(mpmath.e))
            text = text.replace("е", "*" + str(mpmath.e))
        if "π" in self.new_text or "π" in text:
            self.new_text = self.new_text.replace("π", str(mpmath.pi))
            text = text.replace("π", str(mpmath.pi))
        return text

    def e_and_j(self):
        self.new_text = str(self.new_text)
        self.ans_space.setText(self.new_text)
        self.adjusts()

    def response(self):
        self.resol.setText(f"{self.new_text}=")
        self.adjust_resol_font_size()
        self.calc()
        if "j" in self.new_text or "e" in self.new_text:
            self.e_and_j()
            return
        try:
            self.new_text = str(eval(self.new_text))
        except ZeroDivisionError:
            self.div_zero_err()
            return
        if "e" in self.new_text or "j" in self.new_text:
            self.e_and_j()
            return
        self.checker()
        self.adjusts()
        self.count = 0
        self.start = 0

    # Start rezise text
    def get_entry_text_width(self) -> int:
        return self.ans_space.fontMetrics().boundingRect(self.ans_space.text()).width()

    def get_resol_text_width(self) -> int:
        return self.resol.fontMetrics().boundingRect(self.resol.text()).width()

    def adjust_entry_font_size(self) -> None:
        font_size = default_entry_font_size
        while self.get_entry_text_width() > self.ans_space.width() - 25:
            font_size -= 1
            self.ans_space.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                         f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")
        font_size = 1
        while self.get_entry_text_width() < self.ans_space.width() - 60:
            font_size += 1
            if font_size > default_entry_font_size:
                break
            self.ans_space.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                         f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")

    def adjust_resol_font_size(self) -> None:
        if self.is_engineering:
            font_size = default_entry_font_size
            while self.get_resol_text_width() > self.resol.width() - 25:
                font_size -= 1
                if self.is_engineering:
                    self.resol.setStyleSheet("QLabel{border: 1px solid black; color: rgb(255, 255, 255);" +
                                             f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")
            font_size = 1
            while self.get_resol_text_width() < self.resol.width() - 60:
                font_size += 1
                if font_size > default_font_size:
                    break
                self.resol.setStyleSheet("QLabel{border: 1px solid black; color: rgb(255, 255, 255);" +
                                         f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold';}")

    # Stop rezise text *
    # * These four functions we use to resize our text in QLineEdit and QLabel

    def resizeEvent(self, event):
        self.adjusts()

    def erase(self):  # function to clear one or more signs or digits in number (in QLineEdit)
        sign = 0
        for i in ["-", "*", "/", "+"]:
            if i in self.new_text:
                sign = self.new_text.find(i)
                break
        if self.ans_space.text() != "" or self.ans_space.text() != "0":  # if text in QLineEdit
            # isn't equal empty space or 0 (zero)
            if "e" in self.new_text or "j" in self.new_text:
                return
            if self.new_text[:sign] == self.new_text[-1]:
                self.start = 0
                self.count = 0
                self.counter = 0
            self.new_text = self.new_text[:-1]  # chop number (kinda if we have 1.23, and we chop it once we'll get 1.2)
            if self.new_text == "" or self.new_text == "0":  # if the text still became equal "" we use mini_clear
                self.mini_clear()
                return
            elif sign != 0:
                self.ans_space.setText(self.new_text[:sign])
                self.resol.setText(self.new_text)
                self.adjust_resol_font_size()
            else:
                self.ans_space.setText(self.new_text)
                self.adjusts()
                self.resol.setText("")
                self.start = 0
                self.count = 0

    def full_clear(self):  # function to make full clear in QLineEdir
        self.stop(True)  # unblock buttons
        self.mini_clear()
        self.adjusts()
        self.is_pressed_unpressed()

    def mini_clear(self):
        self.ans_space.setText("0")
        self.resol.setText("")
        self.new_text = "0"
        self.text = ""
        self.count = 0
        self.zero_del = 0
        self.counter = 0
        self.start = 0

    def dot(self):  # function to add dot to number
        if self.new_text == "":  # if we click zero at first
            self.new_text = "0"
        self.zero_del += 1  # so that we don't do a zero check
        if self.new_text[-1] in '0123456789' and self.new_text[self.new_text.find("".join([i for i in self.new_text if
                                                                                           i in ["+", "-", "*", "/"]]))
                                                               + 1:].count(".") == 0:
            self.new_text += "."
            self.counter += 1
            if self.count == 0:
                self.ans_space.setText(self.new_text)
            self.resol.setText(self.new_text)

    def stop(self, flag=True):  # if the error worked we block or unblock buttons
        c = [self.simpleSignButtonsGroup.buttons(), self.complexSignButtonsGroup.buttons(),
             self.numsButtonsGroup.buttons(), self.const_btns.buttons()]
        [j.setEnabled(flag) for i in c for j in i]
        self.dot_btn.setEnabled(flag)
        self.eq_btn.setEnabled(flag)
        self.pl_min_btn.setEnabled(flag)
        self.del_btn.setEnabled(flag)
        if self.is_engineering:
            self.btn_2nd.setEnabled(flag)

    def pl_min(self):  # if we click +/- button
        if "e" in self.new_text or "j" in self.new_text:
            return
        if self.ans_space.text() == "0":  # if QLineEdit contains only zero, we'll skip this sign
            return
        if (self.new_text.isdigit() or str(-abs(eval(self.new_text))) == self.new_text or
                len(self.new_text) - len(list(filter(lambda x: x not in ["-", "*", "/", "+"], self.new_text))) == 0):
            #  (upper) if all self.new_text is digit
            if self.new_text[0] != "-":  # if QLineEdit contains number without minus ("-"), we add it
                self.resol.setText(f"negate({self.new_text})")
                self.new_text = "-" + self.new_text
                self.checker()
            else:
                self.resol.setText(f"negate({self.new_text})")
                self.new_text = self.new_text[1:]  # if QLineEdit contains number with the minus ("-")
                # we remove it (change it for plus)
                self.checker()  # use this function to check and change float or int numbers
        else:
            sign = ["+", "-", "*", "/"]
            res = ""
            for i in self.new_text[1:]:
                if i in sign:
                    res = i
                    break
            if self.new_text.startswith("-"):
                ind = self.new_text[1:].find(res) + 1
            else:
                ind = self.new_text.find(res)
            text = self.new_text[ind + 1:]
            self.resol.setText(self.new_text[:ind + 1] + f"negate({text})")
            if text[0] != "-":
                text = "-" + self.new_text[ind + 1:]
            else:
                text = self.new_text[1:]
            self.new_text = str(eval(self.new_text[:ind + 1] + text))
            self.checker()
            self.ans_space.setText(self.new_text)

    def checker(self):
        if "".join(set(self.new_text[self.new_text.find(".") + 1:])) == '0':
            self.new_text = str(int(float(self.new_text)))
            self.ans_space.setText(self.new_text)
        elif self.new_text.startswith("-") and self.new_text[1:].isdigit():
            self.ans_space.setText(self.new_text)
        elif self.new_text.isdigit():
            self.ans_space.setText(self.new_text)
        else:
            count = 0
            text = ''
            for i in self.new_text[self.new_text.find(".") + 1:]:
                if i == '0':
                    text += i
                else:
                    if count == 5:
                        break
                    else:
                        text += i
                        count += 1
            if_zero_count = 0
            if text.startswith("0"):
                if_zero_count += 1
            if int(text[-1]) in range(5, 10) and len(text) >= 4:
                text = str(int(text[:-2])) + str(int(text[-2]) + 1)
            if if_zero_count == 0:
                self.new_text = self.new_text[:self.new_text.find(".") + 1] + text
            else:
                self.new_text = self.new_text[:self.new_text.find(".") + 1] + "0" + text
            self.ans_space.setText(self.new_text)

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            self.show()
        elif calc_change == "Currency":
            main_window.switch_window(4)
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            main_window.switch_window(9)


class FuncCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uics/Graph.ui", self)
        self.statusBar().showMessage("Functions")
        self.graphic_button.clicked.connect(self.is_clicked)
        [i.clicked.connect(self.complex_operations) for i in self.complexOperarionButtonsGroup.buttons()]
        self.Simple.triggered.connect(self.other_calculators)
        self.Engineering.triggered.connect(self.other_calculators)
        self.Function_graphs.triggered.connect(self.other_calculators)
        self.Currency.triggered.connect(self.other_calculators)
        self.Volume.triggered.connect(self.other_calculators)
        self.Length.triggered.connect(self.other_calculators)
        self.Temperature.triggered.connect(self.other_calculators)
        self.Speed.triggered.connect(self.other_calculators)
        self.Corner.triggered.connect(self.other_calculators)
        self.build_btn.clicked.connect(self.build)

    def complex_operations(self):
        self.ans_space.setText(self.sender().text())

    def build(self):
        connection = sqlite3.connect('dbs/graphics.db')
        cursor = connection.cursor()
        try:
            cursor.execute('''UPDATE graphics SET which_graphic = ?''', (self.ans_space.text(),))
        except sqlite3.OperationalError:
            cursor.execute('''CREATE TABLE graphics(which_graphic TEXT)''')
            cursor.execute('''INSERT INTO graphics(which_graphic) VALUES(?)''', ("x",))
            cursor.execute('''UPDATE graphics SET which_graphic = ?''', (self.ans_space.text(),))
        connection.commit()
        connection.close()

    @staticmethod
    def is_clicked():
        main_window.stacked_widget.widget(3).is_working()
        main_window.switch_window(3)

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            main_window.switch_window(4)
        elif calc_change == "Function graphs":
            self.show()
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            main_window.switch_window(9)


class CreateGraph(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"uics/create_graph.ui", self)
        self.graphic_button.clicked.connect(self.change_widget)

    def is_working(self):
        self.plot_graph.clear()
        connection = sqlite3.connect('dbs/graphics.db')
        cursor = connection.cursor()
        try:
            graphic = "".join(cursor.execute('''SELECT which_graphic FROM graphics''').fetchone()).strip()
        except sqlite3.OperationalError:
            cursor.execute('''CREATE TABLE graphics(which_graphic TEXT)''')
            cursor.execute('''INSERT INTO graphics(which_graphic) VALUES(?)''', ("x",))
            connection.commit()
            graphic = "".join(cursor.execute('''SELECT which_graphic FROM graphics''').fetchone()).strip()
        if "tg" in graphic:
            graphic = graphic.replace("tg", "tan")
        if "sin" in graphic or "cos" in graphic or "tan" in graphic:
            x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
            y = eval("np." + graphic)
        elif "⁴" in graphic:
            x = [i for i in range(-10, 11)]
            y = [i ** 4 for i in range(-10, 11)]
        elif "²" in graphic:
            x = [i for i in range(-10, 11)]
            y = [i ** 2 for i in range(-10, 11)]
        elif "⁻¹" in graphic:
            x = np.linspace(1, 20, 1000)
            y = 1 / x
            self.plot_graph.plot(x, y)
            self.plot_graph.plot(-x, -y)
            return
        elif "³" in graphic:
            x = [i for i in range(-10, 11)]
            y = [i ** 3 for i in range(-10, 11)]
        else:
            x = [i for i in range(-10, 11)]
            y = [i for i in range(-10, 11)]
        self.plot_graph.plot(x, y)

    @staticmethod
    def change_widget():
        main_window.switch_window(2)


class SimpleCalc(EngineeringCalc, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"uics/full_calc.ui", self)
        self.resize(self.width(), self.height())
        self.statusBar().showMessage("Simple")
        self.is_engineering = False
        super().main_func()

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            self.show()
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            main_window.switch_window(4)  # Because third is graphic
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            main_window.switch_window(9)


class Volume(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uics/Volume.ui", self)
        self.statusBar().showMessage("Volume")
        self.text_in_ans = ''
        self.values = ['Миллилитров', 'Литров', 'Кубических метров', 'Кубических километров']
        self.main_func()

    def main_func(self):
        [i.clicked.connect(self.nums) for i in self.numsButtonsGroup.buttons()]
        self.del_btn.clicked.connect(self.delete)
        self.clear_btn.clicked.connect(self.full_clear)
        self.dot_btn.clicked.connect(self.dot)
        self.comboBox_3.currentTextChanged.connect(self.changer)
        self.comboBox_4.currentTextChanged.connect(self.changer)
        self.Simple.triggered.connect(self.other_calculators)
        self.Engineering.triggered.connect(self.other_calculators)
        self.Function_graphs.triggered.connect(self.other_calculators)
        self.Currency.triggered.connect(self.other_calculators)
        self.Volume.triggered.connect(self.other_calculators)
        self.Length.triggered.connect(self.other_calculators)
        self.Temperature.triggered.connect(self.other_calculators)
        self.Speed.triggered.connect(self.other_calculators)
        self.Corner.triggered.connect(self.other_calculators)

    def dot(self):
        if self.text_in_ans[-1] in '0123456789' and self.text_in_ans[self.text_in_ans.find("".join(
                [i for i in self.text_in_ans if
                 i in ["+", "-", "*", "/"]]))
                                                                     + 1:].count(".") == 0:
            self.text_in_ans += "."
            self.ans_space.setText(self.text_in_ans)
            self.changer()

    def changer(self):
        self.convert()
        self.adjust_entry_font_size()
        self.adjust_entry_font_size2()

    def nums(self):
        text = self.sender().text()
        if self.text_in_ans == "0" and text != "0":
            self.text_in_ans = text
            self.ans_space.setText(self.text_in_ans)
            self.adjust_entry_font_size()
            self.changer()
            return
        if self.text_in_ans == "0" and text == "0":
            return
        else:
            self.text_in_ans += text
            self.ans_space.setText(self.text_in_ans)
            self.adjust_entry_font_size()
            self.convert()

    def rounder(self, text):
        if "".join(set(text[text.find(".") + 1:])) == '0':
            text = str(int(float(text)))
        elif text.startswith("-") and text[1:].isdigit():
            pass
        elif text.isdigit():
            pass
        else:
            count = 0
            text1 = ''
            for i in text[text.find(".") + 1:]:
                if i == '0':
                    text1 += i
                else:
                    if count == 5:
                        break
                    else:
                        text1 += i
                        count += 1
            if_zero_count = 0

            if text1.startswith("0"):
                if_zero_count += 1
            try:
                if int(text1[-1]) in range(5, 10) and len(text1) >= 4:
                    text1 = str(int(text1[:-2])) + str(int(text1[-2]) + 1)
            except IndexError:
                self.ans_space2.setText(self.text_in_ans)
                return
            if if_zero_count == 0:
                text = text[:text.find(".") + 1] + text1
        return text

    def convert(self):
        from_val = self.comboBox_3.currentText()
        to_val = self.comboBox_4.currentText()
        text = ''
        if from_val == to_val:
            self.ans_space2.setText(self.ans_space.text())
            self.adjust_entry_font_size2()
            return
        elif self.values.index(from_val) > self.values.index(to_val):
            if self.text_in_ans == "":
                self.text_in_ans = "0"
            if from_val == "Кубических километров":
                if to_val == "Кубических метров":
                    text = str(eval(self.text_in_ans) * 10 ** 9)
                elif to_val == "Литров":
                    text = str(eval(self.text_in_ans) * 10 ** 12)
                elif to_val == "Миллилитров":
                    text = str(eval(self.text_in_ans) * 10 ** 15)
            else:
                text = str(eval(self.text_in_ans) * (10 ** (self.values.index(from_val) - self.values.index(to_val)))
                           ** 3)
        else:
            if self.text_in_ans == "":
                self.text_in_ans = "0"
            if to_val == "Кубических километров":
                if from_val == "Кубических метров":
                    text = str(eval(self.text_in_ans) * 10 ** -9)
                elif from_val == "Литров":
                    text = str(eval(self.text_in_ans) * 10 ** -12)
                elif from_val == "Миллилитров":
                    text = str(eval(self.text_in_ans) * 10 ** -15)
            else:
                text = str(eval(self.text_in_ans) * 10 ** (-3 * (self.values.index(to_val)
                                                                 - self.values.index(from_val))))
        if "e" not in text:
            text = self.rounder(text)
        self.ans_space2.setText(text)
        self.adjust_entry_font_size2()

    def adjust_entry_font_size(self) -> None:
        font_size = default_entry_font_size
        while self.get_entry_text_width() > self.ans_space.width() - 25:
            font_size -= 1
            self.ans_space.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                         f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")
        font_size = 1
        while self.get_entry_text_width() < self.ans_space.width() - 60:
            font_size += 1
            if font_size > default_entry_font_size:
                break
            self.ans_space.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                         f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")

    def adjust_entry_font_size2(self) -> None:
        font_size = default_entry_font_size
        while self.get_entry_text_width2() > self.ans_space.width() - 25:
            font_size -= 1
            self.ans_space2.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                          f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")
        font_size = 1
        while self.get_entry_text_width2() < self.ans_space.width() - 60:
            font_size += 1
            if font_size > default_entry_font_size:
                break
            self.ans_space2.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                          f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")

    def resizeEvent(self, event):
        self.adjust_entry_font_size()
        self.adjust_entry_font_size2()

    def get_entry_text_width(self) -> int:
        return self.ans_space.fontMetrics().boundingRect(self.ans_space.text()).width()

    def get_entry_text_width2(self) -> int:
        return self.ans_space2.fontMetrics().boundingRect(self.ans_space2.text()).width()

    def delete(self):
        if len(self.text_in_ans) <= 1:
            self.text_in_ans = ""
            self.ans_space.setText("0")
            self.ans_space2.setText("0")
            self.adjust_entry_font_size()
            self.adjust_entry_font_size2()
            return
        else:
            self.text_in_ans = self.text_in_ans[:-1]
            self.ans_space.setText(self.text_in_ans)
            self.convert()
            self.adjust_entry_font_size()
            self.adjust_entry_font_size2()

    def full_clear(self):
        self.ans_space.setText("0")
        self.ans_space2.setText("0")
        self.text_in_ans = ""
        self.adjust_entry_font_size()
        self.adjust_entry_font_size2()

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            main_window.switch_window(4)  # Because third is graphic
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            self.show()
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            main_window.switch_window(9)


class CurrencyConvert(Volume, QMainWindow):
    def __init__(self):
        super().__init__()
        if not os.path.exists("dbs"):
            os.mkdir("dbs")
        uic.loadUi("uics/Currency_Widget.ui", self)
        self.is_engineering = False
        self.currency_dict = dict()
        self.upgrade_currency_btn.clicked.connect(self.get_currency_price)
        self.fill_table_count = 0
        self.fill_table()
        super().main_func()

    def convert(self):
        from_val = self.comboBox_3.currentText()
        to_val = self.comboBox_4.currentText()
        if self.text_in_ans == "":
            self.text_in_ans = "0"
            return
        if from_val == to_val:
            self.ans_space2.setText(self.text_in_ans)
            self.adjust_entry_font_size2()
            return
        else:
            try:
                val = eval(self.text_in_ans) * eval(self.currency_dict[from_val.split("-")[0]])
            except KeyError:
                val = '0'
            val = self.rounder(str(val))
            self.ans_space2.setText(val)
            self.adjust_entry_font_size2()

    def adjust_entry_font_size2(self) -> None:
        font_size = default_entry_font_size
        while self.get_entry_text_width2() > self.ans_space.width() - 25:
            font_size -= 1
            self.ans_space2.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                          f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")
        font_size = 1
        while self.get_entry_text_width2() < self.ans_space.width() - 60:
            font_size += 1
            if font_size > default_entry_font_size:
                break
            self.ans_space2.setStyleSheet("QLineEdit{border: 1px solid black; color: rgb(255, 255, 255);" +
                                          f"font: 75 {font_size}pt" + "'Yu Gothic UI Semibold'; }")

    def get_entry_text_width2(self) -> int:
        return self.ans_space2.fontMetrics().boundingRect(self.ans_space2.text()).width()

    def adjust_resol_font_size(self):
        return

    def fill_table(self):
        self.currency_dict = dict()
        connection_to_db = sqlite3.connect('dbs/countries.db')
        cursor = connection_to_db.cursor()
        try:
            currency_values = cursor.execute('''SELECT country_name, value, currency FROM currency_info''').fetchall()
        except sqlite3.OperationalError:
            self.value_parser()
            currency_values = cursor.execute('''SELECT country_name, value, currency FROM currency_info''').fetchall()
        if self.fill_table_count == 1:
            self.comboBox_3.clear()
            self.fill_table_count = 0
        for i in currency_values:
            self.currency_dict[i[0]] = i[-1]
            self.comboBox_3.addItem("-".join(i[:-2]))
        self.fill_table_count += 1
        self.comboBox_4.addItem("Российский рубль-RUB")

    def get_currency_price(self):
        connection_to_db = sqlite3.connect('dbs/countries.db')
        cursor = connection_to_db.cursor()
        rates = ExchangeRates(str(datetime.datetime.now())[:10]).rates
        for db_id, choose_rate in enumerate(rates, start=1):
            cursor.execute('''UPDATE currency_info SET id = ?, country_name = ?, value = ?, currency = ? WHERE
            id = ?''',
                           (db_id, choose_rate.name, choose_rate.code, str(choose_rate.rate), db_id))
            connection_to_db.commit()
        connection_to_db.close()
        self.fill_table()

    @staticmethod
    def value_parser():
        connection = sqlite3.connect(r"dbs/countries.db")
        curs = connection.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS currency_info (id TEXT, country_name TEXT,
        value TEXT, currency TEXT)''')
        connection.commit()
        rates = ExchangeRates(str(datetime.datetime.now())[:10]).rates
        for db_id, vals in enumerate(rates, start=1):
            curs.execute(f'''INSERT INTO currency_info(id, country_name, value, currency)
                            VALUES(?, ?, ?, ?)''', (db_id, vals.name, vals.code,
                                                    str(vals.rate)))
            connection.commit()

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            self.show()
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            main_window.switch_window(9)


class Length(Volume, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uics/Length.ui", self)
        self.statusBar().showMessage("Length")
        self.values = ['Миллиметров', 'Сантиметров', 'Дециметров', 'Метров', 'Километров']
        self.main_func()

    def convert(self):
        from_val = self.comboBox_3.currentText()
        to_val = self.comboBox_4.currentText()
        text = ''
        if from_val == to_val:
            self.ans_space2.setText(self.text_in_ans)
            self.adjust_entry_font_size2()
            return
        elif self.values.index(from_val) > self.values.index(to_val):
            if self.text_in_ans == "":
                self.text_in_ans = "0"
            if from_val == "Километров":
                if to_val == "Метров":
                    text = str(eval(self.text_in_ans) * 1000)
                elif to_val == "Дециметров":
                    text = str(eval(self.text_in_ans) * 10000)
                elif to_val == "Сантиметров":
                    text = str(eval(self.text_in_ans) * 100000)
                elif to_val == "Миллиметров":
                    text = str(eval(self.text_in_ans) * 1000000)
            else:
                text = str(eval(self.text_in_ans) * 10 ** (self.values.index(from_val) - self.values.index(to_val)))
        else:
            if self.text_in_ans == "":
                self.text_in_ans = "0"
            if to_val == "Километров":
                if from_val == "Метров":
                    text = str(eval(self.text_in_ans) * 1000 ** -1)
                elif from_val == "Дециметров":
                    text = str(eval(self.text_in_ans) * 10000 ** -1)
                elif from_val == "Сантиметров":
                    text = str(eval(self.text_in_ans) * 100000 ** -1)
                elif from_val == "Миллиметров":
                    text = str(eval(self.text_in_ans) * 1000000 ** -1)
            else:
                text = str(eval(self.text_in_ans) * 10 ** ((self.values.index(to_val) - self.values.index(from_val))
                                                           * -1))
        if "e" not in text:
            text = self.rounder(text)
        self.ans_space2.setText(text)
        self.adjust_entry_font_size2()

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            main_window.switch_window(4)  # Because third is graphic
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            self.show()
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            main_window.switch_window(9)


class Temperature(Volume, QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_engineering = False
        uic.loadUi("uics/Temperature.ui", self)
        self.statusBar().showMessage("Temperature")
        self.temperature_dict = self.temperature_dict = {
                                    "шкала Цельсия": {"шкала Фаренгейта": "t * 1.8 + 32", "шкала Кельвина": "t+273.15"},
                                    "шкала Фаренгейта": {
                                        "шкала Цельсия": "(t - 32) / 1.8",
                                        "шкала Кельвина": "(t + 459.67)/1.8",
                                    },
                                    "шкала Кельвина": {
                                        "шкала Фаренгейта": "1.8 * t - 459.67",
                                        "шкала Цельсия": "t - 273.15",
                                    },
                                }
        self.pl_min_btn.clicked.connect(self.plus_minus)
        self.main_func()

    def convert(self):
        from_val = self.comboBox_3.currentText()
        to_val = self.comboBox_4.currentText()
        if self.text_in_ans == "":
            self.text_in_ans = "0"
        if from_val == to_val:
            self.ans_space2.setText(self.ans_space.text())
            self.adjust_entry_font_size2()
            return
        else:
            t = str(eval(self.temperature_dict[from_val][to_val].replace("t", str(float(self.text_in_ans)))))
            self.ans_space2.setText(t)
            self.adjust_entry_font_size2()
            return

    def plus_minus(self):
        if self.text_in_ans and self.text_in_ans != "0":
            self.text_in_ans = "-" + self.text_in_ans if "-" not in self.text_in_ans else self.text_in_ans[1:]
            self.ans_space.setText(self.text_in_ans)
            self.adjust_entry_font_size()
            self.convert()

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            main_window.switch_window(4)  # Because third is graphic
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            self.show()
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            main_window.switch_window(9)


class Speed(Temperature, QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_engineering = False
        uic.loadUi("uics/Speed.ui", self)
        self.statusBar().showMessage("Speed")
        self.speed_dict = {"Сантиметры в секунду": {"Метров в секунду": "speed * 0.01",
                                                    "Километров в час": "speed * (0.00001 * 3600)"},
                           "Метров в секунду": {"Сантиметры в секунду": "speed * 100",
                                                "Километров в час": "speed * 3.6"},
                           "Километров в час": {"Сантиметры в секунду": "speed * (100000/3600)",
                                                "Метров в секунду": "speed * (1000 / 3600)"}}
        self.pl_min_btn.clicked.connect(self.plus_minus)
        self.main_func()

    def convert(self):
        from_val = self.comboBox_3.currentText()
        to_val = self.comboBox_4.currentText()
        if self.text_in_ans == "":
            self.text_in_ans = "0"
        if from_val == to_val:
            self.ans_space2.setText(self.text_in_ans)
            self.adjust_entry_font_size2()
            return
        else:
            t = str(eval(self.speed_dict[from_val][to_val].replace("speed", str(float(self.text_in_ans)))))
            self.ans_space2.setText(self.rounder(t))
            self.adjust_entry_font_size2()
            return

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            main_window.switch_window(4)  # Because third is graphic
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            self.show()
        elif calc_change == "Corner":
            main_window.switch_window(9)


class Corner(Temperature, QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_engineering = False
        uic.loadUi("uics/Corner.ui", self)
        self.statusBar().showMessage("Corner")
        self.pl_min_btn.clicked.connect(self.plus_minus)
        self.main_func()

    def convert(self):
        from_val = self.comboBox_3.currentText()
        to_val = self.comboBox_4.currentText()
        if self.text_in_ans == "":
            self.text_in_ans = "0"
        if from_val == to_val:
            self.ans_space2.setText(self.ans_space.text())
            self.adjust_entry_font_size2()
            return
        elif from_val == "Градусы":
            self.ans_space2.setText(str(self.rounder(str(mpmath.radians(eval(self.text_in_ans))))))
            self.adjust_entry_font_size2()
        else:
            self.ans_space2.setText(str(self.rounder(str(mpmath.degrees(eval(self.text_in_ans))))))
            self.adjust_entry_font_size2()

    def other_calculators(self):
        calc_change = self.sender().text().rstrip()
        if calc_change == "Simple":
            main_window.switch_window(0)
        elif calc_change == "Engineering":
            main_window.switch_window(1)
        elif calc_change == "Currency":
            main_window.switch_window(4)  # Because third is graphic
        elif calc_change == "Function graphs":
            main_window.switch_window(2)
        elif calc_change == "Volume":
            main_window.switch_window(5)
        elif calc_change == "Length":
            main_window.switch_window(6)
        elif calc_change == "Temperature":
            main_window.switch_window(7)
        elif calc_change == "Speed":
            main_window.switch_window(8)
        elif calc_change == "Corner":
            self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
