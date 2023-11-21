class CdiscElement:
    def __init__(self, name: str, root: bool = False, **attributes):
        """
        :param attributes: Key 是属性名 , Value是对应的SQL查询返回的列
        :param root: 表明是否是根节点
        :type attributes:
        """
        self.name = name
        self.root = root
        self.attributes = attributes
