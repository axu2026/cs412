from django.db import models

# Create your models here.
class Voter(models.Model):
    """class representing a registered voter"""
    first_name = models.TextField()
    last_name = models.TextField()
    date_of_birth = models.DateField()

    address_street_number = models.IntegerField()
    address_street_name = models.TextField()
    address_apt_number = models.TextField(blank=True)
    address_zip_code = models.IntegerField()

    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()
    voter_score = models.IntegerField()

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    def __str__(self):
        """string representation of a voter"""
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        """returns a string of the full address formatted"""
        optional = ''

        # if there is apt number, set optional field to it
        if self.address_apt_number:
            optional = f'APT. {self.address_apt_number}, '

        zip = str(self.address_zip_code)
        if len(zip) == 8:
            zip = zip[:4] + "-" + zip[4:]

        return f'{self.address_street_number} {self.address_street_name}, {optional}0{zip}'
    
def string_to_bool(string):
    """converts a string to its boolean counterpart"""
    return string.lower() == "true"

def load_data():
    """load in voters using voter model from csv file"""
    filename = "newton_voters.csv"
    f = open(filename, 'r')
    f.readline() # waste the title row

    # go through all rows in the file and create a voter
    for line in f:
        # in case of an invalid input or format, catch the error and continue
        try:
            fields = line.strip().split(',')
            voter = Voter(
                first_name = fields[2],
                last_name = fields[1],
                date_of_birth = fields[7],
                address_street_number = fields[3],
                address_street_name = fields[4],
                address_apt_number = fields[5],
                address_zip_code = fields[6],
                date_of_registration = fields[8],
                party_affiliation = fields[9],
                precinct_number = fields[10],
                voter_score = fields[16],
                v20state = string_to_bool(fields[11]),
                v21town = string_to_bool(fields[12]),
                v21primary = string_to_bool(fields[13]),
                v22general = string_to_bool(fields[14]),
                v23town = string_to_bool(fields[15])
            )

            voter.save() # save voter to database
        except Exception as e:
            print(f'ISSUE AT: {line}')
            print(e)