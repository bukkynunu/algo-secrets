from pyteal import *

from secrets_contract import Secret

if __name__ == "__main__":
    approval_program = Secret().approval_program()
    clear_program = Secret().clear_program()

    # Mode.Application specifies that this is a smart contract
    compiled_approval = compileTeal(approval_program, Mode.Application, version=6)
    print(compiled_approval)
    with open("secrets_approval.teal", "w") as teal:
        teal.write(compiled_approval)
        teal.close()

    # Mode.Application specifies that this is a smart contract
    compiled_clear = compileTeal(clear_program, Mode.Application, version=6)
    print(compiled_clear)
    with open("secrets_clear.teal", "w") as teal:
        teal.write(compiled_clear)
        teal.close()