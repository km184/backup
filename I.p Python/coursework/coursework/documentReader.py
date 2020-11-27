# We've used Multilevel inheritance for dataframe filtering

# This class handle all dataframe related reading process
class documentReader:
    def __init__(self, dfDoc):
        if not dfDoc.empty:
            self.__dfDoc = dfDoc

    def getDocument(self):
        return self.__dfDoc

    def getCountofRows(self):
        return len(self.__dfDoc.index)


# Child Class inheriting Base class
class readWithOneColumn(documentReader):
    def __init__(self, dfDoc, inColumn):
        super().__init__(dfDoc)
        self.__inColumn = inColumn

    def getResponseforOneColumn(self):
        return self.getDocument()[self.__inColumn].value_counts().to_dict()

    def getinColumn(self):
        return self.__inColumn


# Inheriting the child class to include the futher attributes
class readWithMultiColumns(readWithOneColumn):
    def __init__(self, dfDoc, inColumn, UUID, outColumn):
        readWithOneColumn.__init__(self, dfDoc, inColumn)
        self.__UUID = UUID
        self.__outColumn = outColumn

    def getResponseforMultiColumn(self):
        dtReaders = self.getDocument().loc[self.getDocument()[self.getinColumn()] == self.__UUID][self.__outColumn]
        return dtReaders.value_counts().to_dict()


# Inheriting the child class to include the futher attributes with additional filter
class readWithMultiColumnswithRead(readWithOneColumn):
    def __init__(self, dfDoc, inColumn, UUID, outColumn, readFilter, filterColumn):
        readWithOneColumn.__init__(self, dfDoc, inColumn)
        self.__UUID = UUID
        self.__outColumn = outColumn
        self.__readFilter = readFilter
        self.__filterColumn = filterColumn

    def getResponseforMultiColumnRead(self):
        dtReaders = self.getDocument().loc[(self.getDocument()[self.getinColumn()] == self.__UUID) &
                                           (self.getDocument()[self.__filterColumn] == self.__readFilter)][
            [self.__outColumn]]

        return dtReaders
