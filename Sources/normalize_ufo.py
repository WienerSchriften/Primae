#!/usr/bin/env python3
"""
Script to normalize all UFO files recursively
Usage: python3 normalize_ufo.py [directory]
If no directory is specified, uses current directory
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def normalize_ufo_files(target_dir="."):
    """
    Find and normalize all UFO files in the target directory and subdirectories.
    
    Args:
        target_dir (str): Directory to search for UFO files
        
    Returns:
        tuple: (success_count, total_count)
    """
    target_path = Path(target_dir).resolve()
    
    print(f"Normalizing UFO files in: {target_path}")
    print("=" * 50)
    
    # Find all .ufo directories
    ufo_dirs = list(target_path.rglob("*.ufo"))
    
    if not ufo_dirs:
        print("No UFO files found.")
        return 0, 0
    
    success_count = 0
    total_count = len(ufo_dirs)
    
    for ufo_dir in ufo_dirs:
        print(f"Processing: {ufo_dir}")
        
        try:
            # Run ufonormalizer on the UFO directory
            result = subprocess.run(
                ["ufonormalizer", str(ufo_dir)],
                capture_output=True,
                text=True,
                check=True
            )
            
            print(f"✓ Successfully normalized: {ufo_dir}")
            success_count += 1
            
            # Print any output from ufonormalizer if verbose
            if result.stdout.strip():
                print(f"  Output: {result.stdout.strip()}")
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to normalize: {ufo_dir}")
            print(f"  Error: {e.stderr.strip() if e.stderr else str(e)}")
            
        except FileNotFoundError:
            print(f"✗ Error: ufonormalizer command not found")
            print("  Please ensure ufonormalizer is installed and in your PATH")
            break
            
        except Exception as e:
            print(f"✗ Unexpected error processing {ufo_dir}: {str(e)}")
            
        print("-" * 30)
    
    print("=" * 50)
    print("Normalization complete!")
    print(f"Successfully processed: {success_count}/{total_count} UFO files")
    
    return success_count, total_count


def main():
    """Main function to handle command line arguments and run the normalization."""
    parser = argparse.ArgumentParser(
        description="Normalize all UFO files recursively in a directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 normalize_ufo.py                    # Process current directory
  python3 normalize_ufo.py /path/to/fonts     # Process specific directory
  python3 normalize_ufo.py .                  # Process current directory explicitly
        """
    )
    
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to search for UFO files (default: current directory)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose output from ufonormalizer"
    )
    
    args = parser.parse_args()
    
    # Check if target directory exists
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist")
        sys.exit(1)
    
    # Check if target is a directory
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory")
        sys.exit(1)
    
    # Run the normalization
    success_count, total_count = normalize_ufo_files(args.directory)
    
    # Exit with appropriate code
    if success_count == total_count:
        sys.exit(0)  # All successful
    elif success_count > 0:
        sys.exit(1)  # Partial success
    else:
        sys.exit(2)  # Complete failure


if __name__ == "__main__":
    main()
