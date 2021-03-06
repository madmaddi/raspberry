#!/usr/bin/python
# coding=utf-8

import os
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
from xml.dom import minidom
import DayInterval
import datetime


class PartitionEntry(object):

    windowOpenTimeInSeconds = 0
    windowOpenCount = 0
    windowCloseCount = 0

    xmlFile = None

    fileName = ""

    def __str__(self):
        msg = ""
        msg += "windowOpenTimeInSeconds =  %i\n" % self.windowOpenTimeInSeconds
        msg += "windowOpenCount = %i\n" % self.windowOpenCount
        msg += "windowCloseCount = %i\n" % self.windowCloseCount
        return msg

    def setFileName(self, fileName):
        self.fileName = "./db/%s.xml" % fileName

    """
    """
    def __init__(self, fileName):
        self.setFileName(fileName)
        try:
            d = DayInterval.DayInterval()
            partition = d.getCurrentPartition()
            self.initFile(partition)
        except IOError:
            self.createPartitionEntry()
            try:
                self.initFile(partition)  # 2nd try
            except IOError:
                raise Exception("epic fail")

    """
    """
    def addWindowOpenTime(self, t, partition):
        xpath = './entries/partition[@number="%s"]/windowOpenTime' % partition
        e = self.xmlFile.find(xpath)
        e.text = str(int(e.text) + t)
        self.saveToFile()


    """
    """
    def initFile(self, partition):
        self.xmlFile = ElementTree(file=self.fileName)
        xpath = './entries/partition[@number="%s"]' % partition
        for e in self.xmlFile.findall(xpath):
            self.windowOpenTimeInSeconds = e.find("windowOpenTime").text
            self.windowOpenCount = e.find("windowOpenCount").text
            self.windowCloseCount = e.find("windowCloseCount").text

    """
    """
    def updatePartition(self, partition = 0):
        xpath = './entries/partition[@number="%s"]' % partition

        for e in self.xmlFile.findall(xpath):
            e.find("windowOpenTime").text = self.windowOpenTimeInSeconds
            e.find("windowOpenCount").text = self.windowOpenCount
            e.find("windowCloseCount").text = self.windowCloseCount


    """
    Speichert aktuelle Repräsentation der Instanz in xmlFile auf die Platte
    """
    def saveToFile(self):
        if self.fileName == None or self.fileName == "": return
        self.xmlFile.write(self.fileName)

    """
        Erstellt neues PartitionEntryObject und schreibt es auf die Platte
    """
    def createPartitionEntry(self):
        # FileName setzen
        self.setFileName(datetime.date.today())

        root = Element('root')

        comment = Comment('Generated by PartitionEntry.createPartitionEntry')
        root.append(comment)

        date = SubElement(root, 'date')
        date.text = self.fileName

        entries = SubElement(root, 'entries')

        for i in range(DayInterval.DayInterval.NUMBER_PARTITIONS):
            partition = SubElement(entries, 'partition')
            partition.set("number", str(i))

            wot = SubElement(partition, 'windowOpenTime')
            woc = SubElement(partition, 'windowOpenCount')
            wcc = SubElement(partition, 'windowCloseCount')

            wot.text = "0"
            woc.text = "0"
            wcc.text = "0"

        rough_string = tostring(root, 'utf-8')
        rootNode = minidom.parseString(rough_string)


        file_handle = open(self.fileName, "wb")
        rootNode.writexml(file_handle, addindent="\t", newl='\n')
        file_handle.close()


if __name__ == "__main__":
    p = PartitionEntry(datetime.date.today())
    #p.loadFromFile()
    #p.windowOpenCount = "jjj"
    #p.updatePartition()
    #p.saveToFile()
    #p.createPartitionEntry()
    p.addWindowOpenTime(5, 0)
