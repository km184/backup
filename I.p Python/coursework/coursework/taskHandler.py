import constants as const
import dataManipulation as dataM
import documentReader as dataHandler
import plotHist as ref
import pandas as pd
from graphviz import Digraph
from tkinter import messagebox


# This class handles all the tasks related to the course work
class taskHandler:
    def __init__(self, task, file, in_doc_uuid, user_uuid=None):
        self.dReader = dataHandler.documentReader(dataM.loadFromJson(file))
        self.doc_id = in_doc_uuid
        self.user_id = user_uuid
        task_switch = {
            "Task1a": self.viewerByCountry,
            "Task1b": self.viewerByContinent,
            "Task2a": self.viewAllUserAgent,
            "Task2b": self.viewUserBrowser,
            "Task3a": self.viewAlsoLikeDocument,
            "Task3b": self.viewTop10LikelyDocument,
            "Task4a": self.viewAlsoLikesGraph
        }
        try:
            task_switch[task]()
        except Exception as err:
            print(f'Error while paring the user agent: {err}')
            messagebox.showerror('DocumentAnalysis', err)

    # Method support us to find the document viewers by country (for all events)
    def viewerByCountry(self):
        var = dataHandler.readWithMultiColumns(self.dReader.getDocument(), const.Columns.env_doc_id.name,
                                               self.doc_id,
                                               const.Columns.visitor_country.name)
        ref.plotHistogram.show_histo(var.getResponseforMultiColumn(), const.histPos.vert, "Count",
                                     "Country wise distribution", const.histColor.b.name)

    # Method support us to find the document viewers by continent (for all events)
    def viewerByContinent(self):
        var = dataHandler.readWithMultiColumns(self.dReader.getDocument(), const.Columns.env_doc_id.name,
                                               self.doc_id,
                                               const.Columns.continents.name)
        ref.plotHistogram.show_histo(var.getResponseforMultiColumn(), const.histPos.vert, "Count",
                                     "Continent wise distribution", const.histColor.r.name)

    # Method support us to find the viewers user-agent (for all events)
    def viewAllUserAgent(self):
        var = dataHandler.readWithOneColumn(self.dReader.getDocument(), const.Columns.visitor_useragent.name)
        ref.plotHistogram.show_histo(var.getResponseforOneColumn(), const.histPos.vert, "Count",
                                     "User Agent distribution")

    # Method support us to find the viewers browser family name (for all events)
    def viewUserBrowser(self):
        ref.plotHistogram.show_histo(
            dataM.parseUserAgent(self.dReader.getDocument(), const.Columns.visitor_useragent.name),
            const.histPos.horiz, "Count", "Browser distribution")

    # Method support us to find the viewers likely documnet (for read events)
    def viewAlsoLikeDocument(self):
        dfObj = pd.DataFrame(columns=['env_doc_id'])
        visitors = dataHandler.readWithMultiColumnswithRead(self.dReader.getDocument(), const.Columns.env_doc_id.name,
                                                            self.doc_id,
                                                            const.Columns.visitor_uuid.name, 'read',
                                                            const.Columns.event_type.name)
        dfVisitor = visitors.getResponseforMultiColumnRead()
        for visitor in dfVisitor.visitor_uuid.unique():
            if visitor != self.user_id:
                documents = dataHandler.readWithMultiColumnswithRead(self.dReader.getDocument(),
                                                                     const.Columns.visitor_uuid.name, visitor,
                                                                     const.Columns.env_doc_id.name, 'read',
                                                                     const.Columns.event_type.name)
                dfObj = dfObj.append(documents.getResponseforMultiColumnRead())
            else:
                dfObj = dfObj.append(self.dReader.getDocument()[
                                         (self.dReader.getDocument().visitor_uuid == self.user_id) & (
                                                 self.dReader.getDocument()['env_doc_id'] == self.doc_id) & (
                                                 self.dReader.getDocument().event_type == 'read')][['env_doc_id']])

        dfDoc = dfObj.groupby(['env_doc_id']).size().reset_index(name="TimesRead")
        dfLikely = dfDoc.sort_values('TimesRead', ascending=False)
        print(dfLikely)
        return dfLikely

    # Method support us to find top 10 doucments by frequecy of viewers (for read events)
    def viewTop10LikelyDocument(self):
        dfLikely = self.viewAlsoLikeDocument()
        print(dfLikely[:10])

    # Method support us to create graph for the also like functionality (for read events)
    def viewAlsoLikesGraph(self):
        visitors = dataHandler.readWithMultiColumnswithRead(self.dReader.getDocument(), const.Columns.env_doc_id.name,
                                                            self.doc_id, const.Columns.visitor_uuid.name, 'read',
                                                            const.Columns.event_type.name)
        size = dataM.formSize(visitors)

        dot = Digraph(name='The Graph')
        dot.node('Readers', shape='none')
        dot.node('Documents', shape='none')
        dot.edge('Readers', 'Documents', label=('Size: %s' % size))
        dtNew = visitors.getResponseforMultiColumnRead()
        if len(dtNew) > 0:
            for visitor in dtNew.visitor_uuid.unique():
                if visitor == self.user_id:
                    dot.node(str(visitor)[-4:], fillcolor=const.histColor.green.name, style='filled', shape='box')
                else:
                    dot.node(str(visitor)[-4:], shape='box')
                documents = dataHandler.readWithMultiColumnswithRead(self.dReader.getDocument(),
                                                                     const.Columns.visitor_uuid.name, visitor,
                                                                     const.Columns.env_doc_id.name, 'read',
                                                                     const.Columns.event_type.name)
                if visitor == self.user_id:
                    dfDoc = documents.getResponseforMultiColumnRead()
                    dfDoc.drop(dfDoc[dfDoc['env_doc_id'] != self.doc_id].index, inplace=True)
                else:
                    dfDoc = documents.getResponseforMultiColumnRead()
                for document in dfDoc.env_doc_id.unique():
                    if document == self.doc_id:
                        dot.node(str(document)[-4:], fillcolor=const.histColor.green.name, style='filled')
                    else:
                        dot.node(str(document)[-4:])
                    dot.edge(str(visitor)[-4:], str(document)[-4:])

        dot.render('graph-output/document-analysis.gv', view=True)
