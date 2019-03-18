from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import math

class CalcInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        allowed = ['1','2','3','4','5','6','7','8','9','0','-','+','/','*','%']
        if not substring in allowed:#If the key is not a valid key
            return super().insert_text('', from_undo=from_undo)
        else:
            return super().insert_text(substring, from_undo=from_undo)
class CalcWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        nums = [7,8,9,4,5,6,1,2,3,'.',0,'%']
        syms = ['-','(','AC','\u00f7',')','mod','\u00d7\u00b2','\u03c0','\u221a']
        syms2 = ['C','\u00d7','+']
        self.numbers = self.ids.numbers
        self.symbols = self.ids.symbols
        self.last_symbols = self.ids.last_symbols

        #Adding the buttons
        for num in nums: 
            btn = Button(text=str(num),background_normal='',background_color=(0.004, 0.055, 0.102, 1.0),font_size=26)
            btn.bind(on_release=self.echo_num)
            self.numbers.add_widget(btn)
        for num in syms: 
            btn = Button(text=str(num),background_normal='',background_color=(0.004, 0.055, 0.102, 1.0),font_size=26)
            btn.bind(on_release=self.echo_num)
            self.symbols.add_widget(btn)
        eq = Button(text='=', size_hint_y=.25,background_color=(0.133, 0.855, 0.431, 1.0),background_normal='',font_size=26)
        eq.bind(on_release=self.evaluate_exp)
        self.ids.symbols_cont.add_widget(eq)
        for num in syms2: 
            btn_height = .25
            if num == '+':
                btn_height = .5
            btn = Button(text=str(num),size_hint_y = btn_height,background_normal='',background_color=(0.004, 0.055, 0.102, 1.0),font_size=26)
            btn.bind(on_release=self.echo_num)
            self.last_symbols.add_widget(btn)

    def echo_num(self, instance):
        query = self.ids.query

        if instance.text == '%' and len(query.text) > 0:
            symbols = []
            symbols.append(query.text.rfind('-'))
            symbols.append(query.text.rfind('+'))
            symbols.append(query.text.rfind('\u00f7'))
            symbols.append(query.text.rfind('\u00d7'))
            sym_ind = max(symbols)#Get the last symbol
            if sym_ind < 0:
                perc = round(float(query.text)/100,2)
                query.text = str(perc)
            else:
                res = query.text
                target = res[sym_ind+1:]
                perc = round(float(target)/100,2)
                query.text = query.text[:sym_ind+1] + str(perc)

        elif instance.text == '\u221a' and len(query.text) > 0:
            symbols = []
            symbols.append(query.text.rfind('-'))
            symbols.append(query.text.rfind('+'))
            symbols.append(query.text.rfind('\u00f7'))
            symbols.append(query.text.rfind('\u00d7'))
            sym_ind = max(symbols)#Get the last symbol
            if sym_ind < 0:
                # perc = round(float(query.text)/100,2)
                sqrt = math.sqrt(float(query.text))
                query.text = str(sqrt)
            else:
                res = query.text
                target = res[sym_ind+1:]
                # perc = round(float(target)/100,2)
                sqrt = math.sqrt(float(target))
                query.text = query.text[:sym_ind+1] + str(sqrt)
        elif instance.text == 'AC':
            query.text = ''
        elif instance.text == 'C':
            query.text = query.text[:-1]
        else:
            query.text += instance.text

    def evaluate_exp(self, text):
        query = self.ids.query
        exp = query.text
        exp = self.resolve_sym(exp)
        res = eval(exp)
        query.text = str(res)
        
        self.ids.expr.text = exp
        self.ids.equal.text = '='
        self.ids.result.text = str(res)

    def resolve_sym(self, text):
        res = text.replace('\u00f7','/').replace('\u00d7\u00b2','**2').replace('\u00d7','*').replace('\u03c0',str(math.pi)).replace('mod','%')
        return res

class CalcApp(App):
    def build(self):

        return CalcWindow()

if __name__=='__main__':
    CalcApp().run()