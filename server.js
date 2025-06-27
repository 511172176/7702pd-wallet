const express = require('express');
const fs = require('fs');
const fetch = require('node-fetch');
const { Wallet } = require('ethers');

const app = express();
const PORT = process.env.PORT || 3000;

// Load local phishing config
const config = JSON.parse(fs.readFileSync('./eth-phishing-config.json'));

// Simple ephemeral wallet generator using ethers (EIP-7702 style stub)
function createEphemeralWallet() {
  return Wallet.createRandom();
}

// Placeholder third-party blacklist check (stub, no network in this environment)
async function checkThirdParty(value) {
  // In a real environment, call the third-party API here
  // Return true if the value is blacklisted
  return false;
}

// Basic scoring logic
async function evaluate(value) {
  const lower = value.toLowerCase();
  let score = 100;
  let reasons = [];

  if (lower.startsWith('0x') && lower.length === 42) {
    if (config.addressBlacklist.includes(lower)) {
      score -= 70;
      reasons.push('Listed in local address blacklist');
    }
  } else {
    if (config.blacklist.includes(lower)) {
      score -= 70;
      reasons.push('Listed in local domain blacklist');
    }
  }

  if (await checkThirdParty(lower)) {
    score -= 20;
    reasons.push('Listed by third-party blacklist');
  }

  if (score < 0) score = 0;
  return { score, reasons };
}

app.use(express.static('.'));
app.use(express.json());

app.post('/api/check', async (req, res) => {
  const { value } = req.body;
  if (!value) return res.status(400).json({ error: 'Missing value' });
  const result = await evaluate(value);
  res.json(result);
});

app.get('/api/ephemeral', (req, res) => {
  const wallet = createEphemeralWallet();
  res.json({ address: wallet.address });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
