def parse_odd_file(fname):
	"""
	Generator that parses an odd-numbered file
	into dictionaries of attributes.

	Args:
	- fname: file name

	Returns:
	Generator of dictionaries
	"""
	hline = "-" * 80  # Horizontal line
	paper = {}
	prevIsNewLine = False
	with open(fname) as ofile:
		for line in ofile:

			# Skip empty lines or lines before PMID
			if not line or (not paper and not line.startswith("PMID")):
				continue
			# Reset on horizontal line
			elif line.startswith(hline):
				yield paper
				paper = {}

			# Parse keys and values
			else:
				# Subsequent lines of key-value pair
				if line.startswith(" "):
					paper[key] += " " + line.strip()
				# First line of key-value pair
				elif "-" in line:
					# Split key and value
					key, value = [t.strip() for t in line.split("-", 1)]
					# Check if key is in paper
					if key in paper:
						prev = paper[key]
						# Check if already converted into a list
						if isinstance(prev, list):
							paper[key].append(value)
						else:
							paper[key] = [prev, value]
					# If not, simply add the value as string
					else:
						paper[key] = value
				# Flags
				else:
					paper[line.strip()] = True

	# in case the end of the last paper didn't end with a horizontal line
	if paper:
		yield paper



		