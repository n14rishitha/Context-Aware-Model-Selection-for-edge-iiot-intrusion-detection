"""
IDS Evaluation Framework - Main Calculator
==========================================
This script provides a unified interface to run all evaluation calculators:
1. PFO (Pareto Frontier Optimization)
2. ASC (Attack Surface Coverage)
3. TCO (Total Cost of Ownership)
4. Synthesis Engine (Final Ranking)

Usage:
    python main_calculator.py
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_header():
    """Print the main header."""
    print("\n" + "=" * 70)
    print("  IDS MULTI-DIMENSIONAL EVALUATION FRAMEWORK")
    print("  Calculator Suite for Intrusion Detection System Evaluation")
    print("=" * 70)


def print_menu():
    """Print the main menu."""
    print("\n" + "-" * 50)
    print("  AVAILABLE CALCULATORS")
    print("-" * 50)
    print("  1. PFO Calculator - Pareto Frontier Optimization")
    print("     (Detection, Efficiency, Deployment trade-offs)")
    print()
    print("  2. ASC Calculator - Attack Surface Coverage")
    print("     (TPR, FPR, Novel Attack, Inference Efficiency)")
    print()
    print("  3. TCO Calculator - Total Cost of Ownership")
    print("     (5-year deployment economics)")
    print()
    print("  4. Synthesis Engine - Final Model Ranking")
    print("     (Combine all metrics with weighted scoring)")
    print()
    print("  5. Complete Evaluation - Run All Calculators")
    print("     (Full evaluation pipeline)")
    print()
    print("  0. Exit")
    print("-" * 50)


def run_pfo():
    """Run PFO calculator."""
    try:
        from pfo_calculator import main as pfo_main
        pfo_main()
    except ImportError:
        exec(open('pfo_calculator.py').read())


def run_asc():
    """Run ASC calculator."""
    try:
        from asc_calculator import main as asc_main
        asc_main()
    except ImportError:
        exec(open('asc_calculator.py').read())


def run_tco():
    """Run TCO calculator."""
    try:
        from tco_calculator import main as tco_main
        tco_main()
    except ImportError:
        exec(open('tco_calculator.py').read())


def run_synthesis():
    """Run Synthesis Engine calculator."""
    try:
        from synthesis_calculator import main as synthesis_main
        synthesis_main()
    except ImportError:
        exec(open('synthesis_calculator.py').read())


def run_complete_evaluation():
    """Run complete evaluation with all metrics collected."""
    print("\n" + "=" * 70)
    print("  COMPLETE MODEL EVALUATION")
    print("=" * 70)
    print("\nThis will collect all required metrics and compute all scores.\n")
    
    # Collect all inputs once
    print("-" * 50)
    print("MODEL IDENTIFICATION")
    print("-" * 50)
    model_name = input("Enter model name: ")
    
    print("\n" + "-" * 50)
    print("DETECTION METRICS")
    print("-" * 50)
    accuracy = float(input("Accuracy (0-100%): "))
    f1_score = float(input("F1-Score (0-100%): "))
    
    print("\n" + "-" * 50)
    print("EFFICIENCY METRICS")
    print("-" * 50)
    training_time = float(input("Training Time (seconds): "))
    inference_time = float(input("Inference Time per sample (seconds): "))
    
    print("\n" + "-" * 50)
    print("DEPLOYMENT METRICS")
    print("-" * 50)
    model_size = float(input("Model Size (MB): "))
    edge_input = input("Is edge-deployable? (yes/no): ").strip().lower()
    is_edge = edge_input in ['yes', 'y', 'true', '1']
    
    if is_edge:
        edge_score = 1.0
    elif model_size < 10:
        edge_score = 0.8
    else:
        edge_score = 0.2
    
    print("\n" + "-" * 50)
    print("SECURITY METRICS")
    print("-" * 50)
    recall = float(input("Recall/TPR (0-100%): "))
    fpr_input = input("False Positive Rate (e.g., 0.002 for 0.2%): ")
    fpr = float(fpr_input)
    
    print("\n  Architecture types:")
    print("  1. Attention-based (Score: 90)")
    print("  2. Hybrid (Score: 80)")
    print("  3. Traditional ML (Score: 70)")
    arch_choice = input("Select architecture [1/2/3]: ").strip()
    arch_scores = {'1': 90, '2': 80, '3': 70}
    novel_attack = arch_scores.get(arch_choice, 70)
    
    print("\n" + "-" * 50)
    print("INTERPRETABILITY")
    print("-" * 50)
    print("  1. High (Decision Trees, Rule-based)")
    print("  2. Medium (Hybrid with some explainability)")
    print("  3. Low (Deep neural networks)")
    interp_choice = input("Select level [1/2/3]: ").strip()
    interp_map = {'1': ('high', 1.0), '2': ('medium', 0.5), '3': ('low', 0.2)}
    interp_label, interp_score = interp_map.get(interp_choice, ('low', 0.2))
    
    print("\n" + "-" * 50)
    print("COMPARISON CONTEXT (for normalization)")
    print("-" * 50)
    fastest_infer = float(input("Fastest inference time among all models (seconds): "))
    
    # ============ CALCULATIONS ============
    
    # PFO Calculations
    detection_score = (accuracy * f1_score) / 10000
    efficiency_score = (1 / training_time) * (1 / inference_time)
    deployment_score = (1 / model_size) * edge_score
    
    # ASC Calculations
    tpr = recall
    fpr_min = (1 - fpr) * 100
    inference_eff = (fastest_infer / inference_time) * 100
    asc_score = (0.35 * tpr) + (0.35 * fpr_min) + (0.15 * novel_attack) + (0.15 * inference_eff)
    
    # TCO Calculations (using default parameters)
    N, Y, F = 1000, 5, 10000
    
    # Deployment Cost
    c_infra = 50000
    c_hw = 350 * model_size
    c_net = 10000 if is_edge else 50000
    c_int = 20000 if is_edge else 100000
    dep_cost = c_infra + c_hw + c_net + c_int
    
    # Operational Cost
    training_hours = training_time / 3600
    c_train = training_hours * N * 1 * Y * 2
    total_flows = F * N * 365 * Y
    c_infer = (total_flows * inference_time / 3600) * 0.5
    c_energy = 90 * N * Y
    op_cost = c_train + c_infer + c_energy
    
    # Incident Response Cost
    false_alerts = fpr * total_flows
    cost_per_alert = (10/60) * 75
    ir_cost = false_alerts * cost_per_alert
    
    # Scalability Cost
    if is_edge:
        sc_cost = 80000 * edge_score
    else:
        sc_cost = 50000
    
    # Compliance Cost
    opacity = 1 / interp_score
    cc_cost = 120000 * opacity
    
    # Total TCO
    tco = dep_cost + op_cost + ir_cost + sc_cost + cc_cost
    
    # ============ DISPLAY RESULTS ============
    
    print("\n" + "=" * 70)
    print(f"  EVALUATION RESULTS: {model_name}")
    print("=" * 70)
    
    print("\n" + "-" * 50)
    print("  PFO SCORES")
    print("-" * 50)
    print(f"  Detection Score (D):      {detection_score:.6f}")
    print(f"  Efficiency Score (E):     {efficiency_score:.6f}")
    print(f"  Deployment Score (P):     {deployment_score:.6f}")
    print(f"  Edge Compatibility (α):   {edge_score}")
    
    print("\n" + "-" * 50)
    print("  ASC SCORES")
    print("-" * 50)
    print(f"  TPR (Detection Coverage): {tpr:.2f}")
    print(f"  FPR Minimization:         {fpr_min:.4f}")
    print(f"  Novel Attack Score:       {novel_attack}")
    print(f"  Inference Efficiency:     {inference_eff:.2f}")
    print(f"  ─────────────────────────────")
    print(f"  ★ ASC COMPOSITE SCORE:    {asc_score:.2f}")
    
    print("\n" + "-" * 50)
    print("  TCO BREAKDOWN (5-Year)")
    print("-" * 50)
    print(f"  Deployment (DEP):         ${dep_cost:,.0f}")
    print(f"  Operational (OP):         ${op_cost:,.0f}")
    print(f"  Incident Response (IR):   ${ir_cost:,.0f}")
    print(f"  Scalability (SC):         ${sc_cost:,.0f}")
    print(f"  Compliance (CC):          ${cc_cost:,.0f}")
    print(f"  ─────────────────────────────")
    print(f"  ★ TOTAL 5-YEAR TCO:       ${tco:,.0f}")
    
    print("\n" + "-" * 50)
    print("  SUMMARY METRICS")
    print("-" * 50)
    print(f"  Detection Score:          {detection_score:.4f} (target: 1.0)")
    print(f"  ASC Score:                {asc_score:.2f} (target: 100)")
    print(f"  5-Year TCO:               ${tco:,.0f}")
    
    print("\n" + "=" * 70)
    print("  NOTE: For final ranking, use the Synthesis Engine (Option 4)")
    print("  with normalized scores from multiple model comparison.")
    print("=" * 70)
    
    # Ask to save results
    save = input("\nSave results to file? (yes/no): ").strip().lower()
    if save in ['yes', 'y']:
        filename = f"{model_name.replace(' ', '_')}_evaluation.txt"
        with open(filename, 'w') as f:
            f.write(f"IDS EVALUATION RESULTS: {model_name}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Detection Score: {detection_score:.6f}\n")
            f.write(f"ASC Score: {asc_score:.2f}\n")
            f.write(f"5-Year TCO: ${tco:,.0f}\n")
            f.write(f"\nPFO Components:\n")
            f.write(f"  Efficiency: {efficiency_score:.6f}\n")
            f.write(f"  Deployment: {deployment_score:.6f}\n")
            f.write(f"\nASC Components:\n")
            f.write(f"  TPR: {tpr:.2f}\n")
            f.write(f"  FPR_Min: {fpr_min:.4f}\n")
            f.write(f"  Novel Attack: {novel_attack}\n")
            f.write(f"  Inference Eff: {inference_eff:.2f}\n")
            f.write(f"\nTCO Components:\n")
            f.write(f"  DEP: ${dep_cost:,.0f}\n")
            f.write(f"  OP: ${op_cost:,.0f}\n")
            f.write(f"  IR: ${ir_cost:,.0f}\n")
            f.write(f"  SC: ${sc_cost:,.0f}\n")
            f.write(f"  CC: ${cc_cost:,.0f}\n")
        print(f"  Results saved to: {filename}")


def main():
    """Main entry point."""
    print_header()
    
    while True:
        print_menu()
        choice = input("\n  Enter your choice [0-5]: ").strip()
        
        if choice == '1':
            run_pfo()
        elif choice == '2':
            run_asc()
        elif choice == '3':
            run_tco()
        elif choice == '4':
            run_synthesis()
        elif choice == '5':
            run_complete_evaluation()
        elif choice == '0':
            print("\n  Thank you for using the IDS Evaluation Framework!")
            print("  Goodbye.\n")
            break
        else:
            print("\n  ⚠️  Invalid choice. Please enter 0-5.")
        
        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()

