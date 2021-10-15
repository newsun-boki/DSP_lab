class Print(object):
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BlUE = '\033[94m'
    END = '\033[0m'

    @classmethod
    def red(cls, string):
        print(cls.RED + string + cls.END)

    @classmethod
    def green(cls, string):
        print(cls.GREEN + string + cls.END)

    @classmethod
    def yellow(cls, string):
        print(cls.YELLOW + string + cls.END)

    @classmethod
    def cyan(cls, string):
        print(cls.BlUE + string + cls.END)


if __name__ == '__main__':
    Print.green('this is green, such as ....ok')
    Print.red('this is red, such as error:xxxxxx')
    Print.yellow('this is yellow, such as warning........')
    Print.cyan('this is blue, such as, information')
    
