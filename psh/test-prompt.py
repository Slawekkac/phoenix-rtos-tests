from psh.tools.basic import Psh


def harness(p):
    psh = Psh(p)
    psh.run()
    psh.assert_only_prompt()
