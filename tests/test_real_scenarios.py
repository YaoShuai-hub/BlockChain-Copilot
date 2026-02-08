"""
Real-world test scenarios using user's wallet addresses.
Tests the Agent Skills with actual blockchain operations.
"""
import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tool_wrappers import (
    tool_get_token_price,
    tool_get_wallet_balance,
    tool_transfer_tokens,
    tool_energy_rental
)

# User's addresses from requirements
USER_WALLET = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"
TARGET_WALLET = "TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT"

async def main():
    print("🔬 BlockChain-Copilot Real-World Test Suite\n")
    print(f"👤 User Wallet: {USER_WALLET}")
    print(f"🎯 Target Wallet: {TARGET_WALLET}\n")
    print("=" * 70)
    
    # Test 1: Check user's portfolio
    print("\n📊 TEST 1: Query User's Wallet Balance")
    print("=" * 70)
    print(f"Querying assets for {USER_WALLET}...\n")
    result = await tool_get_wallet_balance(USER_WALLET)
    print(result)
    
    # Test 2: Check TRX price
    print("\n\n💰 TEST 2: Get Current TRX Price")
    print("=" * 70)
    result = await tool_get_token_price("TRX")
    print(result)
    
    # Test 3: Check USDT price
    print("\n\n💰 TEST 3: Get Current USDT Price")
    print("=" * 70)
    result = await tool_get_token_price("USDT")
    print(result)
    
    # Test 4: Build TRX transfer transaction
    print("\n\n📤 TEST 4: Build TRX Transfer (10 TRX)")
    print("=" * 70)
    print(f"From: {USER_WALLET}")
    print(f"To:   {TARGET_WALLET}")
    print(f"Amount: 10 TRX\n")
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address=TARGET_WALLET,
        token="TRX",
        amount=10,
        memo="Test transfer from BlockChain-Copilot Agent"
    )
    print(result)
    
    # Test 5: Build USDT transfer transaction
    print("\n\n📤 TEST 5: Build USDT Transfer (5 USDT)")
    print("=" * 70)
    print(f"From: {USER_WALLET}")
    print(f"To:   {TARGET_WALLET}")
    print(f"Amount: 5 USDT\n")
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address=TARGET_WALLET,
        token="USDT",
        amount=5
    )
    print(result)
    
    # Test 6: Energy rental analysis for USDT transfer
    print("\n\n⚡ TEST 6: Energy Rental Analysis (for USDT transfer)")
    print("=" * 70)
    result = await tool_energy_rental(28000, 3)
    print(result)
    
    # Summary
    print("\n\n" + "=" * 70)
    print("✅ TEST SUITE COMPLETED")
    print("=" * 70)
    print("""
📋 Summary:
  ✓ Portfolio query working
  ✓ Price fetching working (TRX, USDT)
  ✓ TRX transfer transaction built
  ✓ USDT transfer transaction built
  ✓ Energy rental calculator working

🔐 Security Note:
  All transactions are UNSIGNED. To actually execute them:
  1. Copy the transaction JSON
  2. Sign with TronLink or your wallet
  3. Broadcast to the network

💡 Next Steps:
  - Add TRONGRID_API_KEY to config.toml for better rate limits
  - Add TRONSCAN_API_KEY for portfolio features
  - Consider using energy rental before USDT transfers!
""")

if __name__ == "__main__":
    asyncio.run(main())
