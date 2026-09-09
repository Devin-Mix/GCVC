import hashlib, json
from pathlib import Path
from struct import pack, unpack
from sys import argv

def main():
	debug = False
	createImages = True
	if "--debug" in argv:
		debug = True
		debugPrint(debug, "Debugging enabled.")
	if "--no-images" in argv:
		debugPrint(debug, "--no-images specified, no images will be created.")
		createImages = False
	if Path("gcvc.py").exists():
		debugPrint(debug, "Working directory appears to be correct. Hashing script...")
		# Hash script here so that, when bugs are submitted with the debug output, we know that the script wasn't modified.
		with open("gcvc.py", "rb") as thisFile:
			thisFileBin = thisFile.read()
		thisFileHash = hashlib.new("sha256")
		thisFileHash.update(thisFileBin)
		debugPrint(debug,"Script hash: {}".format(thisFileHash.hexdigest()))
	else:
		print("GC⚡VC launched successfully, but could not find itself in your working directory.")
		print("Please change your working directory to wherever GC⚡VC is saved, then try again.")
		print("Exiting...")
		exit()
	print("+-----------------------------------------------------------------------------+")
	print("|                                                                             |")
	print("|                     /\\      /\\             ^    ^    /\\                     |")
	print("|                    /  \\    /  \\           / \\  / \\  /  \\                    |")
	print("|                   / |\\ \\  / |\\ \\     ____ \\ /  \\ / / |\\ \\                   |")
	print("|                   | | \\ \\ | | \\ \\   /   / | |  | | | | \\ \\                  |")
	print("|                   | |  \\/ | |  \\/  /   /  | |  | | | |  \\/                  |")
	print("|                   | |     | |     /   /__ | |  | | | |                      |")
	print("|                   | | /\\  | |    /___   / | |  | | | |                      |")
	print("|                   | | \\ \\ | |  /\\   / _/  | |  / / | |  /\\                  |")
	print("|                   | | / / | | / /  / /    | | / /  | | / /                  |")
	print("|                   | |/ /  | |/ /  /_/     | |/ /   | |/ /                   |")
	print("|                   \\   /   \\   /  //       \\   /    \\   /                    |")
	print("|                    \\ /     \\ /  //         \\ /      \\ /                     |")
	print("|                     V       V   V           V        V                      |")
	print("|                                                                             |")
	print("+-----------------------------------------------------------------------------+")
	print("|                                                                             |")
	print("|                      v0.1 by Mixtape | Released 9/7/2026                    |")
	print("|                                                                             |")
	print("+-----------------------------------------------------------------------------+")
	print("|                                                                             |")
	print("|   !!WARNING!! !!WARNING!! !!WARNING!! !!WARNING!! !!WARNING!! !!WARNING!!   |")
	print("|                                                                             |")
	print("|      This script allows you to create custom banner files for your Wii.     |")
	print("|    In certain cases, malformed banner files can result in a banner brick.   |")
	print("|  A banner brick will prevent the Wii System Menu from loading. Depending on |")
	print("|   how your system is set up, this could make your Wii permanently unusable. |")
	print("|    The maintainer(s) of this project assume(s) NO RESPONSIBILITY for any    |")
	print("|              damage that its output may cause to your system!               |")
	print("|                                                                             |")
	print("|  In order to continue, you must agree to take responsibility for any damage |")
	print("|   that this script's output may cause to your Wii. You must also agree to   |")
	print("|   take preventative actions to prevent irreversible damage to your system,  |")
	print("|    such as by taking a NAND backup using BootMii or nanddumper@ios, prior   |")
	print("|                            to using this script.                            |")
	print("|                                                                             |")
	print("|        For information on how to create a NAND backup, please visit:        |")
	print("|                     https://wii.hacks.guide/nand-backup                     |")
	print("|                                                                             |")
	print("|    IF YOU AGREE TO THE ABOVE TERMS, TYPE \"I AGREE\" IN ALL CAPS AND PRESS    |")
	print("|                             ENTER TO CONTINUE.                              |")
	print("|                                                                             |")
	print("|     If you do not agree, press enter without entering any text to exit.     |")
	print("|                                                                             |")
	print("+-----------------------------------------------------------------------------+\n")
	consentResponse = input("Enter your response, without quotation marks, here: ")

	if consentResponse == "I AGREE":
		print("\nAgreement acknowledged, proceeding...")
	else:
		print("\nTerms declined, exiting...")
		exit()

	debugPrint(debug, "Checking for config file...")
	configFilePath = Path("config.json")
	if not configFilePath.exists():
		print("Config file does not exist. Make sure it's present and accessible in your working directory. Exiting...")
		exit()
	debugPrint(debug, "Loading config file...")
	with open("config.json", "r") as configFile:
		data = json.load(configFile)
	debugPrint(debug, "Config file loaded. Options are shown below:")
	debugPrint(debug, data)
	debugPrint(debug, "Parsing paths to platform-compatible format...")
	for ii in data.keys():
		splitPath = data[ii]["path"].split("/")
		newPath = Path(splitPath[0])
		if len(splitPath) > 1:
			for jj in range(1, len(splitPath)):
				newPath = newPath / splitPath[jj]
		debugPrint(debug, "Converted path {} to {}.".format(data[ii]["path"], newPath))
		data[ii]["path"] = newPath
	debugPrint(debug, "Paths parsed successfully.")

	debugPrint(debug, "Checking in, out, and patch directory structures...")
	# Do this by splitting paths specified in the config file instead of hardcoding values here.
	for ii in ["in", "out", "patches"]:
		for jj in data.keys():
			checkPath = Path(ii)
			if checkPath.exists() and checkPath.is_dir():
				show_dir_exists(debug, checkPath)
			else:
				show_dir_absent(checkPath)
			pathParts = data[jj]["path"].parts
			# If this is just a file, no need to check. We'll do that later
			if len(pathParts) > 1:
				# Don't check actual file now, only dirs
				for kk in range(len(pathParts) - 1):
					checkPath = checkPath / Path(pathParts[kk])
					if checkPath.exists() and checkPath.is_dir():
						show_dir_exists(debug, checkPath)
					else:
						show_dir_absent(checkPath)
	debugPrint(debug, "Directory structure OK.")

	print("\nThe script will now check for the required donor files from F-Zero (USA) (SNES) (Virtual Console).wad.")
	print("If you have not already extracted them using CustomizeMii, please do so now and place them in the following folders:")
	print("\n[Working Directory]")
	print("|")
	print("+- in")
	print("   |")
	print("   +- banner")
	print("   |  |")
	print("   |  +- my_BackSNES_a.png")
	print("   |  |")
	print("   |  +- VCPic.png")
	print("   |")
	print("   +- icon")
	print("   |  |")
	print("   |  +- LogoSNES.png")
	print("   |  |")
	print("   |  +- IconVCPic.png")
	print("   |")
	print("   +- banner.brlyt")
	print("\nPlease see the README for more information on how to extract these files.")
	input("\nOnce your files are placed properly, press enter to continue...")

	debugPrint(debug, "\nChecking for input files...")
	inputFilePaths = [Path("in") / data[key]["path"] for key in data.keys()]
	for ii in inputFilePaths:
		if ".png" in str(ii) and not createImages:
			debugPrint(debug, "Skipping check for image {}".format(ii))
			continue
		if ii.exists() and not ii.is_dir():
			show_file_exists(debug, ii)
		else:
			show_file_absent(ii)
	debugPrint(debug, "All input files are present.")

	debugPrint(debug, "Loading input files...")
	for ii in data.keys():
		if ".png" in str(ii) and not createImages:
			debugPrint(debug, "Skipping loading of image {}".format(ii))
			continue
		with open(Path("in") / data[ii]["path"], "rb") as inFile:
			data[ii]["inData"] = inFile.read()
	debugPrint(debug, "All input files loaded.")

	debugPrint(debug, "Checking input file hashes...")
	for ii in data.keys():
		if ".png" in str(ii) and not createImages:
			debugPrint(debug, "Skipping hashing of image {}".format(ii))
			continue
		inHash = hashlib.new("sha256")
		inHash.update(data[ii]["inData"])
		if inHash.hexdigest() == data[ii]["inHash"]:
			debugPrint(debug, "File {} is ok.".format(ii))
		else:
			print("File {} has an incorrect hash. Please ensure that you have the correct donor WAD, re-export the file, and try again. Exiting...".format(ii))
			exit()
	debugPrint(debug, "All files have correct hashes.")

	debugPrint(debug, "\nChecking for patches...")
	patchPaths = [Path(str(Path("patches") / data[key]["path"]) + ".patch") for key in data.keys()]
	for ii in patchPaths:
		if ii.exists() and not ii.is_dir():
			show_patch_exists(debug, ii)
		else:
			show_patch_absent(ii)
	debugPrint(debug, "All patches are present.")

	debugPrint(debug, "\nLoading patches...")
	for ii in data.keys():
		with open(str(Path("patches") / data[ii]["path"]) + ".patch", "rb") as patchFile:
			data[ii]["patchData"] = patchFile.read()
	debugPrint(debug, "All patches loaded.")

	debugPrint(debug, "Checking patch hashes...")
	for ii in data.keys():
		patchHash = hashlib.new("sha256")
		patchHash.update(data[ii]["patchData"])
		if patchHash.hexdigest() == data[ii]["patchHash"]:
			debugPrint(debug, "Patch {}.patch is ok.".format(ii))
		else:
			print("Patch {} has an incorrect hash. If this was not expected, proceeding from here will likely result in corrupted data.".format(ii))
			print("If you are patching to create a modified target and have created a new patch, please provide the updated hash from make_patches.py in config.json and try again.")
			print("Exiting...")
			exit()
	debugPrint(debug, "All patches have correct hashes.")

	debugPrint(debug, "\nPatching files...")
	for ii in data.keys():
		if ".png" in str(ii) and not createImages:
			debugPrint(debug, "Skipping patching for image {}".format(ii))
			continue
		data[ii]["outData"] = b""
		for jj in range(min(len(data[ii]["inData"]), len(data[ii]["patchData"]))):
			# Partial credit for this:
                        # https://stackoverflow.com/questions/22593822/doing-a-bitwise-operation-on-bytes
			data[ii]["outData"] = data[ii]["outData"] + bytes([data[ii]["inData"][jj] ^ data[ii]["patchData"][jj]])
		if len(data[ii]["inData"]) < len(data[ii]["patchData"]):
			debugPrint(debug, "{} is smaller than patch file. Appending supplemental data from patch...".format(data[ii]["path"]))
			data[ii]["outData"] = data[ii]["outData"] + data[ii]["patchData"][len(data[ii]["inData"]):]
		debugPrint(debug, "{} patched successfully.".format(data[ii]["path"]))
		# *Could* hash the output here to validate it. Shouldn't need to though since we've already checked the input and the patch, so the output is deterministic.
	debugPrint(debug, "All files patched successfully.")

	print("\nYou may now modify the game's title, release year, and player count.")
	print("Each field has a very large (>30000) character limit that you are unlikely to hit under any circumstances.")
	print("Note that certain characters may not be present in the channel's font and may cause issues as a result.")
	print("\nThe title will appear below the title screen thumbnail after clicking on the \"channel\" on your home screen.")
	print("Please note that this is not the text that appears when you hover over the channel. Use CustomizeMii to set that.")
	newTitle = input("\nEnter your new title and press enter, or press enter without typing anything to use a placeholder title: ")

	if newTitle != "":
		debugPrint(debug, "\nValidating new title...")
		if len(newTitle) > 32767:
			print("New title exceeds maximum length. (Why would you do this???) Exiting...")
			exit()
		else:
			debugPrint(debug, "Title length ok.")
		try:
			newTitle.encode("utf-16")
		except:
			print("New title cannot be encoded in utf-16. Either you've intentionally done something really crazy or this is a bug. Please file an issue on GitHub. Exiting...")
			exit()
		debugPrint(debug, "Title encoding ok.")
		debugPrint(debug, "New title is valid.")
		debugPrint(debug, "Modifying title...")
		data["banner.brlyt"]["outData"] = replace_txt1_string(debug, data["banner.brlyt"]["outData"], b"T_VCTitle_", newTitle)
	else:
		print("Title modification skipped.")

	print("\nWhen entering a release year, keep in mind that the \"Released: \" prefix will not be included by default.")
	print("For example, if you want the release information to say \"Released: 20XX\", you should type that entire phrase, not just \"20XX\".")
	newReleased = input("Enter your new Released line, or press enter to use a placeholder: ")

	if newReleased != "":
		debugPrint(debug, "\nValidating new Released line...")
		if len(newReleased) > 32767:
			print("New Released line exceeds maximum length. (Why would you do this???) Exiting...")
			exit()
		else:
			debugPrint(debug, "Released line length ok.")
		try:
			newReleased.encode("utf-16")
		except:
			print("New released line cannot be encoded in utf-16. Either you've intentionally done something really crazy or this is a bug. Please file an issue on GitHub. Exiting...")
			exit()
		debugPrint(debug, "Released line encoding ok.")
		debugPrint(debug, "New Released line is valid.")
		debugPrint(debug, "Modifying Released line...")
		data["banner.brlyt"]["outData"] = replace_txt1_string(debug, data["banner.brlyt"]["outData"], b"T_Year_", newReleased)
	else:
		print("Released line modification skipped.")

	print("\nAs with the release year, the player count will not be automatically prefixed with \"Players: \".")
	print("\nIf you want to replicate the default look, you should enter \"Players: X-Y\" or \"Players: 1\".")
	newPlayers = input("Enter your new Players line, or press enter to use a placeholder: ")

	if newPlayers != "":
		debugPrint(debug, "\nValidating new Players line...")
		if len(newPlayers) > 32767:
			print("New Players line exceeds maximum length. (Why would you do this???) Exiting...")
			exit()
		else:
			debugPrint(debug, "Players line length ok.")
		try:
			newPlayers.encode("utf-16")
		except:
			print("New Players line cannot be encoded in utf-16. Either you've intentionally done something really crazy or this is a bug. Please file an issue on GitHub. Exiting...")
			exit()
		debugPrint(debug, "Players line encoding ok.")
		debugPrint(debug, "New Players line is valid.")
		debugPrint(debug, "Modifying Players line...")
		data["banner.brlyt"]["outData"] = replace_txt1_string(debug, data["banner.brlyt"]["outData"], b"T_Play_", newPlayers)
	else:
		print("Players line modification skipped.")


	print("\nThe patched files will now be saved to the out directory. Any existing output files located there will be overwritten.")
	input("If you have existing output files that you would like to keep, please move or rename them, then press enter to continue...") 
	print("\nSaving output files...")
	for ii in data.keys():
		if ".png" in str(ii) and not createImages:
			debugPrint(debug, "Skipping outputting image {}".format(ii))
			continue
		debugPrint(debug, "Writing to file {}...".format(Path("out") / data[ii]["path"]))
		with open(Path("out") / data[ii]["path"], "wb+") as outFile:
			outFile.write(data[ii]["outData"])
		debugPrint(debug, "Write complete.")
	print("All files written successfully.")
	

def show_dir_exists(debug, dirPath):
	debugPrint(debug, "Directory {} exists...".format(str(dirPath)))

def show_dir_absent(dirPath):
	print("Directory {} is absent. Make sure it's present and accessible in your working directory. Exiting...".format(str(dirPath)))
	exit()

def show_file_exists(debug, filePath):
	debugPrint(debug, "File {} exists...".format(str(filePath)))

def show_file_absent(filePath):
	print("File {} is absent. Make sure it's present and accessible in your working directory. Exiting...".format(str(filePath)))
	exit()

def show_patch_exists(debug, patchPath):
	debugPrint(debug, "Patch {} exists...".format(str(patchPath)))

def show_patch_absent(patchPath):
	print("Patch {} is absent. Make sure it's present and accessible in your working directory. Exiting...".format(str(patchPath)))
	exit()

# Nice. clean function for modifying the string shown in txt1 panes.
# Takes in the full brlyt binary, a substring of the pane name to search for, and the text to replace the existing string with.
# Returns the modified binary.
def replace_txt1_string(debug, data, searchString, newText):
	debugPrint(debug, "Fetching BOM...")
	# Grab the byte order here for struct to use later.
	if data[4:6] == b"\xfe\xff":
		bom = ">"
	else:
		bom = "<"
	debugPrint(debug, "BOM is {}.".format(bom))
	# Indexer to allow for restarting iteration without revisiting previously reviewed data
	searchPoint = 0
	while True:
		for ii in range(searchPoint, len(data)):
			# Lots of information from https://mkwiiki.org/wiki/BRLYT_%28File_Format%29 was used here.
			# TODO: Should probably actually parse/skip panes instead of naively looking for txt1, but it's probably harmless.
			if data[ii:ii+4] == b"txt1":
				debugPrint(debug, "Found txt1 at decimal offset {}, checking for {}...".format(ii, searchString))
				# Check offset here is 0x08 (to get to base pane) plus 0x04 (to get to pane name)
				# Pane name is Char[16]. Easy to check against.
				if searchString in data[ii+12:ii+28]:
					debugPrint(debug, "Pane found with {} in name.".format(searchString))
					# Pane offset +76 gets to UInt16 string size
					oldStrSize = unpack("{}H".format(bom), data[ii + 76:ii + 78])[0]
					debugPrint(debug, "Current string size is {} bytes.".format(oldStrSize))
					# Everything from here on out will assume that the string comes immediately after the line size.
					# This should be taken into account when creating a target file, in case you're one of those creative types who wants to put your strings elsewhere for some reason.
					# However, in most cases, it shouldn't be a problem.
					oldPaneEnd = ii + 116 + oldStrSize
					debugPrint(debug, "Old pane ended at decimal offset {}.".format(oldPaneEnd))
					if oldPaneEnd % 4 != 0:
						oldPaneEnd += 4 - (oldPaneEnd % 4)
						debugPrint(debug, "Padded to {} to account for 4 alignment.".format(oldPaneEnd))
					# Quick slice for readability's sake
					oldPane = data[ii:ii+oldPaneEnd]
					debugPrint(debug, "Building new pane...")
					# Can start with magic and base pane, since those are unchanged.
					newPane = oldPane[0:76]
					# Setting max string size = string size shouldn't be a problem, right?
					newPane = newPane + pack("{}H".format(bom), (len(newText) * 2) + 2) + pack("{}H".format(bom), (len(newText) * 2) +  2)
					# Keep everything else right up to the actual string
					# (Good modding opportunity here)
					newPane = newPane + oldPane[80:116]
					# Handle endianness here so that python doesn't prepend a BOM to the string.
					if bom == ">":
						newTextBytes = newText.encode("utf-16-be") + b"\x00\x00"
					else:
						newTextBytes = newText.encode("utf-16-le") + b"\x00\x00"
					newPane = newPane + newTextBytes
					debugPrint(debug, "New pane is {} bytes long.".format(len(newPane)))
					if len(newPane) % 4 != 0:
						newPane = newPane + (b"\x00" * (4 - (len(newPane) % 4)))
						debugPrint(debug, "Padded to {} for 4 alignment.".format(len(newPane)))
					# Set section length
					newPane = newPane[0:4] + pack("{}I".format(bom), len(newPane)) + newPane[8:]
					debugPrint(debug, "Inserting new pane...")
					data = (
						# Everything up to the old pane
						data[0:ii] +
						# The new pane
						newPane +
						# Everything that came after the old pane
						data[oldPaneEnd:]
					)
					# Update searchpoint to keep looking for txt1 *after* the pane that we just inserted, then reset the iteration loop.
					searchPoint = ii + len(newPane)
					break
		else:
			# We hit this when iteration is complete.
			# Update the file length in the header to account for any changes that were made.
			# TODO: Add some handling for if this number overflows. (Probably an edge case, but worth handling.)
			data = (
				# File magic, BOM, and format version number
				data[0:8] +
				# New length
				pack("{}I".format(bom), len(data)) +
				# Everything else
				data[12:]
			)
			return data

def debugPrint(debug, printout):
	if debug:
		print(printout)

if __name__ == "__main__":
	main()
