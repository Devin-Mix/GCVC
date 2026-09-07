import hashlib
from pathlib import Path

# This is a quick and dirty script for creating patches.
# It does absolutely no checking of whether or not files or directories are missing. If something is off, it throws an unhandled exception.
# In other words, it's not idiot-proof. This script assumes that you know what you're doing when you create a patch.
# If you decide to use it, be sure to validate that your patches produce good, working files before publishing them anywhere.
# Once your patches are made, the hash for each will be printed. Be sure to copy those to config.json to so that convert.py's hash checks will pass.

def main():
	filesToPatch = [
		Path("banner") / Path("my_BackSNES_a.png"),
		Path("banner") / Path("VCPic.png"),
		Path("icon") / Path("LogoSNES.png"),
		Path("icon") / Path("IconVCPic.png"),
		Path("banner.brlyt")
	]
	print("Creating patches for {} files...".format(len(filesToPatch)))
	inPaths = [Path("in") / ii for ii in filesToPatch]
	targetPaths = [Path("targets") / ii for ii in filesToPatch]
	patchPaths = [str(Path("patches") / ii) + ".patch" for ii in filesToPatch]
	for ii in range(len(filesToPatch)):
		print("Loading input file {}...".format(inPaths[ii]))
		with open(inPaths[ii], "rb") as inFile:
			inData = inFile.read()
		print("Load complete.")
		print("Loading target file {}...".format(targetPaths[ii]))
		with open(targetPaths[ii], "rb") as targetFile:
			targetData = targetFile.read()
		print("Load complete.")
		patchData = b""
		print("Generating patch data...")
		for jj in range(min(len(inData), len(targetData))):
			# Partial credit for this:
			# https://stackoverflow.com/questions/22593822/doing-a-bitwise-operation-on-bytes
			patchData = patchData + bytes([inData[jj] ^ targetData[jj]])
		if len(inData) < len(targetData):
			print("Input file is smaller than target file. Appending supplemental data from target...")
			patchData = patchData + targetData[len(inData):]
		print("Patch created successfully. Hashing...")
		patchHash = hashlib.new("sha256")
		patchHash.update(patchData)
		print("Hash for file {}: {}".format(patchPaths[ii], patchHash.hexdigest()))
		print("Writing to file {}...".format(patchPaths[ii]))
		with open(patchPaths[ii], "wb+") as patchFile:
			patchFile.write(patchData)
		print("Write complete.")

if __name__ == "__main__":
	main()
