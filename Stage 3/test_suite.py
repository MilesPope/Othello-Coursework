"""
Module containing tests for core game logic
"""

import unittest
from game_engine import initialise_board, legal_move, outflanked
from game_engine import has_legal_move
from ai_opponent import choose_move, possible_flip_counts

# Test the initialise_board function
class TestInitialiseBoard(unittest.TestCase):
    """
    Test cases for initialise_board
    """

    def test_board_size(self):
        """
        Test that board size is as expected
        """
        board = initialise_board(8)
        self.assertEqual(len(board),8)
        self.assertEqual(len(board[0]),8)

    def test_starting_tokens(self):
        """
        Test the starting tokens are placed correctly
        """
        board = initialise_board(8)
        self.assertEqual(board[3][3], "Light")
        self.assertEqual(board[3][4], "Dark ")
        self.assertEqual(board[4][3], "Dark ")
        self.assertEqual(board[4][4], "Light")

    def test_empty_cells(self):
        """
        Test that there are 60 empty cells represented by none on 8x8
        """
        board = initialise_board()
        none_count = 0
        for x in range(len(board)):
            for y in range(len(board)):
                if board[y][x] is None:
                    none_count += 1
        self.assertEqual(none_count, 60)


class TestLegalMove(unittest.TestCase):
    """
    Test cases for legal_move
    """

    def test_known_legal(self):
        """
        Test a move that is known to be legal
        """
        board = initialise_board()
        self.assertTrue(legal_move("Dark ", (2,3), board))

    def test_occupied(self):
        """
        Test when a move is attempted on an occupied cell
        """
        board = initialise_board()
        self.assertFalse(legal_move("Dark ", (3,3), board))

    def test_no_outflanked(self):
        """
        Test when no peices are outflanked
        """
        board = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.assertFalse(legal_move("Dark ", (1,1), board))

    def test_single_flip(self):
        """
        Test when one token is flipped
        """
        board = [
            [None, None, None, None],
            [None, "Dark ", "Light", None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.assertTrue(legal_move("Dark ", (3,1), board))

    def test_multi_flip(self):
        """Test when multiple tokens should be flipped by move"""
        board = board = [
            [None, None, "Light", None, None],
            [None, "Light", "Dark ", "Light", None],
            ["Light", "Dark ", None, "Dark ", "Light"],
            [None, "Light", "Dark ", "Light", None],
            [None, None, "Light", None, None]
        ]
        self.assertTrue(legal_move("Light", (2,2), board))

    def test_legal_edge(self):
        """
        Test where a legal move is attempted on the edge
        """
        board = [
            [None, "Light", "Dark ", None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None]
        ]
        self.assertTrue(legal_move("Dark ", (0,0), board))

    def test_illegal_edge(self):
        """
        Test where an illegal move is attempted on the edge
        """
        board = [
            [None, "Light", None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None]
        ]
        self.assertFalse(legal_move("Dark ", (0,0), board))
 
    def test_opponent_then_none(self):
        """
        Test when no peices are outflanked due to none in line
        """
        board = [
            [None, "Light", None, "Dark "],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.assertFalse(legal_move("Dark ", (0,0), board))

class TestOutflanked(unittest.TestCase):
    """
    Test functionality of the outflanked function
    """

    def test_single_flip(self):
        """
        Test when a single token is flipped
        """
        board = [
            [None, "Dark ", "Light", None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        outflanked_board = outflanked(board, "Dark ", (3,0))
        self.assertEqual(outflanked_board[0][2], "Dark ")

    def test_multi_flip(self):
        """
        Test multiple tokens can be flipped by one move
        """
        board = [
            [None, None, "Light", None, None],
            [None, "Light", "Dark ", "Light", None],
            ["Light", "Dark ", None, "Dark ", "Light"],
            [None, "Light", "Dark ", "Light", None],
            [None, None, "Light", None, None]
        ]
        outflanked_board = outflanked(board, "Light", (2,2))
        self.assertEqual(outflanked_board[1][2], "Light")
        self.assertEqual(outflanked_board[2][0], "Light")

    def test_corner_flip(self):
        """
        Test where multiple tokens in the same line are flipped on an edge
        """
        board = [
            ["Light", "Dark ", "Dark ", None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        outflanked_board = outflanked(board, "Light", (3,0))
        self.assertEqual(outflanked_board[0][1], "Light")
        self.assertEqual(outflanked_board[0][2], "Light")

class TestHasLegal(unittest.TestCase):
    """
    Test cases for the has_legal_move function
    """
    
    def test_initial(self):
        """
        Test both players can go on initial board
        """
        board = initialise_board()
        self.assertTrue(has_legal_move(board,"Dark "))
        self.assertTrue(has_legal_move(board,"Light"))

    def test_full_board(self):
        """
        Test no legal moves exist on a full board
        """
        board = [
            ["Dark ", "Dark ", "Dark "],
            ["Dark ", "Dark ", "Dark "],
            ["Dark ", "Dark ", "Dark "]
        ]
        self.assertFalse(has_legal_move(board,"Dark "))
        self.assertFalse(has_legal_move(board,"Light"))

    def test_edge_only(self):
        """
        Test where the only legal move is an edge case
        """
        board = [
                [None, "Dark ", "Light", None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None]
            ]
        self.assertTrue(has_legal_move(board,"Dark "))
        
class TestAiOpponent(unittest.TestCase):
    """
    Test functionality of the AI opponent
    """

    def test_returns_legal(self):
        """
        Test that the ai returns a legal move
        """
        board = initialise_board()
        ai_move = choose_move(1, possible_flip_counts(board, "Light"))
        self.assertTrue(legal_move("Light", ai_move, board))

    def test_move_in_possible_set(self):
        """
        Test that the move given by choose move is among the ones in the possible moves
        """
        board = initialise_board()
        ai_move = choose_move(1, possible_flip_counts(board, "Light"))
        possible_moves = possible_flip_counts(board, "Light")
        self.assertIn(ai_move, possible_moves)

    def test_no_moves(self):
        """
        Test none is returned when there are no moves
        """
        board = [
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None],
                [None, None, None, None]
            ]
        ai_move = choose_move(1, possible_flip_counts(board, "Light"))
        self.assertIsNone(ai_move)
        