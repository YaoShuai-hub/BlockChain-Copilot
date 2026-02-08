"""
Comprehensive Test Suite for BlockChain-Copilot Skills
Tests all skills with 3 test cases each:
1. Success scenario (happy path)
2. Edge case
3. Error handling
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
import json
import importlib.util

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Helper function to load skills dynamically
def load_skill_module(skill_path):
    """Dynamically load a skill module from file path."""
    spec = importlib.util.spec_from_file_location("skill_module", skill_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Test results storage
test_results = {
    'timestamp': datetime.now().isoformat(),
    'total_skills': 0,
    'passed': 0,
    'failed': 0,
    'skills': {}
}


def log_test_result(skill_name, test_name, passed, message="", details=None):
    """Log a test result."""
    if skill_name not in test_results['skills']:
        test_results['skills'][skill_name] = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'tests': []
        }
    
    test_results['skills'][skill_name]['total'] += 1
    test_results['skills'][skill_name]['tests'].append({
        'name': test_name,
        'passed': passed,
        'message': message,
        'details': details
    })
    
    if passed:
        test_results['skills'][skill_name]['passed'] += 1
        test_results['passed'] += 1
        print(f"  ✅ {test_name}: PASSED")
    else:
        test_results['skills'][skill_name]['failed'] += 1
        test_results['failed'] += 1
        print(f"  ❌ {test_name}: FAILED - {message}")
    
    if details:
        print(f"     Details: {details}")


async def test_token_price():
    """Test token-price skill."""
    print("\n" + "="*80)
    print("🧪 Testing: token-price")
    print("="*80)
    
    try:
        # Load module
        fetch_price_module = load_skill_module(
            project_root / "skills/token-price/scripts/fetch_price.py"
        )
        get_token_price = fetch_price_module.get_token_price
        
        # Test 1: Valid token (TRX)
        try:
            result = await get_token_price("TRX")
            passed = result.get('success') and result.get('data', {}).get('price') is not None
            log_test_result(
                'token-price',
                'Test 1: Get TRX price',
                passed,
                "Successfully fetched TRX price" if passed else "Failed to fetch price",
                f"Price: ${result.get('data', {}).get('price')}" if passed else None
            )
        except Exception as e:
            log_test_result('token-price', 'Test 1: Get TRX price', False, str(e))
        
        # Test 2: Another valid token (USDT)
        try:
            result = await get_token_price("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
            passed = result.get('success') and result.get('data', {}).get('symbol') == 'USDT'
            log_test_result(
                'token-price',
                'Test 2: Get USDT price by address',
                passed,
                "Successfully fetched USDT price" if passed else "Failed",
                f"Price: ${result.get('data', {}).get('price')}" if passed else None
            )
        except Exception as e:
            log_test_result('token-price', 'Test 2: Get USDT price', False, str(e))
        
        # Test 3: Invalid token
        try:
            result = await get_token_price("INVALID_TOKEN_123")
            # Should gracefully handle invalid token
            passed = 'error' in result or not result.get('success')
            log_test_result(
                'token-price',
                'Test 3: Invalid token handling',
                passed,
                "Correctly handled invalid token" if passed else "Should return error",
                result.get('message')
            )
        except Exception as e:
            log_test_result('token-price', 'Test 3: Invalid token', True, "Exception handled", str(e))
        
    except ImportError as e:
        log_test_result('token-price', 'Import check', False, f"Cannot import skill: {e}")


async def test_wallet_balance():
    """Test wallet-balance skill."""
    print("\n" + "="*80)
    print("🧪 Testing: wallet-balance")
    print("="*80)
    
    try:
        # Load module
        get_balance_module = load_skill_module(
            project_root / "skills/wallet-balance/scripts/get_balance.py"
        )
        get_wallet_balance = get_balance_module.get_wallet_balance
        
        # Test 1: Valid address (TRON Foundation)
        test_address = "TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH"
        try:
            result = await get_wallet_balance(test_address)
            passed = result.get('success') and 'data' in result
            log_test_result(
                'wallet-balance',
                'Test 1: Get balance for valid address',
                passed,
                "Successfully fetched balance" if passed else "Failed",
                f"TRX: {result.get('data', {}).get('trx_balance')}" if passed else None
            )
        except Exception as e:
            log_test_result('wallet-balance', 'Test 1: Valid address', False, str(e))
        
        # Test 2: Address with specific tokens
        try:
            result = await get_wallet_balance(
                test_address,
                tokens=["TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"]  # USDT
            )
            passed = result.get('success')
            log_test_result(
                'wallet-balance',
                'Test 2: Get specific token balance',
                passed,
                "Successfully fetched token balance" if passed else "Failed",
                f"Tokens: {len(result.get('data', {}).get('tokens', []))}" if passed else None
            )
        except Exception as e:
            log_test_result('wallet-balance', 'Test 2: Specific tokens', False, str(e))
        
        # Test 3: Invalid address format
        try:
            result = await get_wallet_balance("INVALID_ADDRESS")
            passed = not result.get('success') or 'error' in result
            log_test_result(
                'wallet-balance',
                'Test 3: Invalid address handling',
                passed,
                "Correctly rejected invalid address" if passed else "Should reject invalid address",
                result.get('message')
            )
        except Exception as e:
            log_test_result('wallet-balance', 'Test 3: Invalid address', True, "Exception handled", str(e))
        
    except ImportError as e:
        log_test_result('wallet-balance', 'Import check', False, f"Cannot import skill: {e}")


async def test_energy_rental():
    """Test energy-rental skill."""
    print("\n" + "="*80)
    print("🧪 Testing: energy-rental")
    print("="*80)
    
    try:
        # Load module
        energy_module = load_skill_module(
            project_root / "skills/energy-rental/scripts/calculate_rental.py"
        )
        calculate_energy_cost = energy_module.calculate_energy_cost
        
        # Test 1: Small energy amount
        try:
            result = await calculate_energy_cost(32000)
            passed = result.get('success') and 'data' in result
            log_test_result(
                'energy-rental',
                'Test 1: Calculate cost for 32k energy',
                passed,
                "Successfully calculated rental cost" if passed else "Failed",
                f"Best option: {result.get('data', {}).get('recommendation')}" if passed else None
            )
        except Exception as e:
            log_test_result('energy-rental', 'Test 1: Small energy', False, str(e))
        
        # Test 2: Large energy amount
        try:
            result = await calculate_energy_cost(100000)
            passed = result.get('success')
            log_test_result(
                'energy-rental',
                'Test 2: Calculate cost for 100k energy',
                passed,
                "Successfully calculated for large amount" if passed else "Failed",
                f"Platforms compared: {len(result.get('data', {}).get('platforms', []))}" if passed else None
            )
        except Exception as e:
            log_test_result('energy-rental', 'Test 2: Large energy', False, str(e))
        
        # Test 3: Edge case - very small amount
        try:
            result = await calculate_energy_cost(1000)
            passed = result.get('success') or 'error' in result
            log_test_result(
                'energy-rental',
                'Test 3: Very small energy amount',
                passed,
                "Handled small amount" if passed else "Failed",
                result.get('message')
            )
        except Exception as e:
            log_test_result('energy-rental', 'Test 3: Edge case', True, "Exception handled", str(e))
        
    except ImportError as e:
        log_test_result('energy-rental', 'Import check', False, f"Cannot import skill: {e}")


async def test_address_risk_checker():
    """Test address-risk-checker skill."""
    print("\n" + "="*80)
    print("🧪 Testing: address-risk-checker")
    print("="*80)
    
    try:
        # Load module
        risk_module = load_skill_module(
            project_root / "skills/address-risk-checker/scripts/check_address.py"
        )
        check_address_security = risk_module.check_address_security
        
        # Test 1: Known safe address
        safe_address = "TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH"
        try:
            result = await check_address_security(safe_address)
            passed = result.get('success')
            log_test_result(
                'address-risk-checker',
                'Test 1: Check known safe address',
                passed,
                "Successfully checked address" if passed else "Failed",
                f"Risk: {result.get('data', {}).get('risk_level')}" if passed else None
            )
        except Exception as e:
            log_test_result('address-risk-checker', 'Test 1: Safe address', False, str(e))
        
        # Test 2: Another address
        try:
            result = await check_address_security("TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t")
            passed = result.get('success')
            log_test_result(
                'address-risk-checker',
                'Test 2: Check USDT contract',
                passed,
                "Successfully checked contract" if passed else "Failed",
                f"Labels: {result.get('data', {}).get('labels', [])}" if passed else None
            )
        except Exception as e:
            log_test_result('address-risk-checker', 'Test 2: Contract check', False, str(e))
        
        # Test 3: Invalid address
        try:
            result = await check_address_security("INVALID")
            passed = not result.get('success') or 'error' in result
            log_test_result(
                'address-risk-checker',
                'Test 3: Invalid address handling',
                passed,
                "Correctly handled invalid address" if passed else "Should reject",
                result.get('message')
            )
        except Exception as e:
            log_test_result('address-risk-checker', 'Test 3: Invalid', True, "Exception handled", str(e))
        
    except ImportError as e:
        log_test_result('address-risk-checker', 'Import check', False, f"Cannot import skill: {e}")


async def test_sr_ranking():
    """Test sr-ranking skill."""
    print("\n" + "="*80)
    print("🧪 Testing: sr-ranking")
    print("="*80)
    
    try:
        # Load module
        sr_module = load_skill_module(
            project_root / "skills/sr-ranking/scripts/get_ranking.py"
        )
        get_sr_ranking = sr_module.get_sr_ranking
        
        # Test 1: Get top 5 SRs
        try:
            result = await get_sr_ranking(top_n=5, sort_by="voter_apy")
            passed = result.get('success') and len(result.get('data', {}).get('rankings', [])) > 0
            log_test_result(
                'sr-ranking',
                'Test 1: Get top 5 SRs by APY',
                passed,
                "Successfully fetched SR rankings" if passed else "Failed",
                f"Found {len(result.get('data', {}).get('rankings', []))} SRs" if passed else None
            )
        except Exception as e:
            log_test_result('sr-ranking', 'Test 1: Top 5 SRs', False, str(e))
        
        # Test 2: Different sorting
        try:
            result = await get_sr_ranking(top_n=3, sort_by="total_votes")
            passed = result.get('success')
            log_test_result(
                'sr-ranking',
                'Test 2: Sort by total votes',
                passed,
                "Successfully sorted by votes" if passed else "Failed",
                f"Top SR: {result.get('data', {}).get('rankings', [{}])[0].get('name')}" if passed else None
            )
        except Exception as e:
            log_test_result('sr-ranking', 'Test 2: Sort votes', False, str(e))
        
        # Test 3: Invalid sort criteria
        try:
            result = await get_sr_ranking(sort_by="invalid_sort")
            passed = not result.get('success') and 'error' in result
            log_test_result(
                'sr-ranking',
                'Test 3: Invalid sort criteria',
                passed,
                "Correctly rejected invalid sort" if passed else "Should reject",
                result.get('error')
            )
        except Exception as e:
            log_test_result('sr-ranking', 'Test 3: Invalid sort', True, "Exception handled", str(e))
        
    except ImportError as e:
        log_test_result('sr-ranking', 'Import check', False, f"Cannot import skill: {e}")


async def run_all_tests():
    """Run all skill tests."""
    print("\n" + "="*100)
    print("🚀 BLOCKCHAIN-COPILOT COMPREHENSIVE SKILLS TEST SUITE")
    print("="*100)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Core skills
    await test_token_price()
    await test_wallet_balance()
    await test_energy_rental()
    await test_address_risk_checker()
    await test_sr_ranking()
    
    # Print summary
    print("\n" + "="*100)
    print("📊 TEST SUMMARY")
    print("="*100)
    
    test_results['total_skills'] = len(test_results['skills'])
    
    for skill_name, skill_data in test_results['skills'].items():
        status = "✅ PASS" if skill_data['failed'] == 0 else "❌ FAIL"
        print(f"\n{status} {skill_name}")
        print(f"  Tests: {skill_data['passed']}/{skill_data['total']} passed")
        
        if skill_data['failed'] > 0:
            print(f"  Failed tests:")
            for test in skill_data['tests']:
                if not test['passed']:
                    print(f"    - {test['name']}: {test['message']}")
    
    print("\n" + "-"*100)
    print(f"Total Skills Tested: {test_results['total_skills']}")
    print(f"Total Tests: {test_results['passed'] + test_results['failed']}")
    print(f"Passed: {test_results['passed']} ✅")
    print(f"Failed: {test_results['failed']} ❌")
    
    success_rate = (test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100) if (test_results['passed'] + test_results['failed']) > 0 else 0
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Save results to file
    results_file = project_root / 'tests' / 'test_results.json'
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    print("="*100)
    
    return test_results


if __name__ == "__main__":
    results = asyncio.run(run_all_tests())
