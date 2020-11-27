from tkinter import *
from tkinter import ttk
from tkinter.font import Font
import constants as const
from tkinter import messagebox
import dataManipulation as dataM
import taskHandler


class DocumentGUI:
    def __init__(self):
        self.dataAnalysis = Tk()

        docFont = Font(family="calibri", size=10, weight="bold")
        # Configure frame
        # self.dataAnalysis.geometry('400x300')
        self.dataAnalysis.title('Document Analysis')
        mainframe = ttk.Frame(self.dataAnalysis, padding="30 30 30 30")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # Text fields
        self.documnetUUID = StringVar()
        self.visitorUUID = StringVar()
        self.fileName = StringVar()
        self.box_value = StringVar()

        lblDocID = Label(mainframe, text="Documnet UUID", font=docFont)
        lblVisitorID = Label(mainframe, text="Visitor UUID", font=docFont)
        lblInputFile = Label(mainframe, text="File Name", font=docFont)

        txtDocID = Entry(mainframe, textvariable=self.documnetUUID)
        txtVisitorID = Entry(mainframe, textvariable=self.visitorUUID)
        txtInputFile = Entry(mainframe, textvariable=self.fileName)

        lblDocID.grid(row=1, sticky=E)
        lblVisitorID.grid(row=2, sticky=E)
        lblInputFile.grid(row=3, sticky=E)

        txtDocID.grid(row=1, column=1, padx=10, sticky=(W, E))
        txtVisitorID.grid(row=2, column=1, padx=10, sticky=(W, E))
        txtInputFile.grid(row=3, column=1, padx=10, sticky=(W, E))

        btnSearch = Button(mainframe, text="Search", command=self.Process, font=docFont)
        cbTasks = ttk.Combobox(mainframe, textvariable=self.box_value, state='readonly', values=const.tasks)
        cbTasks.current(0)

        btnSearch.grid(row=1, column=4, padx=10, sticky=W)
        cbTasks.grid(row=2, column=4, padx=10, sticky=W)

        # self.populateData()

        self.dataAnalysis.mainloop()

    # If we want to load on page load we can use this method
    def populateData(self):
        dataM.loadFromJson()

    def Process(self):
        self.initializeSearch(self.box_value.get())

    def initializeSearch(self, task):
        print(self.fileName.get())
        if len(self.fileName.get()) > 0:
            if len(self.documnetUUID.get()) > 0 or len(self.visitorUUID.get()) > 0 or task in const.tasks[2:4]:
                taskHandler.taskHandler(task, self.fileName.get(), self.documnetUUID.get(), self.visitorUUID.get())
            else:
                messagebox.showinfo("Info", "Input Document ID or  in order to Search in document")
        else:
            messagebox.showinfo("Info", "Input File Name in order to Search")


if __name__ == '__main__':
    gui = DocumentGUI()
