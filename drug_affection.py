import json
from client import textPrompt
from database.db_connection import Database

class DrugRegionParser:
    def __init__(self, drugName: str):
        self.drugName = drugName

    # Fn: prompt()
    # Brief: Prompts the language model for the regions and afflication types for the drug
    def prompt(self):
        req = f"""
        You are a medical information specialist tasked with analyzing and describing the effects of a specific drug on the human body. Your goal is to provide a structured JSON response containing clear, accurate information about the drug's common effects at regular dosages.

        Here is the name of the drug you need to analyze:

        <drug_name>
        {self.drugName}
        </drug_name>

        Follow these guidelines for your analysis and final JSON response:

        1. Focus only on common effects that occur at regular dosages. Exclude rare side effects or effects from high dosages.
        2. Include information for a body system only if there are notable effects. Omit systems not significantly affected.
        3. Use language that is easily understandable for the average person.
        4. For the brain, try to only pick the most notable regions
        5. Use "POSITIVE" for beneficial effects and "NEGATIVE" for adverse effects.

        After your analysis, generate a JSON response using the following structure:

        {{
          "brain": [
            {{
              "name": "[Name of affected brain region]",
              "responseType": "[POSITIVE or NEGATIVE]",
              "responseDescription": "[Clear description of the effect]"
            }}
          ],
          "muscular": [
            {{
              "name": "[Name of affected muscle or muscle group]",
              "responseType": "[POSITIVE or NEGATIVE]",
              "responseDescription": "[Clear description of the effect]"
            }}
          ],
          "skeletal": [
            {{
              "name": "[Name of affected bone or bone group]",
              "responseType": "[POSITIVE or NEGATIVE]",
              "responseDescription": "[Clear description of the effect]"
            }}
          ],
          "organs": [
            {{
              "name": "[Name of affected organ]",
              "responseType": "[POSITIVE or NEGATIVE]",
              "responseDescription": "[Clear description of the effect]"
            }}
          ]
        }}

        Important: Your final output must be valid JSON only, with no additional text or explanations outside the JSON structure. Ensure all descriptions are clear and easily understandable for non-medical professionals.

        Please proceed with your analysis and JSON response for the drug specified.    
        """

        data = textPrompt(req, False)
        return data

    # Fn: query()
    # Brief: Queries the db for the drug
    # Rets: The data or None if it wasn't found
    def query(self):
        db = Database().db
        drugs = db['Drugs']

        drug = drugs.find_one({"name": self.drugName})
        return drug

    # Fn: addDrug()
    # Brief: Adds the drug into mongo
    def addDrug(self, data):
        db = Database().db
        drugs = db['Drugs']
        res = drugs.insert_one(data)
        data['_id'] = res.inserted_id

        # Now fetch the drug
        return data

    def setDrugName(self, drugName):
        self.drugName = drugName

    # Fn findAffected()
    # Brief: Check if the name of the drug already exists in the db, else prompt for it
    # Rets: str - The json of the affected regions in this format { brain: [], muscular: [], skeletal: [], organs: [] }
    def findAffected(self):
        # 1. Query for data
        data = self.query()

        # 2. If drug doesn't exist, then prompt for it
        if not data:
            promptData = self.prompt()
            newData = {
                "name": self.drugName,
                "form": None,
                "affections": json.loads(promptData)
            }
            data = self.addDrug(newData)
        return data

if __name__ == "__main__":
    regionParser = DrugRegionParser("advil")

    regions = regionParser.findAffected()
    # print(regions)
    print(regions['name'])
    for affectionRegion in regions['affections']:
        ent = regions['affections'][affectionRegion]
        for item in ent:
            print(item)