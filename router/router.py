from pyteal import *


router = Router(
    "my-first-router",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
        opt_in=OnCompleteAction.call_only(Approve()),
        close_out=OnCompleteAction.always(Approve()),
        update_application=OnCompleteAction.never(),
        delete_application=OnCompleteAction.never(),
    ),
    clear_state=Approve(),
)

@router.method
def hello(name:abi.String, *, output:abi.String):
    return output.set(Concat(Bytes("Hello "), name.get()))


if __name__ == "__main__":
    import os
    import json

    path = os.path.dirname(os.path.abspath(__file__))
    approval, clear, contract = router.compile_program(version=6)
 
    # dum out the contract as json
    with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
        f.write(json.dumps(contract.dictify(), indent=2))

    # write the approval and clear program

    with open(os.path.join(path, "artifacts/approval.teal"),"w") as f:
        f.write(approval)


    with open(os.path.join(path, "artifacts/clear.teal"),"w") as f:
        f.write(clear)