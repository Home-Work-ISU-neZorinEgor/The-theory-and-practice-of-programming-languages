import struct
from enum import Enum
import json


class Alignment(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Widget():
    def add_child(self, children: "Widget"):
        if children not in self.childrens:
            self.childrens.append(children)

    def __init__(self, parent):
        self.parent = parent
        self.childrens = []

        if self.parent is not None:
            self.parent.add_child(self)

    def to_binary(self):
        class_name = self.__class__.__name__.encode()
        result = struct.pack("i", len(class_name)) + class_name

        if isinstance(self, Layout):
            alignment_value = self.alignment.value
            result += struct.pack("i", alignment_value)
        elif isinstance(self, LineEdit):
            max_length = self.max_length
            result += struct.pack("i", max_length)
        elif isinstance(self, ComboBox):
            items = [str(item) for item in self.items]
            items_str = ";".join(items).encode()
            result += struct.pack("i", len(items_str)) + items_str
        elif isinstance(self, MainWindow):
            title_str = self.title.encode()
            result += struct.pack("i", len(title_str)) + title_str

        children_data = b"".join([child.to_binary() for child in self.childrens])
        result += struct.pack("i", len(children_data)) + children_data

        return result

    @classmethod
    def from_binary(cls, binary_data, parent=None):
        class_name_length = struct.unpack("i", binary_data[:4])[0]
        current_pos = 4
        class_name = binary_data[current_pos:current_pos + class_name_length].decode()
        current_pos += class_name_length

        property_length = struct.unpack("i", binary_data[current_pos:current_pos + 4])[0]
        current_pos += 4
        property_value = binary_data[current_pos:current_pos + property_length].decode()
        current_pos += property_length

        root_element = None
        if class_name == "MainWindow":
            root_element = cls(property_value)
        elif class_name == "Layout":
            current_pos -= property_length
            root_element = Layout(parent, property_length)
        elif class_name == "LineEdit":
            current_pos -= property_length
            root_element = LineEdit(parent, property_length)
        elif class_name == "ComboBox":
            root_element = ComboBox(parent, property_value)

        children_length = struct.unpack("i", binary_data[current_pos:current_pos + 4])[0]
        current_pos += 4
        children_data = binary_data[current_pos:]

        cursor = 0
        while cursor < children_length:
            child_node, child_cursor = root_element.from_binary(children_data[cursor:], parent=root_element)
            cursor += child_cursor

        return root_element, current_pos + cursor

    def to_json(self):
        widget_dict = {
            "class_name": self.__class__.__name__,
            "children": [child.to_json() for child in self.childrens]
        }

        if isinstance(self, Layout):
            widget_dict["alignment"] = self.alignment.name
        elif isinstance(self, LineEdit):
            widget_dict["max_length"] = self.max_length
        elif isinstance(self, ComboBox):
            widget_dict["items"] = self.items
        elif isinstance(self, MainWindow):
            widget_dict["title"] = self.title

        return widget_dict

    @classmethod
    def from_json(cls, json_data, parent=None):
        class_name = json_data["class_name"]
        root_element = None

        class_constructors = {
            "MainWindow": lambda data: cls(data["title"]),
            "Layout": lambda data: Layout(parent, Alignment[data.get("alignment", "HORIZONTAL")]),
            "LineEdit": lambda data: LineEdit(parent, data.get("max_length", 10)),
            "ComboBox": lambda data: ComboBox(parent, data.get("items", []))
        }

        if class_name in class_constructors:
            root_element = class_constructors[class_name](json_data)

        for child_data in json_data.get("children", []):
            child_node = cls.from_json(child_data, parent=root_element)
            root_element.add_child(child_node)

        return root_element

    def __str__(self):
        return f"{self.__class__.__name__}{self.childrens}"

    def __repr__(self):
        return str(self)


class MainWindow(Widget):

    def __init__(self, title: str):
        super().__init__(None)
        self.title = title


class Layout(Widget):

    def __init__(self, parent, alignment: Alignment):
        super().__init__(parent)
        self.alignment = alignment


class LineEdit(Widget):

    def __init__(self, parent, max_length: int = 10):
        super().__init__(parent)
        self.max_length = max_length


class ComboBox(Widget):

    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items


app = MainWindow("Application")
layout1 = Layout(app, Alignment.HORIZONTAL)
layout2 = Layout(app, Alignment.VERTICAL)

edit1 = LineEdit(layout1, 20)
edit2 = LineEdit(layout1, 30)

box1 = ComboBox(layout2, [1, 2, 3, 4])
box2 = ComboBox(layout2, ["a", "b", "c"])

print(app)

bts = app.to_binary()
print(f"Binary data length {len(bts)}")
print(f"Binary data {bts}")

new_app = MainWindow.from_binary(bts)
print(new_app[0])

app_json = app.to_json()
app_json_str = json.dumps(app_json, indent=2)
print(f"Representation:\n{app_json_str}")

new_app_from_json = MainWindow.from_json(app_json)
print(new_app_from_json)

if str(app) == str(new_app_from_json):
    print("Objects are equal")