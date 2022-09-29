from pyteal import *


class Secret:
    class Variables:
        secret = Bytes("NAME")
        likes = Bytes("LIKES")
        dislikes = Bytes("DISLIKES")
        address = Bytes("ADDRESS")
        owner = Bytes("OWNER")

    class AppMethods:
        like = Bytes("like")
        dislike = Bytes("dislike")

    def application_creation(self):
        return Seq([
            Assert(Txn.application_args.length() == Int(2)),
            Assert(Txn.note() == Bytes("secrets:uv1")),
            App.globalPut(self.Variables.secret, Txn.application_args[0]),
            App.globalPut(self.Variables.likes, Int(0)),
            App.globalPut(self.Variables.dislikes, Int(0)),
            App.globalPut(self.Variables.address, Global.creator_address()),
            App.globalPut(self.Variables.owner, Txn.application_args[1]),
            Approve()
        ])

    def like(self):

        return Seq([
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(1),
                ),
            ),
            Assert(
                And(
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == App.globalGet(
                        self.Variables.address),
                    Gtxn[1].amount() == Int(1000000),
                    Gtxn[1].sender() == Gtxn[0].sender(),
                )
            ),

            App.globalPut(self.Variables.likes, App.globalGet(self.Variables.likes) + Int(1)),
            Approve()
        ])

    def dislike(self):

        return Seq([
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(1),
                ),
            ),
            Assert(
                And(
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == App.globalGet(
                        self.Variables.address),
                    Gtxn[1].amount() == Int(1000000),
                    Gtxn[1].sender() == Gtxn[0].sender(),
                )
            ),

            App.globalPut(self.Variables.dislikes,
                          App.globalGet(self.Variables.dislikes) + Int(1)),
            Approve()
        ])

    def application_deletion(self):
        return Return(Txn.sender() == Global.creator_address())

    def application_start(self):
        return Cond(
            [Txn.application_id() == Int(0), self.application_creation()],
            [Txn.on_completion() == OnComplete.DeleteApplication,
             self.application_deletion()],
            [Txn.application_args[0] == self.AppMethods.like, self.like()],
            [Txn.application_args[0] == self.AppMethods.dislike, self.dislike()],
        )

    def approval_program(self):
        return self.application_start()

    def clear_program(self):
        return Return(Int(1))
