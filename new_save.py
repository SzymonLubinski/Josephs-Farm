import json


class NewSave:
    def __init__(self, save_index, data):
        self.save_index = save_index
        self.data = data
        self.data_list = []

    def save_it(self):
        with open(f'saves/save{self.save_index}', 'w') as file:
            for objects_list in self.data[:4]:
                one_group = []
                for obj in objects_list:
                    content = {'x': obj.x, 'y': obj.y, 'tp': obj.__class__.__name__, 'effigy': obj.effigy}
                    one_group.append(content)
                self.data_list.append(one_group)

            nature_group = []
            for item in self.data[4]:
                nature_item = {'x': item.x, 'y': item.y, 'tp': item.__class__.__name__}
                nature_group.append(nature_item)
            self.data_list.append(nature_group)

            for single_object in self.data[5:]:
                self.data_list.append(single_object)
            json.dump(self.data_list, file)


class LoadSave:
    def __init__(self, load_index):
        self.load_index = load_index
        self.a = None

    def load_it(self):
        with open(f'saves/save{self.load_index}') as file:
            data = json.load(file)
            return data

