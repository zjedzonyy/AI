import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters
    

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Iterate over each variable and its assigned domain
        for variable, domain in self.domains.items():
            # Check if the word length matches the variable's length requirement
            for word in list(domain):
                if len(word) != variable.length:
                    # Remove words that don't match the length requirement
                    self.domains[variable].remove(word)

        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made. 
        """
        #DONE
        updated = False
        overlap = self.crossword.overlaps.get((x, y))  
        if overlap:
            overlap_x, overlap_y = overlap
            # Check each word in variable_x's domain
            for word_x in list(self.domains[x]):
                match_found = False
                # Compare with words in variable_y's domain
                for word_y in list(self.domains[y]):
                    if word_x != word_y and word_x[overlap_x] == word_y[overlap_y]:
                        match_found = True
                        break
                if not match_found:
                    # Remove the word from variable_x if no match found
                    self.domains[x].remove(word_x)
                    updated = True
        return updated    


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # Initialize queue with all possible arcs
            queue = [item for item in self.crossword.overlaps.items() if item[1] is not None and len(item[0]) == 2 and all(isinstance(i, Variable) for i in item[0])]
            while queue:
                pair = queue.pop(0)
                overlap = pair[1]
                (x, y) = pair[0]
                if self.revise(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    # Enqueue all neighbors except variable_y for consistency check
                    for z in self.crossword.neighbors(x):
                        if z != y:                        
                            for i in self.crossword.overlaps.items():
                                if i[0] == (z,x) or i[0] == (x,z):
                                    overlap = i[1]
                            queue.append(((z, x), overlap))
            return True
        
        else:
            queue = arcs
            while queue:
                x, y = queue.pop(0)
                for i in self.crossword.overlaps.items():
                    if i[0] == (x, y) or i[0] == (y, x):
                        overlap = i[1]
                if self.revise(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    for z in self.crossword.neighbors(x):
                        if z != y:                        

                            for i in self.crossword.overlaps.items():
                                if i[0] == (z,x) or i[0] == (x,z):
                                    overlap = i[1]
                            queue.append(((z, x), overlap))
            return True
            



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
            
        return True
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Ensure all values are unique
        values = list(assignment.values())
        unique_values = set(values)

        if len(values) > len(unique_values):
            return False
        
        # Ensure every value is the correct length
        for var, value in assignment.items():
            if len(value) != var.length:
                return False
        
        # Ensure there are no conflicts between neighboring variables
        for var in assignment:
            for neigbhor in self.crossword.neighbors(var):
                if neigbhor in assignment:
                    i, j = self.crossword.overlaps[var, neigbhor]
                    if assignment[var][i] != assignment[neigbhor][j]:
                        return False
            
        return True
            

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = list(self.domains[var])
        neighbors = [neighbor for neighbor in self.crossword.neighbors(var) if neighbor not in assignment]
        counts = {word_x: 0 for word_x in values}

        # Count how many options each word eliminates for each neighbor
        for word_x in values:
            for neighbor in neighbors:
                overlap = self.crossword.overlaps.get((var, neighbor))
                if overlap:
                    overlap_x, overlap_y = overlap
                    for word_y in list(self.domains[neighbor]):
                        if word_x != word_y and word_x[overlap_x] == word_y[overlap_y]:
                            counts[word_x] += 1
        # Sort words by least eliminations to most
        sorted_values = sorted(values, key=lambda word_x: counts[word_x], reverse=True)

        return sorted_values        


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = [var for var in self.crossword.variables if var not in assignment]
        if not unassigned_vars:
            return None

        best_var = None
        smallest_domain_size = float('inf')
        highest_degree = -1

        for var in unassigned_vars:
            domain_size = len(self.domains[var])
            degree = len(self.crossword.neighbors(var))  
            # Choose var with smallest domain or highest degree among those with smallest domain
            if domain_size < smallest_domain_size or (domain_size == smallest_domain_size and degree > highest_degree):
                best_var = var
                smallest_domain_size = domain_size
                highest_degree = degree

        return best_var


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment) and self.consistent(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        if var is not None:
            for value in self.order_domain_values(var, assignment):
                if value not in assignment.values():
                    assignment[var] = value
                    result = self.backtrack(assignment)
                    if result is not False:
                        return result
            assignment[var] = None

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
