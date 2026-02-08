# BlockChain-Copilot MCP Server

An AI-powered assistant for the TRON blockchain, built with the [Model Context Protocol (MCP)](https://modelcontextprotocol.io). This server enables AI Agents (like Claude) to interact with the TRON network, providing market intelligence, asset management, and secure transaction construction.

## Features

### 🔍 Market Intelligence
- **Token Price**: Real-time prices via CoinGecko/DexScreener.
- **Security Check**: Basic contract safety scanning (Mocked/Basic).

### 💼 Asset Management
- **Wallet Balance**: View TRX and TRC20 token balances.
- **Transaction History**: (Planned) View recent activity.

### ⚡ Transaction Execution (Safe Mode)
- **Unsigned Transactions**: Generates JSON transaction objects for:
  - Token Swaps (SunSwap V2).
  - Energy Rental (Cost saving).
- **Simulation**: Pre-flight checks for transaction safety and gas estimation.

> **Note**: This server **NEVER** asks for or handles private keys. It only constructs *unsigned* transactions for the user to sign in their own wallet (e.g., TronLink).

## Setup

1. **Prerequisites**:
   - Python 3.10+
   - `uv` (Fast Python package installer)

2. **Installation**:
   ```bash
   git clone <repo>
   cd BlockChain-Copilot
   uv sync
   ```

3. **Configuration**:
   
   The project supports configuration via `config.toml` (recommended) or `.env`.
   
   **Option A: TOML (Preferred)**
   Edit `config.toml` to set your API keys and endpoints:
   ```toml
   trongrid_api_key = "your_key_here"
   request_timeout = 15.0
   ```
   
   **Option B: Environment Variables**
   Copy `.env.example` to `.env` and add your keys:
   ```env
   TRONGRID_API_KEY=your_key_here
   ```

## Usage

### Running with Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "tron-copilot": {
      "command": "uv",
      "args": ["run", "src/main.py"]
    }
  }
}
```

### Running Manually (Web UI)
To run the full web assistant locally:

1. **Start Backend (API)**:
   ```bash
   uv run python src/server.py
   ```
   *The server will start on `http://localhost:8000`.*

2. **Start Frontend (UI)**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   *The web interface will be available at `http://localhost:3000`.*

### Tools Available
- `get_token_price(symbol)`: Check price of TRX, BTT, etc.
- `get_wallet_balance(address)`: Show portfolio.
- `swap_tokens(address, token_in, token_out, amount)`: Generate swap tx.
- `rent_energy(amount, duration)`: Calculate and propose energy rental.
- `simulate_transaction(hex)`: Check if a tx is likely to succeed.
