import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.info import get_token_price, get_token_security
from src.tools.asset import get_wallet_balance, simulate_transaction
from src.tools.trade import swap_tokens, rent_energy
from src.config import Config

async def main():
    print("🚀 Starting BlockChain-Copilot Verification...\n")
    print(f"Configuration Loaded. Timeout: {Config.TIMEOUT}s, USDT: {Config.USDT_CONTRACT[:6]}...\n")

    # 1. Test Price
    print(f"1. Testing get_token_price('TRX')...")
    price = await get_token_price("TRX")
    print(f"Result: {price}\n")

    # 2. Test Security
    print(f"2. Testing get_token_security('TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t')...")
    security = await get_token_security("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t") # USDT
    print(f"Result: {security}\n")

    # 3. Test Wallet Balance (SunSwap V2 Router Address)
    addr = "TKzxdSv2FZKQrEqkKVgp5DcwEXBEKMg2Ax"
    print(f"3. Testing get_wallet_balance('{addr}')...")
    balance = await get_wallet_balance(addr)
    print(f"Result: {balance}\n")

    # 4. Test Swap Generation
    print(f"4. Testing swap_tokens (TRX -> USDT)...")
    # USDT Address from Config
    usdt = Config.USDT_CONTRACT
    # Using the router address as user address just for generation (unsigned)
    swap_tx = await swap_tokens(addr, "TRX", usdt, 10, 0.5)
    print(f"Result (First 500 chars): {swap_tx[:500]}...\n")

    # 5. Test Rent Energy
    print(f"5. Testing rent_energy...")
    rental = await rent_energy(32000, 3)
    print(f"Result: {rental}\n")
    
    # 6. Test Simulation
    print(f"6. Testing simulate_transaction...")
    sim = await simulate_transaction("00000000000000000aaaaaa")
    print(f"Result: {sim}\n")

if __name__ == "__main__":
    asyncio.run(main())
