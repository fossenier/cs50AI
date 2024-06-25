import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # mines are only known with certainty when in a given area all
        # cells must be a mine
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # similarly, safe tiles  are only known with certainty when in a
        # given area all cells cannot be a mine
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        cell = set(cell)
        # if the mine is a cell in this sentence
        if cell.issubset(self.cells):
            # don't track it anymore and mark that there is one less mine
            self.cells.difference_update(cell)
            self.count -= len(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        cell = set(cell)
        # if the safe tile is a cell in this sentence
        if cell.issubset(self.cells):
            # don't track it anymore
            self.cells.difference_update(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)

        # 3
        cells = self.adjacent_cells(cell)
        # if there are known mines, update the count to be reflect uncertainty
        count -= len(cells.intersection(self.mines))
        # ignore known mines and safe cells
        cells.difference_update(self.mines)
        cells.difference_update(self.safes)
        self.knowledge.append(Sentence(cells, count))

        # 4 & 5
        new_info = True
        while new_info:
            new_info = False
            # mark cells as safe or as mines
            new_info = self.update_sentences()
            # create new inferences
            new_info = self.infer_sentences()

        raise NotImplementedError

    def infer_sentences(self):
        """
        Sentences are inferred using the tactics discussed in the problem definition
        background.
        """
        inferred_sentences = []

        for i, sentence_a in enumerate(self.knowledge):
            for sentence_b in self.knowledge[i:]:
                # skip these sentences if they are the same
                if sentence_a == sentence_b:
                    continue
                # sentence a is a subset of the info in sentence b
                if sentence_a.cells.issubset(sentence_b.cells):
                    inferred_sentences.append(
                        Sentence(
                            sentence_b.cells.difference(sentence_a),
                            sentence_b.count - sentence_a.count,
                        )
                    )
                # sentence b is a subset of the info in sentence a
                if sentence_b.cells.issubset(sentence_a.cells):
                    inferred_sentences.append(
                        Sentence(
                            sentence_a.cells.difference(sentence_b),
                            sentence_a.count - sentence_b.count,
                        )
                    )

        for sentence in inferred_sentences:
            self.knowledge.append(sentence)

        # return True if updates were made
        return len(inferred_sentences) > 0

    def update_sentences(self):
        """
        Cells are marked as safe or as mines based on the sentences in self.knowledge.
        """
        resolved_sentences = []
        for sentence in self.knowledge:
            mines = sentence.known_mines()
            if mines:
                resolved_sentences.append(sentence)
                for cell in mines:
                    self.mark_mine(cell)
            safes = sentence.known_safes()
            if safes:
                resolved_sentences.append(sentence)
                for cell in safes:
                    self.mark_safe(cell)

        for sentence in resolved_sentences:
            self.knowledge.remove(sentence)

        # return True if updates were made
        return len(resolved_sentences) > 0

    def adjacent_cells(self, cell):
        """
        Finds all adjacent valid cells on the board.
        """
        adjacent = set()
        i, j = cell
        for row in range(i - 1, i + 2):
            for col in range(j - 1, j + 2):
                if 0 < row < self.height and 0 < col < self.width:
                    adjacent.add((row, col))

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # find safe moves not yet taken
        unused_safe_moves = self.safes.difference(self.moves_made)
        # none were found
        if unused_safe_moves == set():
            return None
        # return a safe move
        return unused_safe_moves.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            move = (random.randrange(self.height), random.randrange(self.width))
            if move in self.mines:
                continue
            return move
