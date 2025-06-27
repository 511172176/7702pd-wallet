# 7702pd-wallet

This is a minimal demo of an address and domain phishing detector inspired by
[EIP-7702](https://eips.ethereum.org/EIPS/eip-7702). It loads a local blacklist
based on the MetaMask phishing detector, exposes a simple API, and provides a
basic web interface for testing addresses or domains.

## Getting Started

Install dependencies:

```bash
npm install
```

Run the server:

```bash
npm start
```

Open `http://localhost:3000` in a browser and enter an address or domain to see
a security score. The server also exposes `/api/ephemeral` which returns a
random ephemeral address generated via `ethers`.

> **Note:** The blacklist and third-party API integration are illustrative and
> contain only sample data. For full functionality you should download the
> official MetaMask blacklist and configure a real API endpoint.
