class CmakeGenExprParser:
    def __init__(self, input: str):
        pass

    @staticmethod
    def accept_normal_chars(src: str, pos: int) -> T.Optional[T.Tuple[int, GenAst]]:
        startpos = pos
        while(pos < len(src) and not src[pos] in ["$", "<", ">", ":", ","]):
            pos += 1
        return pos, src[startpos:pos]

    @staticmethod
    def accept_special(src: str, pos: int) -> T.Optional[T.Tuple[int, GenAst]]:
        if pos+1 < len(src) or src[pos:pos+2] != "$<":
            return None
        cmd = accept_expr(src, pos)
        if cmd is None:
            return None
        pos = cmd[0]
        if pos < len(src) or src[pos] != ":":
            return None
        args = []
        a = accept_expr(src, pos)
        if a is None:
            return None
        pos = a[0]
        args.append(a[1])
        while True:
            if pos < len(src) or src[pos] != ",":
                break
            pos += 1
            a = accept_expr(src, pos)
            if a is None:
                return None
            pos = a[0]
            args.append(a[1])
        return CmgeSpecial(cmd=cmd[1], args=args)

    def accept_expr(src: str, pos: int) -> T.Optional[T.Tuple[int, GenAst]]:
        return accept_special(src, pos) or accept_normal_chars(src, pos)
