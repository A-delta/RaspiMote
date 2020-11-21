# -*- coding: utf-8 -*-

def errorclose(reason):
    print(f'The program encountered a problem and needs to close.\nError : “{reason}”')

try:
    import change_volume as vol
    import prog_init as init

    if init.check_platorm() == 'linux':
        pc_init = init.init_lnx
        pc_init = dict(pc_init)
        vol.change_volume_lnx(0, pc_init["sound_conf"])

except:
    errorclose(reason="Unknown")