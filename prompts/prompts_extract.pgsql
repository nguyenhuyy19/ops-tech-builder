# This Prompts I use is written on the basis of the PostgreSQL language used to extract the name of the person, date and location from a text.
# It will return the results in the form of structured JSON with "Names", "dates", and "locations" courses.

{
  "prompt": "Extract all the names of people, dates, and locations mentioned in the following paragraph. Return the result as a structured JSON with keys: \"names\", \"dates\", and \"locations\".\nText: [Insert paragraph here]",
  "output_format": {
    "names": [],
    "dates": [],
    "locations": []
  }
}

>> Extract all the names of people, dates, and locations mentioned in the following paragraph. 
Return the result as a structured JSON with keys: "names", "dates", and "locations".
Text: [Insert paragraph here]
