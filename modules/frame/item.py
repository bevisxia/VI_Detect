
class DetectItem(object):
    def __init__(self, id, name, count):
        self.__id = id
        self.__name = name
        self.__count = count

    def get_name(self):
        return self.__name

    def get_count(self):
        return self.__count

    def get_id(self):
        return self.__id

class Item(object):
    def __init__(self,id,name,x,y,score):
        self.__id = id
        self.__name = name
        self.__x = x
        self.__y = y
        self.__score = score

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_score(self):
        return self.__score