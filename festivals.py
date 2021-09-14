import requests, logging, json

def getData(url):
	logging.info('Fetching data...')
	data = None

	# Sometimes API doesn't return data due to throttling
	while not data:
		r = requests.get(url)
		try:
			data = r.json()
		except json.decoder.JSONDecodeError:
			pass # Catch any parsing errors from throttling message
	
	logging.debug('API data: ' + str(data))
	return data

def parseData(jsonData):
	logging.info('Parsing data...')
	data = {}
	for festival in jsonData:
		# Some 'festivals' don't have a festival name
		# Presumably because some bands didn't play at a festival
		try:
			festivalName = festival['name']
		except KeyError:
			festivalName = None

		for band in festival['bands']:
			bandName = band['name']
			# Some bands have an empty recordLabel, or missing field
			# Presumably because they aren't attached to a label
			try:
				if len(band['recordLabel']) == 0:
					recordLabel = 'No Record Label'
				else:
					recordLabel = band['recordLabel']
			except KeyError:
				recordLabel = 'No Record Label'

			if recordLabel not in data:
				data[recordLabel] = {}
			if bandName not in data[recordLabel]:
				data[recordLabel][bandName] = []
			if festivalName and festivalName not in data[recordLabel][bandName]:
				data[recordLabel][bandName].append(festivalName)
			logging.debug(recordLabel + ' - ' + bandName + ' - ' + str(festivalName))
	return data
	
def printData(data):
	logging.debug('To print: ' + str(data))
	for label in sorted(data):
		print(label)
		for band in sorted(data[label]):
			print('\t' + band)
			for festival in sorted(data[label][band]):
				print('\t\t' + festival)
		print() #newline

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	jsonData = getData('https://eacp.energyaustralia.com.au/codingtest/api/v1/festivals')
	parsedData = parseData(jsonData)
	printData(parsedData)
