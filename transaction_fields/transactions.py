from pyteal import *

"""
Simple RSVP App

Methods:
- Pay : check if the account opted in, paid 1 ALGO, and create local states
- Check paid : check if the account paid

"""

router = Router(
    "Simple RSVP App",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
        opt_in=OnCompleteAction.call_only(Approve()),
        close_out=OnCompleteAction.always(Approve()),
    ),
    clear_state=Approve()
)

@router.method
def pay(pay:abi.PaymentTransaction):
    return Seq(
        Assert(App.optedIn(Txn.sender(), Global.current_application_id())),
        Assert(pay.get().amount() == Int(1000000)),
        Assert(pay.get().receiver()== Global.current_application_address()),
        App.localPut(Txn.sender(),Bytes("paid"), Bytes("True")),
        Approve()
    )

@router.method
def check_paid(*, output:abi.String):
    paid_state = App.localGet(Txn.sender(), Bytes("paid"))
    return Seq(
        Assert(paid_state == Bytes("True")),
        output.set(paid_state)
    )



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