#! /usr/bin/env python
# encoding: utf-8

# Toby Thurston -- 08 Apr 2010 

import vim
import decimal
from decimal_tools import * # so that our methods override those in decimal 
import re

def tokens_from(s):
    """Get commands, numbers, and operators from user input.

    This elaborate scheme turns user input into a stream of tokens and 
    allows the user to omit as many spaces as possible.  
    So "2 3+" produces "['2', '3', '+']"
    and "5sqrt" produces "['5', 'sqrt']"
    etc.

    Numbers, plain words, and unicode chars get pushed out first, 
    and for mixed input (like 5sqrt) we resort to a mini-tokenizer.

    There's an accidental felicity here because find() returns -1
    on failure so anything not in alphabet gets the type of the
    final character in it. 
    a=words
    n=numbers
    o=other or operators with one character
    d=doubletons (eg ** ++ //) 
    x=exit chars (as many as you like)

    5.830951894845300470874152878

    """
    tokens = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890.-+*^/@#=%&!?:;,|<>~ "'
    typecast = 'aaaaaaaaaaaaaaaaaaaaaaaaaannnnnnnnnnnoddodooxoooooooooooso'
    for w in s.split():
        if looks_like_a_number(w): 
            tokens.append(w)
        elif re.match(r'^[a-z]+$', w): 
            tokens.append(w)
        elif w in ["∑", "π"]:
            tokens.append(w) # because the trick with the alphabet only works with single byte chars
        else:
            last_type = 's'
            t = ""
            for c in w:
                c_type = typecast[alphabet.find(c)]
                if   last_type == 's': t=c
                elif last_type == 'a' and c_type == 'a': t+=c
                elif last_type == 'n' and c_type == 'n': t+=c
                elif last_type == 'x' and c_type == 'x': t+=c
                elif last_type == 'd' and c_type == 'd': 
                    tokens.append(t+c)
                    t=''
                    c_type = 's'
                elif c_type == 'o':
                    if t!='': 
                        tokens.append(t)
                        t=''
                    tokens.append(c)
                    c_type = 's'
                else:
                    if t!='':
                        tokens.append(t)
                    t=c
                last_type = c_type 
            if t != '':
                tokens.append(t)
    return tokens

def looks_like_an_expr(s): return False

stack = []
want_more = 1
msg = ''
while want_more:
    prompt = msg + '----------\n' + '\n'.join(map(str, stack[:])) + '\nMaynard: '
    msg = ''
    vim.command("redraw!")
    vim.command("let expr = input('" + prompt + "')")
    user_input = vim.eval('expr')
    if user_input == None: break
    if user_input == "": user_input = "dup"

    for token in tokens_from(user_input):
        if re.match(r'\A=+\Z',token):
            for x in stack[-len(token):]:
                vim.command("normal I" + str(x) + "\n")
        elif looks_like_a_number(token): stack.append(decimal.Decimal(token))
        elif looks_like_an_expr(token):  stack.append(decimal.Decimal(str(eval(token))))
        elif token in ["pi", "π"]:  stack.append(pi())
        elif token in ["e"]:        stack.append(exp(decimal.Decimal(1)))
        elif token in ["+", 'add' ]: a=stack.pop();stack.append(stack.pop()+a)
        elif token in ["*", "mul" ]: a=stack.pop();stack.append(stack.pop()*a)
        elif token in ["-", "sub" ]: a=stack.pop();stack.append(stack.pop()-a)
        elif token in ["/", "div" ]: a=stack.pop();stack.append(stack.pop()/a)
        elif token in ["**", "^", "pow" ]: a=stack.pop();b=stack.pop();stack.append(pow(b,a))
        elif token in ["q", "sqrt"]: a=stack.pop();stack.append(a.sqrt())
        elif token in ["c", "neg" ]: a=stack.pop();stack.append(-a)
        elif token in ["v", "inv" ]: a=stack.pop();stack.append(1/a)
        elif token in ["sin"]:       a=stack.pop();stack.append(sin(a))
        elif token in ["cos"]:       a=stack.pop();stack.append(cos(a))
        elif token in ["tan"]:       a=stack.pop();stack.append(sin(a)/cos(a))
        elif token in ["ln"]:        a=stack.pop();stack.append(ln(a))
        elif token in ["exp"]:       a=stack.pop();stack.append(exp(a))
        elif token in ["∑", "sum"]: stack = [ sum(stack[:]) ]
        elif token in [ "dup"  ]: a=stack.pop(); stack.append(a); stack.append(a)
        elif token in [ "trip" ]: a=stack.pop(); stack.append(a); stack.append(a); stack.append(a)
        elif token in [ "dupp" ]: a=stack.pop();b=stack.pop();stack.append(a);stack.append(b);stack.append(a);stack.append(b)
        elif token in [  "vat" ]: a=stack.pop();stack.append(a); stack.append(a*7/40)
        elif token in [ "xvat" ]: a=stack.pop();stack.append(a*40/47);stack.append(a*7/47)
        elif token in ["o", "over"]: a=stack.pop();b=stack.pop();stack.append(b);stack.append(a);stack.append(b)
        elif token in ["x", "swap"]: a=stack.pop();b=stack.pop();stack.append(a);stack.append(b)
        elif token in ["r", "rot" ]: a=stack.pop();b=stack.pop();c=stack.pop(); stack = stack + [ b, a, c ]
        elif token in ["p", "pop" ]: a=stack.pop()
        elif token == "?": 
            msg = """Brother Maynard - a simple RPN calculator for VIM in Python
                  Use it a bit like an HP calculator, ie 2 2 + will produce 4
                  <Esc> to finish; "=" copies the "top" of the stack to your current buffer.
                  "... and the number of the counting shall be three."
                  """
        else: 
            msg = "Ignored >>" + token + "<<\n"
