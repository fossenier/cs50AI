import sys

from crossword import *
from typing import Dict, List, Tuple


class CrosswordCreator:

    def __init__(self, crossword: Crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
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
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()

        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self) -> None:
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            inconsistent_words = set()
            for word in self.domains[var]:
                if len(word) != var.length:
                    inconsistent_words.add(word)
            self.domains[var].difference_update(inconsistent_words)

    def revise(self, x: Variable, y: Variable) -> bool:
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        # There is nothing to revise.
        if not overlap:
            return revised

        # (i, j), where v1's ith character overlaps v2's jth character.
        i, j = overlap
        y_letters = set()
        inconsistent_words = set()
        for word in self.domains[y]:
            y_letters.add(word[j])
        for word in self.domains[x]:
            if word[i] not in y_letters:
                inconsistent_words.add(word)

        # Revise the domain
        if len(inconsistent_words) > 0:
            revised = True
            self.domains[x].difference_update(inconsistent_words)
        return revised

    def ac3(self, arcs: List[Tuple[Variable, Variable]] = None) -> bool:
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = (
            arcs
            if arcs
            else [(x, y) for (x, y), flag in self.crossword.overlaps.items() if flag]
        )
        while len(queue) > 0:
            x, y = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for var in self.crossword.neighbors(x):
                    if var != y:
                        queue.append((var, x))
        return True

    def assignment_complete(self, assignment: Dict[Variable, str]) -> bool:
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        variables = set()
        for var in assignment:
            variables.add(var)
            value = assignment[var]
            # A variable has an incomplete assignment.
            if not value:
                return False

        # At least one variable is not yet assigned.
        if variables != set([var for var in self.domains]):
            return False
        return True

    def consistent(self, assignment: Dict[Variable, str]) -> bool:
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        seen_values = set()
        for var, word in assignment.items():
            # This word is not unique.
            if not word or word in seen_values:
                return False
            # An improper length is being used.
            elif len(word) != var.length:
                return False
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                # Check to see if the neighbor has an assigned word
                try:
                    v2_word = assignment[neighbor]
                except KeyError:
                    # No word, and thus consistent.
                    continue
                i, j = self.crossword.overlaps[var, neighbor]
                # An inconsistency in placed words has occurred.
                if word[i] != v2_word[j]:
                    return False
            seen_values.add(word)
        return True

    def order_domain_values(
        self, var: Variable, assignment: Dict[Variable, str]
    ) -> str:
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # TODO implement, this is first slice
        return list(self.domains[var])

    def select_unassigned_variable(self, assignment: Dict[Variable, str]) -> Variable:
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # TODO implement, this is first slice
        for var in self.domains:
            if var not in assignment:
                return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]
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
