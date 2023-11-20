#!/usr/bin/python
# -*-coding: utf-8-*-

import os
import re
import json
import Utils.FileUtils as FileUtils

class LineItem():
	def __init__(self, lineInfo):
		self.init(lineInfo)

	def init(self, lineInfo):
		self.lineInfo = lineInfo
		self.blank = re.findall(r'([\s]*)', self.lineInfo, re.M | re.I)[0]
		self.realLine = self.lineInfo.strip()
		self.addedLineItems = []

	def addAddedLineItem(self, lineItem):
		self.addedLineItems.append(lineItem)
		pass

	def replaceInfo(self, oldInfo, newInfo):
		lineInfo = self.lineInfo.replace(oldInfo, newInfo)
		self.init(lineInfo)

	def setSameLineId(self, lineId):
		self.lineId = lineId

class FileItem():
	def __init__(self, file, logInfo = False):
		self.file = file
		self.logInfo = logInfo
		self.fileData = FileUtils.readFile(self.file)
		self.allLineItems = [LineItem(item) for item in self.fileData.split("\n")]

		allMap = {}

		def setItemLineId(item):
			if(item.realLine not in allMap):
				allMap[item.realLine] = 0
			item.setSameLineId(allMap[item.realLine])
			allMap[item.realLine] = allMap[item.realLine] + 1
			return item

		self.allLineItems = [setItemLineId(item) for item in self.allLineItems]

	def replaceLine(self, oldInfo, newInfo):
		print("==> [FileItem] [replaceLine] ", oldInfo, newInfo)
		for lineItem in self.allLineItems:
			if(oldInfo and newInfo):
				if(oldInfo in lineItem.lineInfo):
					print("==>  [FileItem] [replaceLine] 1:[{}] {} -> {}".format(FileUtils.getFileName(self.file, True), oldInfo, newInfo))
					lineItem.replaceInfo(oldInfo, newInfo)
				# if(self.logInfo and (oldInfo in lineItem.lineInfo)):
				# 	print("==> [FileItem] [replaceLine] 2 : 已包含 {} ".format(newInfo))
		
		self.saveFile()

	def shouldAddLines(self, addedLines, preLine, preLineId):
		if(len(addedLines) <= 0):
			return True;

		firstAddedLine = addedLines[0]
		findLineIdx = len(self.allLineItems)
		for lineIdx in range(0, len(self.allLineItems)):
			lineItem = self.allLineItems[lineIdx]
			if(lineItem.realLine == preLine and lineItem.lineId == preLineId):
				findLineIdx = lineIdx;

		subLineItems = self.allLineItems[findLineIdx:]
		allSubRealLines = [item.realLine for item in subLineItems]

		containsFirstLine = firstAddedLine in allSubRealLines
		shouldAdd = not containsFirstLine
		return shouldAdd

	def addLines(self, addedLines, preLine, preLineId):
		if(not self.shouldAddLines(addedLines, preLine, preLineId)):
			print("==> [FileItem] [addLines] 已包含:\n", json.dumps(addedLines, indent = 4));
			return;

		for lineIdx in range(0, len(self.allLineItems)):
			lineItem = self.allLineItems[lineIdx]
			if(lineIdx < len(self.allLineItems) - 1):
				nextLineItem = self.allLineItems[lineIdx+1]
				if(len(addedLines) > 0):
					firstAddedLine = addedLines[0]
					if(lineItem.realLine == preLine and lineItem.lineId == preLineId):
						if(nextLineItem.realLine != firstAddedLine):
							for addedLine in addedLines:
								lineInfo = "{}{}".format(lineItem.blank, addedLine)
								lineItem.addAddedLineItem(LineItem(lineInfo))
			else:
				if(lineItem.realLine == preLine and lineItem.lineId == preLineId):
					for addedLine in addedLines:
						lineInfo = "{}{}".format(lineItem.blank, addedLine)
						lineItem.addAddedLineItem(LineItem(lineInfo))

		lineItems = []
		for item in self.allLineItems:
			lineItems.append(item)
			if(len(item.addedLineItems) > 0):
				for addedLineItem in item.addedLineItems:
					lineItems.append(addedLineItem)
					if(self.logInfo):
						print("==> [FileItem] [addLines]: {} -> {}".format(self.file, addedLineItem.lineInfo))
					item.addedLineItems = []

		self.allLineItems = lineItems
		self.saveFile()

	def saveFile(self):
		newFileData = "\n".join([item.lineInfo for item in self.allLineItems])
		FileUtils.writeFile(self.file, newFileData)