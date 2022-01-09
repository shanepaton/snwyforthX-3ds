import sys

def compilem() -> None:
    global compile_mode
    compile_mode = True

def semic() -> None:
    global compile_mode, word_accumulator
    compile_mode = False
    w = word_accumulator[1:]

    def exec_word() -> None:
        for word in w:
            process_fragment(word)

    dictionary[word_accumulator[0]] = exec_word
    word_accumulator = []

def get_next() -> str | None:
    if len(input_stack) != 0:
        return input_stack.pop(0)
    else:
        return None

def forth_call() -> None:
    call = call_stack[-1]
    dictionary[call]()
    call_stack.pop()

def process_fragment(word: str) -> None:
    if word in dictionary.keys():
        call_stack.append(word)
        forth_call()
    else:
        if word[-1] == '\'':
            data_stack.append(word[:-1])
        elif word[-1] == '&':
            data_stack.append(dictionary[word[:-1]])
        else:
            if word.isnumeric():
                data_stack.append(float(word))
            else:
                print(word)
                raise Exception('?')

def forth_exec() -> None:
    word = get_next()
    while word is not None:
        if compile_mode and word != ';':
            word_accumulator.append(word)
        else:
            process_fragment(word)
        word = get_next()

def get_name(val) -> str:
    for key, value in dictionary.items():
        if val == value:
            return key
    return "(anonymous)"

def write_e() -> list:
    li = []
    w = get_next()
    while w != ']':
        if w == '[':
            li.append(write_e())
        else:
            li.append(w)
        w = get_next()
    return li

def process_e(e) -> None:
    for i in e:
        process_fragment(i)

def bind() -> None:
    v = data_stack.pop()
    dictionary[data_stack.pop()] = lambda: data_stack.append(v)

def throw() -> None:
    raise Exception(data_stack.pop())

def dup() -> None:
    v = data_stack.pop()
    data_stack.append(v)
    data_stack.append(v)

def drop() -> None:
    data_stack.pop()

def swap() -> None:
    a = data_stack.pop()
    b = data_stack.pop()
    data_stack.append(a)
    data_stack.append(b)

def loop() -> None:
    body = data_stack.pop()
    count = data_stack.pop()
    for i in range(0, count):
        data_stack.append(i)
        process_e(body)

def while_l() -> None:
    body = data_stack.pop()
    while data_stack.pop():
        process_e(body)

input_stack = []
data_stack = []
call_stack = []
compile_mode = False
word_accumulator = []
dictionary = {'.': lambda: print(data_stack.pop()),
              'emit': lambda: print(chr(data_stack.pop())),
              '+': lambda: data_stack.append(data_stack.pop() + data_stack.pop()),
              '-': lambda: data_stack.append(data_stack.pop() - data_stack.pop()),
              '*': lambda: data_stack.append(data_stack.pop() * data_stack.pop()),
              '/': lambda: data_stack.append(data_stack.pop() / data_stack.pop()),
              '%': lambda: data_stack.append(data_stack.pop() % data_stack.pop()),
              ':': compilem,
              ';': semic,
              '#t': lambda: data_stack.append(True),
              '#f': lambda: data_stack.append(False),
              'throw': throw,
              '[': lambda: data_stack.append(write_e()),
              'if': lambda: process_e(data_stack.pop()) if data_stack.pop() else data_stack.pop(),
              'bind': bind,
              'input':lambda: data_stack.append(input()),
              'dup': dup,
              'drop': drop,
              'swap': swap,
              'nil': lambda: data_stack.append(None),
              'loop': loop,
              'bye': lambda: print('bye') or exit(0),
              'while': while_l,
              '=': lambda: data_stack.append(data_stack.pop() == data_stack.pop()),
              '!=': lambda: data_stack.append(data_stack.pop() != data_stack.pop()),
              'and': lambda: data_stack.append(data_stack.pop() and data_stack.pop()),
              'or': lambda: data_stack.append(data_stack.pop() or data_stack.pop()),
              'not': lambda: data_stack.append(not data_stack.pop())}

def main() -> None:
    global input_stack, call_stack
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as file:
            input_stack = file.read().replace('\n', ' ').split(' ')
        try:
            forth_exec()
        except EOFError:
            print('bye')
            exit(0)
        except KeyboardInterrupt:
            print('bye')
            exit(0)
        except Exception as e:
            print(str(e))
            for j in call_stack:
                print('\t', j)
            exit(1)
    else:
        i = 0
        while True:
            try:
                input_stack = input('sf[' + str(i) + ']> ').split(' ')
                i += 1
                forth_exec()
                print('ok')
            except EOFError:
                print('bye')
                exit(0)
            except KeyboardInterrupt:
                print('bye')
                exit(0)
            except Exception as e:
                print(str(e))
                for j in call_stack:
                    print('\t', j)
                call_stack = []

if __name__ == "__main__":
    main()
