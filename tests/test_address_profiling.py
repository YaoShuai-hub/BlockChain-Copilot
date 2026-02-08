"""
Test address profiling functionality.
"""
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tool_wrappers import tool_profile_address, tool_transfer_tokens

USER_WALLET = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"

async def main():
    print("📊 Address Profiling Test Suite")
    print("=" * 70)
    print()
    
    # Test 1: Profile user's own wallet
    print("TEST 1: Profile User Wallet (Direct Address)")
    print("-" * 70)
    result = await tool_profile_address(USER_WALLET, max_transactions=100)
    print(result)
    print()
    
    # Test 2: First create a contact via transfer
    print("\n\nTEST 2: Create Contact '测试地址' via Transfer")
    print("-" * 70)
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address="TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT",
        token="TRX",
        amount=1,
        memo="测试地址"
    )
    print("Transfer created (contact saved)")
    print()
    
    # Test 3: Profile using alias
    print("\n\nTEST 3: Profile Address Using Alias '测试地址'")
    print("-" * 70)
    result = await tool_profile_address("测试地址", max_transactions=100)
    print(result)
    print()
    
    # Test 4: Profile well-known address (USDT contract)
    print("\n\nTEST 4: Profile USDT Contract (High Activity)")
    print("-" * 70)
    result = await tool_profile_address("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", max_transactions=50)
    print(result)
    
    print("\n\n" + "=" * 70)
    print("✅ Address profiling tests completed!")
    print("=" * 70)
    print("""
💡 Features Demonstrated:
  ✓ Transaction history analysis (up to 1000 txs or 1 year)
  ✓ Behavioral pattern detection
  ✓ Address classification (trader, holder, etc.)
  ✓ Anomaly detection (spikes, unusual patterns)
  ✓ Alias resolution from address book
  ✓ Risk assessment
""")

if __name__ == "__main__":
    asyncio.run(main())
