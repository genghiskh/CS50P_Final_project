# Drug Interaction Checker
#### Video Demo:  <URL www.google.com>
#### Description:
This project purpose to get user to input a list of drugs and use the NIH RxNorm API to conduct a drug-drug interaction.

User must enter in at least 2 drugs and the drug must be a valid drug per the NIH API. The program will prompt the user to enter in as many drugs as they would like until they hit "done" or enter without any value.

Steps needed to accomplish this project:


1. Get RXCUI Codes and drug: The program will use this API function: https://lhncbc.nlm.nih.gov/RxNav/APIs/api-RxNorm.getApproximateMatch.html to get the approximate match of a drug name and will return the RXCUI code needed to run the drug interaction checker.
print back the name of the drug entered for user alert user if mismatched occurred and/or remind them what they already entered in. This allows the program to be forgiving of slight mispelling errors or if they type in more data than just the drug ingredient, such as dose and formulation will be accepted.

    Data will be stored as a dictionary with Key value pair being "drug name": RXCUI.

2. When the user is done with adding all the drugs by entering 'done' or empty string a interaction checker function will be called to check the list of RXCUI and return all the matches for interactions. If no interactions are found, it will print as such.

3. DDI API used: https://lhncbc.nlm.nih.gov/RxNav/APIs/api-Interaction.findInteractionsFromList.html
This function will accept a list of RXCUI and return any matches. However, it will check two sources ONCHigh and DRUGBANK.CA and return a JSON file with both data. This will produce similar and/or duplicative results.

A function will create two dictionary one from DRUGBANK and ONCHIGH if either is found and combined them into one. DRUGBANK has a great description for its interactions but no severity rating, conversely ONCHIGH has a severity rating but a limited description of the interaction.
Therefore, the program will combine data based on ONCHIGH first if exsits and merge the description from the DRUGBANK behind the description of ONCHIGH.

There will be times where one interaction is found in one source and not the other so this will also reconcile this.


