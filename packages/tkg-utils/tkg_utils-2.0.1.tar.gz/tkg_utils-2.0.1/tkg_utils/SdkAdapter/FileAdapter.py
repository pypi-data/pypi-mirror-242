
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

class FileAdapter():
	def __init__(self, projectFolder):
		self.projectFolder = projectFolder

	def doAdapt(self, adapterFolder, sdkName):
		fileAdapterFolder = f"{adapterFolder}/FileAdapter"
		excels = FileUtils.getFiles(fileAdapterFolder, ".xls")
		sdkFileAdapterExcels = [item for item in excels if(FileUtils.getFileName(item, False) == sdkName)]
		if(len(sdkFileAdapterExcels) <= 0):
			print(f"\n==> [FileAdapter] [doAdapt] not exists: {sdkName}.xls")
			return

		sdkFileAdapterExcel = sdkFileAdapterExcels[0]
		print("\n==> [FileAdapter] [doAdapt] start")
		sdkConfigInfos = FileUtils.readConfigExcel(sdkFileAdapterExcel, ["sdkPackages"])
		sdkConfigInfos = [ItemInfo(item) for item in sdkConfigInfos]
		for sdkConfigInfo in sdkConfigInfos:
			sdkFolder = f"{adapterFolder}/File/FileAdapter"
			sdkPackages = sdkConfigInfo.sdkPackages
			sdkPackageFolders = [os.path.join(sdkFolder, item) for item in sdkPackages]
			for packageOrFile in sdkPackageFolders:
				print(f"\n==> [FileAdapter] [doAdapt] fileOrFolder: {os.path.abspath(packageOrFile)}")
				if(os.path.isfile(packageOrFile)):
					relPath = os.path.relpath(packageOrFile, sdkFolder)
					newPath = os.path.join(self.projectFolder, relPath)
					print("==> [FileAdapter] [doAdapt] file: " + relPath)
					FileUtils.copyFile(packageOrFile, newPath)
					continue

				allFiles = FileUtils.getFiles(packageOrFile, "", onlyTop = True)
				for file in allFiles:
					relPath = os.path.relpath(file, sdkFolder)
					newPath = os.path.join(self.projectFolder, relPath)
					print("==> [FileAdapter] [doAdapt] fileInFolder: " + relPath)
					FileUtils.copyFile(file, newPath)

		print("\n==> [FileAdapter] [doAdapt] end\n")

	




