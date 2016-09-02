import unittest
import src
import src.ErrorMessagesBuilder.ErrorMessageHandler as Err
import src.ErrorMessagesBuilder.ErrorBuilder.ErrorMessagesConstants as ErrConst
import sys


class TestSkipLineCommand(unittest.TestCase):

    WARNINGS = 'Warnings'

    @classmethod
    def setUpClass(cls):
        cls.error = Err.ErrorMessageHandler()
        cls.indentCheck = src.CheckIndentationCommand()
        if sys.argv[0].endswith('nosetests'):
            cls.filepath_prefix = "./resources/"
        else:
            cls.filepath_prefix = "../resources/"

    def testSkipLineCommandSkipTypo(self):
        config = src.load_config_file()
        src.lexer = src.Lexer(config)
        exp_result = []
        result = src.lexer.lex("'BSLint_skip_line \nxgygu= 22\ny = 4")
        self.assertEqual(exp_result, result[self.WARNINGS])

    def testSkipLineCommandEmptyLine(self):
        config = src.load_config_file()
        src.lexer = src.Lexer(config)
        exp_result = []
        result = src.lexer.lex("'BSLint_skip_line \n\ny = 4")
        self.assertEqual(exp_result, result[self.WARNINGS])

    def testSkipLineCommandWithTypo(self):
        config = src.load_config_file()
        src.lexer = src.Lexer(config)
        exp_result = [self.error.get(ErrConst.TYPO_IN_CODE, [3])]
        result = src.lexer.lex("'BSLint_skip_line \ny=4\nxgygu = 22\n")
        self.assertEqual(exp_result, result[self.WARNINGS])

    def testSkipLineCommandInactive(self):
        config = src.load_config_file(self.filepath_prefix + "config/inactive-skip-line-config.json")
        src.lexer = src.Lexer(config)
        exp_result = [self.error.get(ErrConst.TYPO_IN_CODE, [2])]
        result = src.lexer.lex("'BSLint_skip_line \nxgygu = 22\ny = 4")
        self.assertEqual(exp_result, result[self.WARNINGS])