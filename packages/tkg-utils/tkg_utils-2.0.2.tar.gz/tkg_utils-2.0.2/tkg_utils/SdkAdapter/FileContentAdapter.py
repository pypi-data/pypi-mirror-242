
import shutil
import os
import time
import json
import sys
import re
import pandas as pd
import subprocess

import Utils.FileUtils as FileUtils

from Normal.ItemInfo import ItemInfo
from SdkAdapter.FileItem import FileItem

class FileContentAdapter():
	def __init__(self, projectFolder):
		self.projectFolder = projectFolder

	def doAdapt(self, adapterFolder, sdkName):
		sdkFileContentAdapterFolder = f"{adapterFolder}/FileContentAdapter"
		excels = FileUtils.getFiles(sdkFileContentAdapterFolder, ".xls")
		sdkFileContentAdapterExcels = [item for item in excels if(FileUtils.getFileName(item, False) == sdkName)]
		if(len(sdkFileContentAdapterExcels) <= 0):
			print(f"\n==> [FileContentAdapter] [doAdapt] not exists: {sdkName}.xls")
			return
		sdkFileContentAdapterExcel = sdkFileContentAdapterExcels[0]

		print("\n==> [FileContentAdapter] [doAdapt] start:", sdkFileContentAdapterExcel)
		configs = FileUtils.readConfigExcel(sdkFileContentAdapterExcel, ["addedLines"])
		for item in configs:
			file = os.path.join(self.projectFolder, item["file"])
			if(not os.path.exists(file)):
				print("\n==> [FileContentAdapter] [doAdapt] file not exists:", file)
				continue;
			fileItem = FileItem(file, logInfo = True)
			newLines = []
			for addLine in item["addedLines"]:
				addLineFile = f"{adapterFolder}/File/FileContentAdapter/{addLine}"
				if(not os.path.exists(addLineFile)):
					print("\n==> [FileContentAdapter] [doAdapt] [addLine]:", addLineFile)
					newLines.append(addLine)
				else:
					print("\n==> [FileContentAdapter] [doAdapt] [addLineFile]:", addLineFile)
					fileData = FileUtils.readFile(addLineFile)
					fileLines = fileData.split("\n")
					for fileLine in fileLines:
						newLines.append(fileLine)

			fileItem.addLines(newLines , item["preLine"], item["preLineId"])
			fileItem.replaceLine(item["toBeReplacedContent"], item["replaceContent"])

		print("==> [FileContentAdapter] [doAdapt] end\n")

	def getFileContentInfos(self, adapterFolder, sdkName):
		fileAdapterFolder = f"{adapterFolder}/FileContentAdapter"
		excels = FileUtils.getFiles(fileAdapterFolder, ".xls")
		sdkFileAdapterExcels = [item for item in excels if(FileUtils.getFileName(item, False) == sdkName)]
		if(len(sdkFileAdapterExcels) <= 0):
			print(f"\n==> [FileAdapter] [getFileContentInfos] not exists: {sdkName}.xls")
			return []

		sdkFileAdapterExcel = sdkFileAdapterExcels[0]
		print("\n==> [FileAdapter] [getFileContentInfos] start")
		sdkConfigInfos = FileUtils.readConfigExcel(sdkFileAdapterExcel, ["addedLines"])
		sdkConfigInfos = [ItemInfo(item) for item in sdkConfigInfos]
		return sdkConfigInfos;




