from subprocess import run

def command_cmd(command_,arguments):
        #TODO: deberia verificar que si el sistema es windows.
        if (arguments):
            return run(f'{command_}',arguments,shell=True) 
        return run(f'{command_}',shell=True)