# AgriChain

AgriChain is a blockchain-based escrow management and inventory tracking system for agricultural supply chains. This application allows different participants—such as mediators, wholesalers, retailers, and manufacturers—to manage transactions securely on the Algorand blockchain.

## Requirements

1. **Algorand Supported Wallet**: You’ll need an Algorand wallet (e.g., AlgoSigner or MyAlgo Wallet). Create an account if you haven’t already.
2. **LocalNet Setup**: The website runs on Algorand's LocalNet, so make sure you have set it up and started the local network.
3. **Funding**: Add funds to your new Algorand account on LocalNet to enable transactions within the application.
4. **Python Dependencies**: The project uses Python for backend functionalities. Make sure to install the dependencies listed below.

### Python Dependencies

- Python 3.x
- `algosdk`: For interacting with Algorand blockchain.
- Other dependencies as required by your setup (e.g., Flask if using a Python web server).

Install dependencies via pip:

```bash
pip install algosdk
```

## Getting Started

### Running the Frontend

1. Open `index.html` in the root directory.
2. Use a live server (such as the Live Server extension in Visual Studio Code) to start the project:
   - **Right-click on `index.html`** > **Open with Live Server**

### Wallet Connection

- Open the website on your browser.
- Click **Connect Wallet** on the main page.
- Make sure your Algorand wallet is installed and connected.

### Features

- **Role-Based Transactions**: Select your role (e.g., Mediator, Wholesaler, Retailer, Manufacturer) to manage and update relevant inventory.
- **Escrow Management**: Manage and release escrow funds securely.
- **Inventory Updates**: Each role can update inventory and transaction records on the blockchain.
- **Donation**: Built-in support for donations in the platform.

## Usage Notes

1. **Make sure your wallet is funded** on LocalNet, as all transactions require a minimum balance.
2. **Set the Algorand network to LocalNet** in your wallet settings, if applicable.
3. **Run the backend** if any backend services are required, ensuring it is connected to the same network as your LocalNet instance.

## Repository Structure

- `index.html`: Main entry point of the application.
- `approval_program.teal`: The Algorand smart contract logic for escrow and inventory updates.
- `clear_program.teal`: The clear state program for contract termination.

## Important Links

- **Algorand LocalNet Setup**: [Algorand Developer Documentation](https://developer.algorand.org/)
- **Python SDK for Algorand**: [AlgoSDK](https://developer.algorand.org/docs/sdks/python/)
- **Your Wallet**: Make sure to download a wallet supported on the Algorand network.

---

For further questions, contact [Vattigunta Siva Sankar Reddy](mailto:sivasankarreddyvattigunta@gmail.com).
```
