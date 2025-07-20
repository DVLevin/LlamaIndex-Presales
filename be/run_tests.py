"""
Test runner script for backend tests
"""
import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all backend tests"""
    # Add the parent directory to Python path so imports work
    backend_dir = Path(__file__).parent
    project_root = backend_dir.parent
    
    # Add paths to sys.path for imports
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(backend_dir))
    
    # Run pytest with proper configuration
    cmd = [
        sys.executable, 
        "-m", 
        "pytest", 
        str(backend_dir / "tests"),
        "-v",
        "--tb=short"
    ]
    
    print(f"Running backend tests from: {backend_dir}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)