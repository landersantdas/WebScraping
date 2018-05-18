import json
from tkinter import filedialog


def save(parseResult):
	savefile = filedialog.asksaveasfile(defaultextension=".json", mode = 'w', title = 'Select where to save the result')
	if (savefile is not None):
		json.dump(parseResult, savefile, indent = 4)
		print("\nParsing complete. ")
		print("\nResult saved successfully!")
	else:
		with open('result.json', 'w') as fp:
			json.dump(parseResult, fp, indent = 4)
			print("\nParsing complete.")
			print("\nThe result is saved on your default folder as 'result.json'.")
