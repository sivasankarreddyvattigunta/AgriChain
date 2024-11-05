from pyteal import *

def approval_program():
    farmer_key = Bytes("farmer")
    product_key = Bytes("product")
    mediator_key = Bytes("mediator")
    donation_org_key = Bytes("donation_org")
    location_key = Bytes("location")
    quantity_key = Bytes("quantity")
    escrow_key = Bytes("escrow_balance")
    expiry_key = Bytes("expiry")
    price_year1_key = Bytes("price_year1") 
    price_year2_key = Bytes("price_year2")
    current_price_key = Bytes("current_price")
    estimated_price_key = Bytes("estimated_price")

    def is_role(role_key):
        return App.localGet(Int(0), role_key) != Bytes("")

    def register_farmer(location, quantity):
        return Seq([
            App.localPut(Int(0), farmer_key, Txn.application_id()),
            App.localPut(Int(0), location_key, location),
            App.localPut(Int(0), quantity_key, quantity),
            Return(Int(1))
        ])

    def register_mediator(location):
        return Seq([
            App.localPut(Int(0), mediator_key, Txn.application_id()),
            App.localPut(Int(0), location_key, location),
            App.localPut(Int(0), escrow_key, Int(0)),
            Return(Int(1))
        ])

    def register_donation_org(location):
        return Seq([
            App.localPut(Int(0), donation_org_key, Txn.application_id()),
            App.localPut(Int(0), location_key, location),
            Return(Int(1))
        ])

    def update_product_info(product_id, lifespan, quality, expiry, current_price, est_price):
        avg_price_last_two_years = (App.localGet(Int(0), price_year1_key) + App.localGet(Int(0), price_year2_key)) / Int(2)
        notify_consumer = If(
            current_price > avg_price_last_two_years * Int(120) / Int(100),
            App.localPut(Int(0), Bytes("price_alert"), Int(1)),
            App.localPut(Int(0), Bytes("price_alert"), Int(0))
        )

        return Seq([
            Assert(is_role(mediator_key)),
            App.localPut(Int(0), product_key, product_id),
            App.localPut(Int(0), Bytes("lifespan"), lifespan),
            App.localPut(Int(0), Bytes("quality_level"), quality),
            App.localPut(Int(0), expiry_key, expiry),
            App.localPut(Int(0), current_price_key, current_price),
            App.localPut(Int(0), estimated_price_key, est_price),
            notify_consumer,
            Return(Int(1))
        ])

    def get_product_details():
        return Seq([
            Assert(is_role(farmer_key)),
            Return(App.localGet(Int(0), product_key))
        ])

    def search_nearby_locations(min_quantity, max_expiry):
        return Seq([
            Assert(is_role(donation_org_key)),
            Assert(App.localGet(Int(0), quantity_key) >= min_quantity),
            Assert(App.localGet(Int(0), expiry_key) <= max_expiry),
            Return(App.localGet(Int(0), location_key))
        ])

    def buy_directly_from_farmer(product_id, quantity):
        farmer = Txn.accounts[1]
        avg_price_last_two_years = (App.localGet(Int(1), price_year1_key) + App.localGet(Int(1), price_year2_key)) / Int(2)
        current_price = App.localGet(Int(1), current_price_key)

        price_alert = If(
            current_price > avg_price_last_two_years * Int(120) / Int(100),
            App.localPut(Int(0), Bytes("price_alert"), Int(1)),
            App.localPut(Int(0), Bytes("price_alert"), Int(0))
        )

        return Seq([
            Assert(is_role(farmer_key)),
            Assert(App.localGet(Int(1), product_key) == product_id),
            Assert(App.localGet(Int(1), quantity_key) >= quantity),
            App.localPut(Int(1), quantity_key, App.localGet(Int(1), quantity_key) - quantity),
            price_alert,
            Return(Int(1))
        ])

    def mediator_escrow_deposit(amount):
        return Seq([
            Assert(is_role(mediator_key)),
            App.localPut(Int(0), escrow_key, App.localGet(Int(0), escrow_key) + amount),
            Return(Int(1))
        ])

    def release_escrow_to_farmer(farmer, amount):
        return Seq([
            Assert(is_role(mediator_key)),
            Assert(App.localGet(Int(0), escrow_key) >= amount),
            App.localPut(Int(0), escrow_key, App.localGet(Int(0), escrow_key) - amount),
            Return(Int(1))
        ])

    def donate_food(org, quantity):
        return Seq([
            Assert(is_role(farmer_key)),
            Assert(App.localGet(Int(0), quantity_key) >= quantity),
            App.localPut(Int(0), quantity_key, App.localGet(Int(0), quantity_key) - quantity),
            App.localPut(Int(1), Bytes("donated_quantity"), App.localGet(Int(1), Bytes("donated_quantity")) + quantity),
            Return(Int(1))
        ])

    program = Cond(
        [Txn.application_id() == Int(0), register_farmer(Txn.application_args[1], Btoi(Txn.application_args[2]))],
        [Txn.application_id() == Int(1), register_mediator(Txn.application_args[1])],
        [Txn.application_id() == Int(2), register_donation_org(Txn.application_args[1])],
        [
            Txn.application_id() == Int(3),
            update_product_info(
                Txn.application_args[1],
                Btoi(Txn.application_args[2]),
                Btoi(Txn.application_args[3]),
                Btoi(Txn.application_args[4]),
                Btoi(Txn.application_args[5]),
                Btoi(Txn.application_args[6])
            )
        ],
        [Txn.application_id() == Int(4), get_product_details()],
        [Txn.application_id() == Int(5), search_nearby_locations(Btoi(Txn.application_args[1]), Btoi(Txn.application_args[2]))],
        [Txn.application_id() == Int(6), buy_directly_from_farmer(Txn.application_args[1], Btoi(Txn.application_args[2]))],
        [Txn.application_id() == Int(7), mediator_escrow_deposit(Btoi(Txn.application_args[1]))],
        [Txn.application_id() == Int(8), release_escrow_to_farmer(Txn.accounts[1], Btoi(Txn.application_args[1]))],
        [Txn.application_id() == Int(9), donate_food(Txn.accounts[1], Btoi(Txn.application_args[1]))]
    )

    return program

def clear_state_program():
    return Return(Int(1))

if __name__ == "__main__":
    approval_teal = compileTeal(approval_program(), mode=Mode.Application, version=4)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=4)

    print("Approval Program TEAL:")
    print(approval_teal)

    print("\nClear State Program TEAL:")
    print(clear_teal)
