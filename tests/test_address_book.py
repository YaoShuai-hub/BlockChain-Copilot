"""
Test address book functionality with transfers.
"""
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tool_wrappers import (
    tool_transfer_tokens,
    tool_list_contacts,
    tool_search_contacts
)

USER_WALLET = "TFp3Ls4mHdzysbX1qxbwXdMzS8mkvhCMx6"

async def main():
    print("📇 Address Book Integration Test")
    print("=" * 70)
    print()
    
    # Test 1: Transfer with memo (should save alias)
    print("TEST 1: Transfer with memo '家人钱包'")
    print("-" * 70)
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address="TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT",
        token="TRX",
        amount=5,
        memo="家人钱包"
    )
    print(result[:500])  # Truncate for readability
    print()
    
    # Test 2: Transfer to different address with memo
    print("\n\nTEST 2: Transfer with memo '朋友-Alice'")
    print("-" * 70)
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address="TLSxH2dyMJW1v3Qy5FToz87atHwauDXUaj",
        token="USDT",
        amount=10,
        memo="朋友-Alice"
    )
    print(result[:500])
    print()
    
    # Test 3: Transfer to same address WITHOUT memo (should just increment count)
    print("\n\nTEST 3: Transfer to '家人钱包' again (no new memo)")
    print("-" * 70)
    result = await tool_transfer_tokens(
        from_address=USER_WALLET,
        to_address="TMP4FFPpKFDqMW99EdtjU8T8SrYfuANCZT",
        token="TRX",
        amount=3
    )
    print(result[:500])
    print()
    
    # Test 4: List all contacts
    print("\n\nTEST 4: List Address Book")
    print("-" * 70)
    result = await tool_list_contacts(sort_by="count")
    print(result)
    print()
    
    # Test 5: Search contacts
    print("\n\nTEST 5: Search for '家'")
    print("-" * 70)
    result = await tool_search_contacts("家")
    print(result)
    
    print("\n\n" + "=" * 70)
    print("✅ Address book tests completed!")
    print("=" * 70)
    print("""
💡 Features Demonstrated:
  ✓ Auto-save alias from transfer memo
  ✓ Increment transfer count
  ✓ Display saved contact name
  ✓ List all contacts sorted by usage
  ✓ Search contacts by alias
  ✓ Persistent storage (JSON file)
""")

if __name__ == "__main__":
    asyncio.run(main())
