from html.parser import HTMLParser
import sys

DEBUG = False

class CustomHTMLParser(HTMLParser):
    start = False
    tag_struct = []
    frame_stack = []
    stack = []
    decompiled_code = ["window = globals()", "globalThis = globals()"]
    indent = 0
    ret_count = 0

    def wrap_indent(self, s):
        return "   " * self.indent + s

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tag_struct.append(tag)
        if tag == "main":
            self.start = True
            self.stack.append([])

        if self.start:
            # print("Encounter a start tag", tag)
            self.frame_stack.append([])
            if attrs != []:
                attrmap = {}
                for attr in attrs:
                    (k, v) = attr
                    attrmap[k] = v
                # check for id. we add a comment line specifically for id in order to navigate
                if "id" in attrmap and tag != "dfn":
                    code = self.wrap_indent(f"# LOC: {attrmap['id']}")
                    if DEBUG:
                        print(code)
                    self.decompiled_code.append(code)
                match tag:
                    case "data":
                        assert "value" in attrmap
                        self.frame_stack[-1].append(int(attrmap["value"]))
                    case "dfn":
                        assert "id" in attrmap
                        fn_name = attrmap["id"]
                        code = self.wrap_indent(f"def {fn_name}(*args):")
                        self.indent += 1
                        self.stack.append([])
                        if DEBUG:
                            print(code)
                        self.decompiled_code.append(code)
                    case "var":
                        assert len(attrs) == 1
                        assert "title" in attrmap
                        current_stack = self.stack[-1]
                        code = ""
                        varname = attrmap["title"]
                        if len(current_stack) == 0:
                            code = self.wrap_indent(f"(*lst, {varname}) = lst")
                        else:
                            code = self.wrap_indent(f"{varname} = {current_stack[-1]}")
                            current_stack.pop()
                        if DEBUG:
                            print(code)
                        self.decompiled_code.append(code)
                    case "a":
                        assert len(attrs) >= 1
                        assert "href" in attrmap
                        if attrmap["href"].startswith("javascript:"):
                            assert attrmap["href"].endswith("()")
                            fn_name = attrmap["href"][11:-2]
                            if "target" in attrmap:
                                assert attrmap["target"] == "_top"
                                current_stack = self.stack[-1]
                                assert len(current_stack) >= 1
                                current_frame = self.frame_stack[-1]
                                # put into frame stack as args are not confirmed
                                current_frame.append(f"{current_stack[-1]}.{fn_name}")
                                current_stack.pop()
                            else:
                                current_frame = self.frame_stack[-1]
                                current_frame.append(f"{fn_name}")
                            # create a new stack for <a>
                            self.stack.append([])
                        else:
                            assert attrmap["href"].startswith("#")
                            loc = attrmap["href"][1:]
                            code = self.wrap_indent(f"goto {loc}")
                            if DEBUG:
                                print(code)
                            self.decompiled_code.append(code)
                    case "cite":
                        # this should not happen, should be just id
                        assert len(attrs) == 1
                        assert attrs[0][0] == "id"
                    case _:
                        print("Unhandled attr", tag, attrs)
                        input()
            else:
                match tag:
                    case "i":
                        # if
                        current_stack = self.stack[-1]
                        assert len(current_stack) >= 1
                        code = self.wrap_indent(f"if {current_stack[-1]}:")
                        if DEBUG:
                            print(code)
                        current_stack.pop()
                        self.decompiled_code.append(code)
                        # duplicate a stack for the inside if
                        self.stack.append([i for i in current_stack])
                        self.indent += 1
                    case "table":
                        # object, create a new stack = [keyArray, valArray] for it
                        self.stack.append([[], []])
                    case "ol":
                        # table, create a new stack val array
                        self.stack.append([])
                    case _:
                        # assume no attrs dont need to handle
                        return

    def handle_endtag(self, tag: str) -> None:
        if self.start:
            current_frame = self.frame_stack[-1]
            current_stack = self.stack[-1]
            match tag:
                case "cite":
                    assert len(current_frame) == 1
                    current_stack.append(current_frame[0])
                case "samp":
                    assert len(current_stack) >= 2
                    assert len(current_frame) == 1
                    prop = current_frame[0]
                    val = current_stack[-1]
                    obj = current_stack[-2]
                    code = self.wrap_indent(f'{obj}["{prop}"] = {val}')
                    if DEBUG:
                        print(code)
                    self.decompiled_code.append(code)
                    current_stack.pop()
                    current_stack.pop()
                case "data":
                    current_stack.append(current_frame[0])
                case "var":
                    assert len(current_frame) == 0
                case "s":
                    assert len(current_frame) <= 1
                    val = "" if len(current_frame) == 0 else current_frame[0]
                    current_stack.append(f'"{val}"')
                case "a":
                    assert len(current_frame) <= 1
                    if len(current_frame) == 1:
                        fn_name = current_frame[0]
                        args = ", ".join(list(map(str, current_stack)))
                        code = self.wrap_indent(f"_result{self.ret_count} = {fn_name}({args})")
                        if DEBUG:
                            print(code)
                        self.decompiled_code.append(code)
                        self.stack.pop()
                        self.stack[-1].append(f"_result{self.ret_count}")
                        self.ret_count += 1
                    else:
                        # this is the goto case, for now disregard it
                        pass
                case "i":
                    # clean up the duplicated stack
                    self.stack.pop()
                    self.indent -= 1
                case "rp":
                    assert len(current_frame) == 1
                    prop = current_frame[0]
                    current_stack[-1] = f"{current_stack[-1]}.{prop}"
                case "rt":
                    code = ""
                    if len(current_stack) >= 1:
                        value = current_stack[-1]
                        code = self.wrap_indent(f"return {value}")
                    else:
                        code = self.wrap_indent(f"return")
                    if DEBUG:
                        print(code)
                    self.decompiled_code.append(code)
                    # I dont need to clean up stack, as I can cleanup it in end of dfn block
                case "dfn":
                    self.indent -= 1
                    self.stack.pop()
                case "bdi":
                    assert len(current_frame) == 0
                    assert len(current_stack) >= 1
                    val = current_stack[-1]
                    if " " in val:
                        val = f"({val})"
                    current_stack[-1] = f"not {val}"
                case "tr":
                    # tr should be irrelevant
                    pass
                case "table":
                    assert len(current_stack) == 2
                    (keyArr, valArr) = current_stack
                    obj = {}
                    for i in range(len(keyArr)):
                        obj[keyArr[i]] = valArr[i]
                    self.stack.pop()
                    self.stack[-1].append(obj)
                case "ol":
                    arr = [i for i in current_stack]
                    self.stack.pop()
                    self.stack[-1].append(arr)
                case "dd":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    operand1 = current_stack[-2]
                    if type(operand1) == str and " " in operand1:
                        operand1 = f"({operand1})"
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{operand1} + {operand2}")
                case "sub":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    operand1 = current_stack[-2]
                    if type(operand1) == str and " " in operand1:
                        operand1 = f"({operand1})"
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{operand1} - {operand2}")
                case "ul":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack[-1] = f"{current_stack[-1]} * {operand2}"
                case "address":
                    assert len(current_stack) >= 2
                    idx = current_stack[-1]
                    arr = current_stack[-2]
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{arr}[{idx}]")
                case "ins":
                    assert len(current_stack) >= 3
                    val = current_stack[-1]
                    idx = current_stack[-2]
                    arr = current_stack[-3]
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.pop()
                    code = self.wrap_indent(f"{arr}[{idx}] = {val}")
                    if DEBUG:
                        print(code)
                    self.decompiled_code.append(code)
                case "small":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    operand1 = current_stack[-2]
                    if type(operand1) == str and " " in operand1:
                        operand1 = f"({operand1})"
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{operand1} < {operand2}")
                case "big":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    operand1 = current_stack[-2]
                    if type(operand1) == str and " " in operand1:
                        operand1 = f"({operand1})"
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{operand1} > {operand2}")
                case "em":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    operand1 = current_stack[-2]
                    if type(operand1) == str and " " in operand1:
                        operand1 = f"({operand1})"
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{operand1} == {operand2}")
                case "b":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    operand1 = current_stack[-2]
                    if type(operand1) == str and " " in operand1:
                        operand1 = f"({operand1})"
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{operand1} and {operand2}")
                case "bdo":
                    assert len(current_stack) >= 2
                    operand2 = current_stack[-1]
                    operand1 = current_stack[-2]
                    if type(operand1) == str and " " in operand1:
                        operand1 = f"({operand1})"
                    if type(operand2) == str and " " in operand2:
                        operand2 = f"({operand2})"
                    current_stack.pop()
                    current_stack.pop()
                    current_stack.append(f"{operand1} or {operand2}")
                case "dt":
                    assert len(current_stack) >= 1
                    current_stack.append(current_stack[-1])
                case "main":
                    pass
                case "li":
                    # should not relevant
                    pass
                case _:
                    print("tag unimplemented", tag)
                    input()
            self.frame_stack.pop()
        assert self.tag_struct[-1] == tag
        self.tag_struct.pop()

        if tag == "main":
            self.start = False
    
    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.start:
            print("startend tag unimplemented", tag)

    def handle_data(self, data: str) -> None:
        if data.strip() == "":
            return
        if self.start:
            self.frame_stack[-1].append(data.strip())
    
    def decompile(self) -> str:
        return "\n".join(self.decompiled_code)



f = open(sys.argv[1], 'r')
raw = f.read()
f.close()

parser = CustomHTMLParser()
parser.feed(raw)
print(parser.decompile())
