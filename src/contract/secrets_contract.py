from pyteal import *


class Secret:
    class Variables:
        secret = Bytes("NAME")
        likes = Bytes("LIKES")
        address = Bytes("ADDRESS")
        owner = Bytes("OWNER")
        liked = Bytes("LIKED")

    class AppMethods:
        like = Bytes("like")
        dislike = Bytes("dislike")

    def application_creation(self):
        return Seq([
            # checks if there are any empty values in application_args
            Assert(Txn.application_args.length() == Int(2)),
            Assert(Txn.note() == Bytes("secrets:uv1")),
            Assert(Len(Txn.application_args[0]) > Int(0)),
            Assert(Len(Txn.application_args[1]) > Int(0)),
            App.globalPut(self.Variables.secret, Txn.application_args[0]),
            App.globalPut(self.Variables.likes, Int(0)),
            App.globalPut(self.Variables.address, Global.creator_address()),
            App.globalPut(self.Variables.owner, Txn.application_args[1]),
            Approve()
        ])

    # function(subroutine) to be called when opting in the app
    def optIn(self):
        # Sets the local Boolean value of liked for sender to false which is Int 0
        return Seq([
            App.localPut(Txn.sender(), self.Variables.liked, Int(0)),
            Approve()
        ])

    def like(self):

        return Seq([
            # checks if there are 2 transactions in the atomic group
            # the payment and the liked transaction
            # checks if user has not liked the secret yet
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(1),
                ),
            ),
            Assert(
                And(
                    App.localGet(Txn.sender(), self.Variables.liked) == Int(0),
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == App.globalGet(
                        self.Variables.address),
                    Gtxn[1].amount() == Int(1000000),
                    Gtxn[1].sender() == Gtxn[0].sender(),
                )
            ),
            App.localPut(Txn.sender(), self.Variables.liked, Int(1)),
            App.globalPut(self.Variables.likes, App.globalGet(self.Variables.likes) + Int(1)),
            Approve()
        ])

    def dislike(self):

        return Seq([
            # checks if there are 2 transactions in the atomic group
            # the payment and the dislike transaction
            # checks if user has already liked the secret
            Assert(
                And(
                    Global.group_size() == Int(2),
                    Txn.application_args.length() == Int(1),
                ),
            ),
            Assert(
                And(
                    App.localGet(Txn.sender(),self.Variables.liked) == Int(1),
                    Gtxn[1].type_enum() == TxnType.Payment,
                    Gtxn[1].receiver() == App.globalGet(
                        self.Variables.address),
                    Gtxn[1].amount() == Int(1000000),
                    Gtxn[1].sender() == Gtxn[0].sender(),
                )
            ),
            App.localPut(Txn.sender(), self.Variables.liked, Int(0)),
            App.globalPut(self.Variables.likes,
                          App.globalGet(self.Variables.likes) - Int(1)),
            Approve()
        ])

    def application_deletion(self):
        return Return(Txn.sender() == Global.creator_address())

    def application_start(self):
        return Cond(
            [Txn.application_id() == Int(0), self.application_creation()],
            [Txn.on_completion() == OnComplete.DeleteApplication,
             self.application_deletion()],
            [Txn.on_completion() == OnComplete.OptIn, self.optIn()],
            [Txn.application_args[0] == self.AppMethods.like, self.like()],
            [Txn.application_args[0] == self.AppMethods.dislike, self.dislike()],
        )

    def approval_program(self):
        return self.application_start()

    def clear_program(self):
        return Return(Int(1))
