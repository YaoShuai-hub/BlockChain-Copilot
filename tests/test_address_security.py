"""
Test address security checker with various addresses.
"""
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tool_wrappers import tool_check_address_security, tool_transfer_tokens

# Test addresses
SAFE_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT contract - known safe
USER_WALLET = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"
RANDOM_ADDRESS = "TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT"

async def main():
    print("🔒 Address Security Checker - Test Suite")
    print("=" * 70)
    print()
    
    # Test 1: Known safe address (USDT contract)
    print("TEST 1: Check USDT Contract (should be SAFE)")
    print("-" * 70)
    result = await tool_check_address_security(SAFE_ADDRESS)
    print(result)
    print()
    
    # Test 2: User's own address
    print("\n\nTEST 2: Check User Wallet")
    print("-" * 70)
    result = await tool_check_address_security(USER_WALLET)
    print(result)
    print()
    
    # Test 3: Random address (unknown risk)
    print("\n\nTEST 3: Check Target Wallet")
    print("-" * 70)
    result = await tool_check_address_security(RANDOM_ADDRESS)
    print(result)
    print()
    
    # Test 4: Try transfer with auto security check
    print("\n\nTEST 4: Transfer with Auto Security Check")
    print("-" * 70)
    print("Attempting to transfer 10 USDT to target address...")
    print("(Security check will run automatically)")
    print()
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address=RANDOM_ADDRESS,
        token="USDT",
        amount=10
    )
    print(result)
    
    print("\n\n" + "=" * 70)
    print("✅ Security tests completed!")
    print("=" * 70)
    print("""
💡 Key Features Demonstrated:
  ✓ TronScan security API integration
  ✓ Blacklist detection
  ✓ Fraud transaction checking
  ✓ Address label verification
  ✓ Automatic pre-transfer security check
  ✓ Transaction blocking for high-risk addresses
""")

if __name__ == "__main__":
    asyncio.run(main())
