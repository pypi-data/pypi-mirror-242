from bat_lexer import Lexer
from bat_parser import Parser
from bat_interpreter import interpret
from bat_env import create_global_env


def run():
    env = create_global_env()


    
    
    file = open("test.batsy", "r")
    prompt = file.read()
    lexer = Lexer(prompt)
    parser = Parser(lexer)
    program = parser.produceAST()
    
    results = interpret(program, env)
    

run()
    