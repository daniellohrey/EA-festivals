import json
from festivals import parseData

class TestParseData:
	def test_parseData(self):
		testData = '[{"name":"Festival A","bands":[{"name":"Band A","recordLabel":"Label A"},{"name":"Band B", "recordLabel":"Label B"}]}, {"name":"Festival B","bands":[{"name":"Band C","recordLabel":"Label C"},{"name":"Band D", "recordLabel":"Label D"}]}]'

		jsonData = json.loads(testData)
		data = parseData(jsonData)

		assert 'Label A' in data
		assert 'Band A' in data['Label A']
		assert 'Festival A' in data['Label A']['Band A']

		assert 'Label B' in data
		assert 'Band B' in data['Label B']
		assert 'Festival A' in data['Label B']['Band B']

		assert 'Label C' in data
		assert 'Band C' in data['Label C']
		assert 'Festival B' in data['Label C']['Band C']

		assert 'Label D' in data
		assert 'Band D' in data['Label D']
		assert 'Festival B' in data['Label D']['Band D']

	def test_missingLabel(self):
		testData = '[{"name":"Festival A","bands":[{"name":"Band A","recordLabel":"Label A"},{"name":"Band B"}]}]'

		jsonData = json.loads(testData)
		data = parseData(jsonData)

		assert 'Label A' in data
		assert 'Band A' in data['Label A']
		assert 'Festival A' in data['Label A']['Band A']

		assert 'No Record Label' in data
		assert 'Band B' in data['No Record Label']
		assert 'Festival A' in data['No Record Label']['Band B']

	def test_emptyLabel(self):
		testData = '[{"name":"Festival A","bands":[{"name":"Band A","recordLabel":"Label A"},{"name":"Band B", "recordLabel":""}]}]'

		jsonData = json.loads(testData)
		data = parseData(jsonData)

		assert 'Label A' in data
		assert 'Band A' in data['Label A']
		assert 'Festival A' in data['Label A']['Band A']

		assert 'No Record Label' in data
		assert 'Band B' in data['No Record Label']
		assert 'Festival A' in data['No Record Label']['Band B']

	def test_emptyFestival(self):
		testData = '[{"bands":[{"name":"Band A","recordLabel":"Label A"},{"name":"Band B", "recordLabel":"Label B"}]}]'

		jsonData = json.loads(testData)
		data = parseData(jsonData)

		assert 'Label A' in data
		assert 'Band A' in data['Label A']
		assert len(data['Label A']['Band A']) == 0

		assert 'Label B' in data
		assert 'Band B' in data['Label B']
		assert len(data['Label B']['Band B']) == 0
