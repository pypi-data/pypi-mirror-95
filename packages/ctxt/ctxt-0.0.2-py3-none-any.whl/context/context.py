from functools import wraps
import textwrap
import inspect


def wrap_paragraph(text, width=70):
    return "\n".join(map(lambda s: textwrap.shorten(s, width=width), text.splitlines()))


class Context(object):
    def __init__(
        self,
        auto_wrap_callable=True,
        text_prefix="> ",
        text_width=70,
        text_indent="  ",
        echo_args=False,
        echo_ret=False,
    ):
        self.auto_wrap_callable = auto_wrap_callable
        self.text_prefix = text_prefix
        self.text_indent = text_indent
        self.depth_count = 0
        self.text_width = text_width
        self.echo_args = echo_args
        self.echo_ret = echo_ret

    def wrap(self, f):

        header_call = f"CALL: {f.__name__}"
        header_ret = "-> out"

        @wraps(f)
        def wrapper(*args, **kwargs):
            caller = inspect.getframeinfo(inspect.stack()[1][0])
            caller_info = "%s:%d in %s" % (
                caller.filename,
                caller.lineno,
                caller.function,
            )

            header = f"[{header_call}, FROM: {caller_info}]"

            if self.echo_args:
                header = header + "\n<- in"
                content_call = self.describe_args(*args, **kwargs)
                self.echo(header, content_call)
            else:
                self.echo(header)

            self.depth_count += 1

            ret = f(*args, **kwargs)

            self.depth_count -= 1

            if self.echo_ret:
                ret_tuple = ret if isinstance(ret, tuple) else (ret,)
                content_ret = self.describe_args(*ret_tuple)
                self.echo(header_ret, content_ret)

            return ret

        return wrapper

    def describe_args(self, *args, **kwargs):
        if not self.echo_args:
            return ""

        content = ""
        if args:
            content += "\n".join(map(repr, args))
            if kwargs:
                content += "\n"

        if kwargs:
            content += "\n".join(
                f"{key} = {repr(value)}" for key, value in kwargs.items()
            )

        if content:
            content = textwrap.indent(content, prefix=self.text_prefix)

        return content

    def echo(self, header, content=""):
        if content:
            text = header + ":\n" + content
        else:
            text = header

        text = wrap_paragraph(text, width=self.text_width)
        text = textwrap.indent(text, prefix=self.text_indent * self.depth_count)

        print(text)

    def __call__(self, *args, **kwargs):
        if args and inspect.isfunction(args[0]) and self.auto_wrap_callable:
            return self.wrap(args[0])

        caller = inspect.getframeinfo(inspect.stack()[1][0])
        header = "[%s:%d] in %s" % (caller.filename, caller.lineno, caller.function)
        content = self.describe_args(*args, **kwargs)

        self.echo(header, content)

        if args and kwargs:
            return (args, kwargs.items())

        elif args:
            if len(args) == 1:
                return args[0]
            else:
                return args
        elif kwargs:
            if len(kwargs) == 1:
                return kwargs.popitem()
            else:
                return kwargs.items()


here = Context()
ctxt = Context(echo_args=True, echo_ret=True)
