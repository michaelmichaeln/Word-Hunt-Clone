import pickle

class Profile:
    def __init__(self, name, highscore = 0):
        self.name = name
        self.highScore = highscore
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return f'{self.name}:{self.highScore}'
    def __eq__(self,other):
        if type(other) != Profile:
            return False
        return self.name == other.name

def saveProfiles(existingProfile):
    with open('Profiles_database', 'wb') as file:
            pickle.dump(existingProfile, file)