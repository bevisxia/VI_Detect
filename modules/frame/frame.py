
class Frame(object):
    def __init__(self, frame_id=None):
        self.__frame_id = frame_id
        self.__items = []

    def set_frame_id(self, id):
        self.__frame_id = id

    def get_frame_id(self):
        return self.__frame_id

    def add_item(self, item):
        self.__items.append(item)

    def get_items(self):
        return self.__items

    def get_item_names(self):
        result = []
        for item in self.__items:
            result.append(item.get_name())
        return list(set(result))

    def get_items_by_id(self, id):
        return [item for item in self.__items if item.get_id() == id]

    def get_items_by_name(self, name):
        return [item for item in self.__items if item.get_name() == name]

