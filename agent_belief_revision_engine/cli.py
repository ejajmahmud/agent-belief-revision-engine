"""CLI for agent-belief-revision-engine."""
import sys
import argparse
from .engine import BeliefRevisionEngine


def main():
    parser = argparse.ArgumentParser(description="Agent Belief Revision Engine")
    parser.add_argument("--demo", action="store_true", help="Run belief revision demonstration")
    args = parser.parse_args()

    engine = BeliefRevisionEngine()
    if args.demo:
        engine.add_belief("db_type", "sqlite", entrenchment=0.5)
        engine.add_belief("use_in_memory", True, entrenchment=0.8, derived_from=["db_type"])
        print("Initial beliefs:", engine.get_beliefs())
        retracted = engine.revise("db_type", "postgres", entrenchment=0.9)
        print("Retracted beliefs due to contradiction:", retracted)
        print("Updated consistent beliefs:", engine.get_beliefs())
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
