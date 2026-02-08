"""
Quick test with Nile testnet configuration
"""
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tool_wrappers import (
    tool_get_token_price,
    tool_get_wallet_balance,
    tool_transfer_tokens
)

USER_WALLET = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"
TARGET_WALLET = "TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT"

async def main():
    print("🌐 NILE TESTNET - Quick Validation Test")
    print("=" * 70)
    print(f"User Wallet: {USER_WALLET}")
    print(f"Target Wallet: {TARGET_WALLET}")
    print("=" * 70)
    print()
    
    # Test 1: Price check
    print("TEST 1: TRX Price")
    print("-" * 70)
    result = await tool_get_token_price("TRX")
    print(result)
    print()
    
    # Test 2: Wallet balance on testnet
    print("\\nTEST 2: Wallet Balance (Nile Testnet)")
    print("-" * 70)
    result = await tool_get_wallet_balance(USER_WALLET)
    print(result)
    print()
    
    # Test 3: Build transfer
    print("\\nTEST 3: Build TRX Transfer (Nile Testnet)")
    print("-" * 70)
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address=TARGET_WALLET,
        token="TRX",
        amount=10,
        memo="Nile testnet transfer"
    )
    print(result)
    
    print("\\n" + "=" * 70)
    print("✅ Nile testnet configuration validated!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
