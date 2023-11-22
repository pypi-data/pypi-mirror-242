if __name__ == "__main__":
    pass
    # from command_cmd import command_cmd
else:
    pass
    # from .command_cmd import command_cmd


from os.path import splitext

def get_extension(file):
    fileExtencion = splitext(file)[1].partition(".")[2]
    return fileExtencion
"optiene la extencion del archivo"