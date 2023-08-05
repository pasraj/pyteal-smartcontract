from pyteal import *

"""
Simple charirty application that does the following:
- Accept funding more or equal to 2 ALGOs and records the funder,
- Pay out one ALGO to an account 
- Retrive who the funder is
"""


router = Router(
    "abi-type-example",
    BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
    )
)

PAYMENT_AMOUNT = Int(1000000) # 1 million microalgos = 1 ALGO

@router.method
def pay(receiver:abi.Account, *,output:abi.Address):
    return Seq(
        InnerTxnBuilder.Execute({
                TxnField.type_enum:TxnType.Payment,
                TxnField.amount: PAYMENT_AMOUNT,
                TxnField.receiver: receiver.address()
                }),
                output.set(receiver.address())
    )


@router.method
def fund(payment:abi.PaymentTransaction):
    return Seq(
        Assert(payment.get().receiver()== Global.current_application_address()),
        Assert(payment.get().amount()==(PAYMENT_AMOUNT * Int(2))),
        App.globalPut(Bytes("funder"), payment.get().sender())
    )


@router.method
def get_funder(*, output:abi.Address):
    return output.set(App.globalGet(Bytes("funder")))




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