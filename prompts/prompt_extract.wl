# This is a another prompt for extracting named entities from a paragraph. I use is written on the basis of the mathematica is fully setup with Flask.
# The entities should be classified into names people, dates, and locations.


Extract named entities from the paragraph below. Classify them into:
- names (people only)
- dates (exact or approximate)
- locations (cities, countries, landmarks)

Return JSON format:
{
  "names": [],
  "dates": [],
  "locations": []
}

Paragraph: [Insert paragraph here]


