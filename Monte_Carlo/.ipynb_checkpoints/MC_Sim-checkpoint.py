import numpy as np
import pandas as pd

class Die():
    """
    A class representing a die with customizable faces and weights.
    
    The die has N sides ("faces") and W weight. W defaults to 1.0
    for each face, but can be changed after the object is created. 
    Each side has an associated weight that affects the probability
    of rolling a certain side. The faces must be unique and stored in
    a numpy array. 
    
    Attributes:
    sides (numpy.ndarray): Array of unique face values for the die
    die (pandas.DataFrame): DataFrame storing faces as index and their weights

    Methods:
    change_face_weight(face, new_weight): Changes the weight of a specific face
    roll_die(r=1): Rolls the die r times and returns results
    die_state(): Prints current state of die faces and weights
    """
    
    
    def __init__(self, sides):
        """
        Initializes the die with given sides and default weight of 1.0
        for each side.
        
        Parameters:
            sides: numpy.ndarray
                An array of unique face values.
            
        Raises:
            TypeError: If input is not a NumPy array.
            ValueError: If face values are not unique.
        """
        
        self.sides = sides
        # if it is a numpy array#
        if isinstance(sides, np.ndarray):
            # test for uniqueness#
            if len(self.sides) == len(set(self.sides)):
                # set up weights variable#
                weights = np.array([1])
                # make weights same length as sides#
                while len(weights) < len(self.sides):
                    weights = np.append(weights, 1)
                # set up dataframe#
                self.die = pd.DataFrame({'Faces': self.sides, 'Weight': weights})
                self.die.set_index('Faces', inplace=True)
            else:
                raise ValueError('The array has repeated sides')
        else:
            raise TypeError('Sides is not a numpy array')
            
    def change_weight(self, face, new_weight):
        """
        Changes the weight of a specific face on the die.
        
        Parameters:
            face: the face value to modily as long as it exists in the face array.
            new_weight: the new weight assigned to a face (float or int)
            
        Raises:
            IndexError: If the face is not found.
            TypeError: If the weight is not numeric.
            ValueError: If the weight is negative.
        """
        
        if face not in self.sides:
            raise IndexError("Face not found on die")

        try:
            new_weight = float(new_weight)
        except (ValueError, TypeError):
            raise TypeError("The weight must be numeric or castable to float.")

        if new_weight < 0:
            raise ValueError("The weight must be non-negative.")

        self.die.loc[face, 'Weight'] = new_weight
        
    def roll_die(self, roll=1):
        """
        Rolls the die one or more times.
        
        Parameters:
            n: int, optional
                number of times to roll the die (default is 1 roll).
            
        Returns:
            list: Outcome of the die rolls based on face weight.
        
        """
        probs = self.die['Weights'] / self.die['Weights'].sum()
        die_roll = list(np.random.choice(self.die.index, size=roll, p=probs))
        return die_roll
    
    def show_die(self):
        """
        Shows the current state for the die.
        
        Returns:
            DataFrame showing the faces and corresponding weights.
        
        """
        
        return self.die.copy()
        
        
        
class Game():
    """
    A class to simulate rolling one or more similar die objects one or more times.
    
    Each die must have the same number of sides and faces, but can have different weights.
    Each game is initialized with a Python list that contains one or more dice.
    Game objects have a behavior to play a game, i.e. to roll all of the dice a given number of times.
    Game objects only keep the results of their most recent play.
    
    Attributes:
        dice (list): A list of Die objects to be used in the game
        results (DataFrame): A DataFrame containing the results of the dice rolls, where each column represents a die and each row represents a roll

    Methods:
        play(n_rolls): Rolls all dice n_rolls times and stores results
        show(form): Returns the results in either 'wide' or 'narrow' format
    """
    
            
    def __init__(self, dice):
        """
        Initialize a new dice game.

        Parameters:
            dice : list
                 A list of Die objects to be used in the game.

        Returns:
            None
            
        """

        self.dice = dice
        self.results = None
        
    def play(self, n_rolls):
        """
        Rolls all dice a given number of time and records the results.
        
        Parameters
            n_rolls: int
                The number of times to roll all the dice.
            
        Returns:
            None: Results are stored in a private data frame.
            
        """
        
        results = {f'die_{i}': die.roll_die(n_rolls) 
                   for i, die in enumerate(self.dice)}
        self.results = pd.DataFrame(results, index=[f'roll_{i + 1}' for i in range(n_rolls)])
        
    def show(self, form = 'wide'):
        """
        Returns a copy of the private play data frame to the user.
        
        Parameters:
            form : str, optional
                Format of the results, either 'wide' or 'narrow' (default is 'wide')
                    - 'wide': Each die roll is a column
                    - 'narrow': Results are melted into a long format with die number and outcome columns

        Returns:
            pandas.DataFrame
                DataFrame containing the results in the specified format

        Raises:
            ValueError
                If no games have been played or if form is not 'wide' or 'narrow'
                
        """
        if self.results is None:
            raise ValueError("No games have been played yet")

        if form == 'wide':
            return self.results
        elif form == 'narrow':
            narrow = self.results.reset_index().melt(id_vars=['Roll'], 
                                                 var_name='Die', 
                                                 value_name='Face')
            return narrow
        else:
            raise ValueError("form must be 'wide' or 'narrow'")
class Analyzer:
    """
    A class to anlayze the results of single game and computes various descriptive statistical properties about it.
    
    Provides methods to compute jackpots, face counts, combinations, and permutations of rolled dice. 
    

    Methods:
        jackpot(): Returns the number of rolls that resulted in all dice showing the same face
        face_counts(): Returns a DataFrame showing the count of each face value per roll
        combo_count(): Returns counts of unique combinations of faces (order doesn't matter)
        permu_count(): Returns counts of unique permutations of faces (order matters)
        
    """    
    
    def __init__(self, game):
        """
        Initializes the analyzer with a game object.
        
        Parameters:
            Game: A  Game objec that has been played.
            
        Raises:
            ValueError: If the passed value is not a Game object.
            
        """
        
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")
            
        self.game = game
        self._results = game.show(form='wide')
        
    def jackpot(self):
        """
        Counts the number of rolls that resulted in Jackpot (all faces are the same).
        
        Returns:
            int: Number of Jackpots.
            
        """
        
        return (self._results.nunique(axis=1) == 1).sum()

    
    def face_counts(self):
        """
        Computes how many times each face appears in each roll.
        
        Returns:
            DataFrame: Index of roll numbers, face values as columns, and values show count of each face in that roll. 
            
        """
        
        return self._results.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)

        
    def combo_count(self):
        """
        Computes distinct combinations of faces rolled and their counts.
        Combos are order-independent and may contain repetitions.
        
        Returns:
            DataFrame: MultiIndex shows distinct combos with a column to count occurrences.
        
        """
        
        df = self.game.show('wide')
        combos = df.apply(lambda x: tuple(sorted(x)), axis=1)
        return combos.value_counts()
    
    def perm_count(self):
        """
        Computes distinct permutations of rolled faces and their frequencies.
        Permutations are order-dependent and may contain repetitions. 
        
        Returns:
            DataFrame: MultiIndex shows distinct permutations with columns showing count of occurrences.
            
        """
        
        df = self.game.show('wide')
        perms = df.apply(tuple, axis=1)
        return perms.value_counts()