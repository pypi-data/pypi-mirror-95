# xmlui

* 基于wxPython，用xml描述ui结构，辅助python界面开发的库。
* 环境依赖
  * wxPython 4.1.1

# 安装

```
pip install xmlui
```

# 使用

## 使用xml描述UI结构

```xml
<App controller="MainController">
	<Frame name="main_frame">
		<BoxSizer stretch="1">
			<Button name="ui_mybtn" label="按钮1">
				<Bind type="wx.EVT_BUTTON">OnClickButton</Bind>
			</Button>
		</BoxSizer>
	</Frame>
</App>
```



## 编写代码，显示界面

```python
import sys
sys.path.append("..")

import xmlui
import wx

class MainController(xmlui.Controller):
    def __init__(self):
        self.doc = None

    def after_load(self):
        self.main_frame.Show(True)

    def OnClickButton(self, evt):
        wx.MessageBox(self.ui_mybtn.GetLabel())

def main():
    loader = xmlui.XmlWXLoader()
    controllers = [MainController]
    wxapp = loader.load("simple_wx.xml", controllers)
    wxapp.MainLoop()

if __name__ == '__main__':
    main()
```



更复杂的例子可以参考sample目录下的内容