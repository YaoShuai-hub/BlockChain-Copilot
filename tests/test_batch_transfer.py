"""
Test the generated batch-transfer skill
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the generated skill using importlib
import importlib.util

spec = importlib.util.spec_from_file_location(
    "batch_transfer",
    project_root / "personal-skills/batch-transfer/scripts/main.py"
)
batch_transfer_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch_transfer_module)

execute_skill = batch_transfer_module.execute_skill
generate_test_addresses = batch_transfer_module.generate_test_addresses

async def test_batch_transfer():
    """Test the batch transfer skill."""
    
    print("=" * 80)
    print("🧪 TESTING GENERATED BATCH-TRANSFER SKILL")
    print("=" * 80)
    print()
    
    # Generate test addresses
    print("Step 1: Generating 10 test addresses...")
    test_addresses = await generate_test_addresses(10)
    
    for i, addr in enumerate(test_addresses, 1):
        print(f"   {i}. {addr}")
    print()
    
    # Create recipients list
    print("Step 2: Creating recipients list...")
    recipients = []
    for i, address in enumerate(test_addresses, 1):
        recipients.append({
            "address": address,
            "amount": i * 10  # Different amounts: 10, 20, 30, ..., 100
        })
    
    total = sum(r['amount'] for r in recipients)
    print(f"   Recipients: {len(recipients)}")
    print(f"   Total amount: {total} TRX")
    print()
    
    # Test execution (dry run - won't actually send)
    print("Step 3: Testing batch transfer logic...")
    print()
    
    sender_address = "TYourTestAddress123..."  # Fake address for demo
    
    try:
        result = await execute_skill(
            from_address=sender_address,
            recipients=recipients,
            token="TRX",
            memo="Batch transfer test"
        )
        
        print()
        print("=" * 80)
        print("RESULT:")
        print("=" * 80)
        
        if result['success']:
            print("✅ Skill executed successfully!")
            print()
            print(f"Message: {result['message']}")
            print()
            print("Details:")
            print(f"  Total amount: {result['data']['total_amount']} TRX")
            print(f"  Total recipients: {result['data']['total_recipients']}")
            print(f"  Successful: {result['data']['successful_count']}")
            print(f"  Failed: {result['data']['failed_count']}")
            print()
            
            # Show first few results
            print("First 3 results:")
            for i, res in enumerate(result['data']['results'][:3], 1):
                status = "✅" if res['status'] == 'success' else "❌"
                print(f"  {i}. {status} {res['recipient']}: {res['amount']} TRX")
        else:
            print(f"❌ Skill execution failed!")
            print(f"Error: {result.get('error')}")
            print(f"Message: {result.get('message')}")
    
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    print("Test Complete")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_batch_transfer())
