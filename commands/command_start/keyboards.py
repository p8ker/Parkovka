from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class Keyboards():
    def KeyboardYesOrNo():
        kb = [[
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет"),
        ]]
        return kb
    
    def KeyboardTime():
        kb = [[
            types.KeyboardButton(text="30 минут"),
            types.KeyboardButton(text="1 час"),
            types.KeyboardButton(text="2 часа"),
        ]]
        return kb
    
    def KeyboardCancel():
        kb = [[
            types.KeyboardButton(text="Завершить парковку"),
            types.KeyboardButton(text="Показать все места на данный момент")
        ]]
        return kb
    
    def Keyboard1Per4():
        builder = ReplyKeyboardBuilder()
        y = [19, 22, 61, 43]
        
        
        for x in range(len(y)):
            builder.add(types.KeyboardButton(text=str(y[x])))
        builder.add(types.KeyboardButton(text="Показать все места на данный момент"))    
        builder.adjust(4)    
        
        
        return builder
    
    def KeyboardUploadTable():
        kb = [[
            types.KeyboardButton(text="Показать все места на данный момент")
        ]]
        return kb