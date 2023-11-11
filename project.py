import requests

def main():

    # key, value = drug, rxcui
    print("\nDRUG-DRUG CHECK, enter 'done' when finished")

    drugs = drugs_to_check()

    if  len(drugs) >=2:

        try:
            onchigh = interaction_check(drugs, "onchigh")
            drugbank = interaction_check(drugs, "drugbank")

            # merge common values into one dict

            interactions = combined_dict(onchigh,drugbank)

            print(f"\n{len(interactions)} INTERACTIONS FOUND!\n")

            inter_num = 1
            for i in interactions:
                print(f"{inter_num}. {i}:\n{interactions[i]}\n")
                inter_num += 1

        except TypeError:
            print("no interactions found :)")

    else:
        print('need more than 1 drug')


# combine two dictionaries, append b after a if there are keys that match.
def combined_dict(a,b):

    combined = a.copy()
    # we want to make a copy of in the input bc it will affect the original dict that was passed in.
    for key, value in b.items():
        if key in combined:
            combined[key] = f"{combined[key]}\n{value}"
        else:
            combined[key] = value


    return combined


# prompt user for input, checks if drug is real drug via get_rxcui, create a list to print back to user.
# return a drug list to be checked.
# must enter more than 1 valid drug to continue

def drugs_to_check():
    drug_number = 1
    drug_list = dict()
    while True:
        drug = input(f"enter drug {drug_number}:  ")
        if drug in {"","done"}:
            break

        if get_rxcui(drug) == None:
            print(f"{drug} not found")
            continue

        if drug in drug_list:
            print(f"{drug} already entered")
            continue

        drug, rxcui = get_rxcui(drug)
        # create a dict of drug names to rxcui
        drug_list[drug] = rxcui
        drug_number += 1
        # convert drug entered to drug names matched and print out for user to see.
        if drug_number > 1:


            drugs_to_check = list()
            for key in drug_list:
                drugs_to_check.append(key)

            print(f'\tCheck interactions between: {drugs_to_check}')

    return drug_list

# get drug code via approximate matching API, return name and rxcui
def get_rxcui(drug):
    response = requests.get(f"https://rxnav.nlm.nih.gov/REST/approximateTerm.json?term={drug}&maxEntries=10")
    if response.status_code == 200:
        data = response.json()

        # print(json.dumps(data, indent=4))

        try:
            matches = data["approximateGroup"]["candidate"]

            for match in matches:
                if match["source"].lower() == "rxnorm":
                    return [match['name'],match['rxcui']]
        except KeyError:
            return None

# do the drug checking via api, return a dictionary of interactions from one source only.

def interaction_check(drug_list, source):
# create a list of values rxcui and join them with '+' delim
    rxcui_list = list()
    delim = "+"
    for key in drug_list:
        rxcui_list.append(drug_list[key])

    rxcui_search = delim.join(rxcui_list)

    search = f"https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={rxcui_search}"

    response = requests.get(search)

    if response.status_code == 200:

        data = response.json()
        data = data.get("fullInteractionTypeGroup")

        interactions_dict = dict()

        for i in data:
            if i["sourceName"].lower() == source:

                intPairs = list()

                for inter in i['fullInteractionType']:
                    intPairs.append(inter['interactionPair'])

                for inter in intPairs:

                    drug1 = (inter[0]['interactionConcept'][0]["minConceptItem"]["name"]).upper()
                    drug2 = (inter[0]['interactionConcept'][1]["minConceptItem"]["name"]).upper()

                    severity = f"{inter[0]['severity'].upper()} severity"

                    if severity == "N/A severity":
                        severity = ""

                    if source == "onchigh":
                        interactions_dict[f"{drug1} and {drug2}"] = f"{severity} interaction(s): {inter[0]['description']}"

                    elif source == "drugbank":
                        interactions_dict[f"{drug1} and {drug2}"] = f"{inter[0]['description']}"

        return interactions_dict



if __name__ == "__main__":
    main()