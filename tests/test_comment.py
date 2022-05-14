import unittest
from pitch.models import Comment

class CommentTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the comment class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_comment = Comment(1,'Test comment for individual pitch')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))
