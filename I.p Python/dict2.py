
# Example of dictionaries and JSON files

import random
import sys
import json

def mkTelDict(n):
    """Build a dictionary of <n> random telephone numbers for <n> random first-names."""
    tel_dict = dict();
    for i in range(n):
        no = random.randint(1000,9999)
        name = names[random.randint(0,99)]
        tel_dict[name]=no

    return tel_dict

def ppTelDict(tel):
    """Pretty print a phone dictionary."""
    for k, v in tel.items():
        print(k, " -&gt; ", v)

def printNoOf(name,tel):
  """Print phone number of <name> in dictionary <tel>, or sorry message."""
  if name in tel:
      print("The tel no. of "+name+" is ", tel[name])
  else:
      print("No phone number for "+name+", sorry!")

# -----------------------------------------------------------------------------
# Constants:

# List of male first names
names = [  "Jack"
         , "Thomas"
         , "Joshua"
         , "Oliver"
         , "Harry"
         , "James"
         , "William"
         , "Samuel"
         , "Daniel"
         , "Charlie"
         , "Benjamin"
         , "Joseph"
         , "Callum"
         , "George"
         , "Jake"
         , "Alfie"
         , "Luke"
         , "Matthew"
         , "Ethan"
         , "Lewis"
         , "Jacob"
         , "Mohammed"
         , "Dylan"
         , "Alexander"
         , "Ryan"
         , "Adam"
         , "Tyler"
         , "Harvey"
         , "Max"
         , "Cameron"
         , "Liam"
         , "Jamie"
         , "Leo"
         , "Owen"
         , "Connor"
         , "Harrison"
         , "Nathan"
         , "Ben"
         , "Henry"
         , "Archie"
         , "Edward"
         , "Michael"
         , "Aaron"
         , "Muhammad"
         , "Kyle"
         , "Noah"
         , "Oscar"
         , "Lucas"
         , "Rhys"
         , "Bradley"
         , "Charles"
         , "Toby"
         , "Louis"
         , "Brandon"
         , "Isaac"
         , "Reece"
         , "Kieran"
         , "Alex"
         , "Finlay"
         , "Finley"
         , "Mason"
         , "Kai"
         , "Logan"
         , "Riley"
         , "Freddie"
         , "David"
         , "Harley"
         , "Jayden"
         , "Mohammad"
         , "Kian"
         , "Bailey"
         , "Sam"
         , "Joel"
         , "Leon"
         , "John"
         , "Robert"
         , "Ellis"
         , "Joe"
         , "Luca"
         , "Billy"
         , "Corey"
         , "Ashton"
         , "Evan"
         , "Taylor"
         , "Christopher"
         , "Aidan"
         , "Elliot"
         , "Hayden"
         , "Morgan"
         , "Jay"
         , "Dominic"
         , "Theo"
         , "Zachary"
         , "Sean"
         , "Sebastian"
         , "Reuben"
         , "Andrew"
         , "Gabriel"
         , "Frederick"
         , "Ewan" ]

jfile = 'tel.json';

if (len(sys.argv) != 2): # expect 1 args: n
  print("Usage: dict2.py <int>\n build a phone dictionary with <n> entries and write it to a JSON file")
else:
  n = int(sys.argv[1])
  # tel = dict([('guido', 4127), ('jack', 4098)])
  tel = mkTelDict(n)
  ppTelDict(tel)
  
  json.dump(tel, fp=open(jfile,'w'), indent=2)
  print("Data has been written to file ", jfile);

  tel_new = json.loads(open(jfile,'r').read())
  ppTelDict(tel_new)

  #print(tel_new)
  #type (tel_new)
  # tel_new = json.loads(jfile);
  # records = [ json.loads(line) for line in open(jfile) ];
  # for rec in records:
  #     tel_new[rec[0]] = rec[1];

  the_name = "Billy"
  printNoOf(the_name,tel_new);
  the_name = names[random.randint(0,99)];
  printNoOf(the_name,tel_new);