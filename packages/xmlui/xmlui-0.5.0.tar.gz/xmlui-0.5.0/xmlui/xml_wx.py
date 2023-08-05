#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from . import xml_ui_tool

def get_all_handle_class():
    return {k:v for k,v in globals().items() if type(v)==type or type(v).__name__=="classobj"}

class HandleCommonTag(xml_ui_tool.HandleTagBase):
    def handle_self(self):
        iscallfunc = self.check_call_func()
        if iscallfunc:
            return

        # self.custom = self.create_custom()
        # if self.custom:
        #     self.apply_all_attrs()
        #     return

        self.ui = self.create_ui()
        if self.ui:
            self.apply_all_attrs()
            return

    # 优先假设xml_element.tag是一个可执行函数
    def check_call_func(self):
        func = getattr(self.parent, self.xml_element.tag, None)
        if not func:
            func = getattr(self, self.xml_element.tag, None)
        if not func and self.parent:
            func = getattr(self.parent.get_result(), self.xml_element.tag, None)

        if not callable(func):
            return False

        if not self.xml_element.text or not self.xml_element.text.strip():
            func()
        else:
            func(xml_ui_tool.convert_attr_value(self.xml_element.text, {"wx":wx}))

        return True

    # 尝试创建ui节点
    def create_ui(self):
        wxClass = getattr(wx, self.xml_element.tag, None)
        if not wxClass:
            return None
        
        args = {}
        self.pick_constructor_arg(args, "label")
        self.pick_constructor_arg(args, "size")
        
        ui = wxClass(self.get_latest_ui(), **args)

        return ui

    def apply_all_attrs(self):
        for attrName, attrValue in self.xml_element.items():
            func = getattr(self, "apply_attr_"+attrName, None)
            if func:
                func(xml_ui_tool.convert_attr_value(attrValue, {"wx":wx}))
                continue

            func = getattr(self.get_result(), attrName, None)
            if callable(func):
                func(xml_ui_tool.convert_attr_value(attrValue, {"wx":wx}))

    # def call_simplefunc_at_result(self, funcName, param):
    #     func = getattr(self.get_result(), funcName, None)
    #     if callable(func):
    #         func(param)

    def pick_constructor_arg(self, args, name):
        attr = self.xml_element.get(name)
        if attr and attr.strip():
            args[name] = xml_ui_tool.convert_attr_value(attr, {"wx":wx})

class App(xml_ui_tool.HandleTagBase):
    def __init__(self):
        self.main_frame = None
    def handle_self(self):
        self.custom = wx.App()
    def after_handle_child(self, child_handle_obj):
        if self.main_frame:
            raise Exception("wx只能有一个主界面")

        if child_handle_obj.ui:
            self.main_frame = child_handle_obj.ui
            self.main_frame.Show()

class BoxSizer(xml_ui_tool.HandleTagBase):
    def handle_self(self):
        self.custom = wx.BoxSizer()

        self.proportion = None
        if self.xml_element.get("proportion", "").strip():
            self.proportion = xml_ui_tool.convert_attr_value(self.xml_element.get("proportion"), {"wx":wx})
        if isinstance(self.proportion, int):
            self.proportion = [self.proportion]

        self.flags = wx.EXPAND
        if self.xml_element.get("flags", None):
            self.flags = xml_ui_tool.convert_attr_value(self.xml_element.get("flags"), {"wx":wx})
        if isinstance(self.flags, int):
            self.flags = [self.flags]

    def after_handle_child(self, child_handle_obj):
        if child_handle_obj.ui:
            prop = self.proportion[len(self.children)-1] if self.proportion and len(self.proportion)>=len(self.children) else 0
            flag = self.flags[len(self.children)-1] if len(self.flags)>=len(self.children) else self.flags[0]
            print "prop", prop, "flag", flag
            self.custom.Add(child_handle_obj.ui, prop, flag)

    def handle_over(self):
        self.parent.ui.SetSizer(self.custom)
        self.custom.Fit(self.parent.ui)

class SplitterWindow(HandleCommonTag):
    def SetSashPosition(self, attrValue):
        p1, p2 = self.ui.GetChildren()
        if self.ui.GetSplitMode()==wx.SPLIT_HORIZONTAL:
            self.ui.SplitHorizontally(p1, p2, attrValue)
        elif self.ui.GetSplitMode()==wx.SPLIT_VERTICAL:
            self.ui.SplitVertically(p1, p2, attrValue)

class Bind(HandleCommonTag):
    def handle_self(self):
        bindtype = xml_ui_tool.convert_attr_value(self.xml_element.get("type"), {"wx":wx})
        bindfunc = getattr(self.controller, self.xml_element.text.strip(), None)
        if bindfunc:
            self.parent.ui.Bind(bindtype, bindfunc, self.parent.ui)
