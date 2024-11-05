from algosdk.transaction import ApplicationCreateTxn, OnComplete, StateSchema, wait_for_confirmation
from algosdk import account, mnemonic
from algosdk.v2client import algod
from contract import approval_program, clear_state_program
from pyteal import compileTeal, Mode
import os
ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # Use 'aaaaaaaa...' if using Algorand sandbox

# Your mnemonic phrase (Replace with yours)
CREATOR_MNEMONIC = "deny over angry doctor junk recipe barely produce senior park lesson purpose toss apart stem sketch avoid fruit clip right message giraffe main absorb castle"

# Initialize Algod client
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def compile_program(client, source_code):
    """Compile a TEAL program using the Algorand client."""
    try:
        compile_response = client.compile(source_code)
        return compile_response['result']
    except Exception as e:
        print("Error compiling program:", e)
        return None

def deploy_smart_contract():
    # Ensure mnemonic is provided
    if not CREATOR_MNEMONIC:
        raise ValueError("Please set the CREATOR_MNEMONIC environment variable.")

    # Compile PyTeal code to TEAL assembly
    print("Compiling PyTeal to TEAL...")
    approval_teal = compileTeal(approval_program(), mode=Mode.Application, version=2)
    clear_teal = compileTeal(clear_state_program(), mode=Mode.Application, version=2)

    # Compile TEAL programs with Algod client
    print("Compiling TEAL approval and clear programs...")
    approval_program_compiled = compile_program(algod_client, approval_teal)
    clear_state_program_compiled = compile_program(algod_client, clear_teal)

    if not approval_program_compiled or not clear_state_program_compiled:
        print("Error compiling TEAL programs. Exiting.")
        return

    # Define application state schema
    global_schema = StateSchema(num_uints=10, num_byte_slices=10)
    local_schema = StateSchema(num_uints=10, num_byte_slices=10)

    # Get creator account info from mnemonic
    creator_private_key = mnemonic.to_private_key(CREATOR_MNEMONIC)
    creator_address = account.address_from_private_key(creator_private_key)

    # Create application transaction
    print("Creating application transaction...")
    params = algod_client.suggested_params()
    app_create_txn = ApplicationCreateTxn(
        sender=creator_address,
        sp=params,
        on_complete=OnComplete.NoOpOC,
        approval_program=approval_program_compiled,
        clear_program=clear_state_program_compiled,
        global_schema=global_schema,
        local_schema=local_schema,
    )

    # Sign and send the transaction
    signed_txn = app_create_txn.sign(creator_private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    print("Transaction ID:", tx_id)

    # Wait for confirmation
    try:
        wait_for_confirmation(algod_client, tx_id)
        print("Smart contract deployed successfully!")
        print("Application ID:", algod_client.pending_transaction_info(tx_id)["application-index"])
    except Exception as e:
        print("Error during deployment confirmation:", e)

if __name__ == "__main__":
    deploy_smart_contract()
