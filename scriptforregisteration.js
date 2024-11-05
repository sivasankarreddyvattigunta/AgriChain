        const algodToken = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
        const algodServer = 'http://localhost';
        const algodPort = 4001;
        const algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);

        const appId = 1002;
        let userWalletAddress = '';

        async function connectWallet() {
            if (typeof AlgoSigner !== 'undefined') {
                try {
                    await AlgoSigner.connect();
                    const accounts = await AlgoSigner.accounts({
                        ledger: 'TestNet'
                    });
                    userWalletAddress = accounts[0].address;
                    document.getElementById('walletStatus').innerText = `Wallet Connected: ${userWalletAddress}`;
                } catch (error) {
                    console.error("Wallet connection failed:", error);
                    document.getElementById('walletStatus').innerText = 'Failed to connect wallet.';
                }
            } else {
                alert('Please install Algorand supported wallet extension to continue');
            }
        }

        async function submitRegistration(formData) {
            try {
                const params = await algodClient.getTransactionParams().do();
                const appArgs = [
                    new Uint8Array(Buffer.from(formData.name)),
                    new Uint8Array(Buffer.from(formData.email)),
                    new Uint8Array(Buffer.from(formData.password)),
                    new Uint8Array(Buffer.from(formData.role)),
                    new Uint8Array(Buffer.from(formData.phone)),
                    new Uint8Array(Buffer.from(formData.age)),
                    new Uint8Array(Buffer.from(formData.address))
                ];

                const txn = algosdk.makeApplicationNoOpTxn(userWalletAddress, params, appId, appArgs);
                const txnBase64 = AlgoSigner.encoding.msgpackToBase64(txn.toByte());

                const signedTxn = await AlgoSigner.signTxn([{ txn: txnBase64 }]);
                const response = await algodClient.sendRawTransaction(
                    AlgoSigner.encoding.base64ToMsgpack(signedTxn[0].blob)
                ).do();

                console.log("Transaction successful with ID:", response.txId);

                localStorage.setItem('userData', JSON.stringify({
                    name: formData.name,
                    email: formData.email,
                    role: formData.role
                }));

                window.location.href = 'login.html';
            } catch (error) {
                console.error("Transaction failed:", error);
                document.getElementById("errorMessage").style.display = "block";
            }
        }

        document.getElementById("registrationForm").addEventListener("submit", function(event) {
            event.preventDefault();

            const formData = {
                name: document.getElementById("name").value,
                email: document.getElementById("email").value,
                password: document.getElementById("password").value,
                age: document.getElementById("age").value,
                phone: document.getElementById("phone").value,
                address: document.getElementById("address").value,
                role: document.getElementById("role").value
            };

            if (userWalletAddress) {
                submitRegistration(formData);
            } else {
                alert("Please connect your wallet first.");
            }
        });
