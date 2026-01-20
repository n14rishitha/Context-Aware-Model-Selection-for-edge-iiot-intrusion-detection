"""
Attack Surface Coverage (ASC) Scoring Calculator
================================================
This script calculates the ASC composite score for IDS models based on:
- Detection Coverage (TPR) - 35% weight
- False Positive Minimization (FPR_Min) - 35% weight
- Novel Attack Adaptability - 15% weight
- Inference Efficiency - 15% weight

Usage:
    python asc_calculator.py
    
Then enter your model's metrics when prompted.
"""


def calculate_tpr(true_positives: int = None, false_negatives: int = None, 
                  recall: float = None) -> float:
    """
    Calculate True Positive Rate (Detection Coverage).
    Equation: TPR = (TP / (TP + FN)) × 100
    
    Args:
        true_positives: Number of true positives
        false_negatives: Number of false negatives
        recall: Recall percentage (if already calculated)
    
    Returns:
        TPR percentage (0-100)
    """
    if recall is not None:
        return recall
    return (true_positives / (true_positives + false_negatives)) * 100


def calculate_fpr_min(fpr: float) -> float:
    """
    Calculate False Positive Minimization score.
    Equation: FPR_m = (1 - FPR) × 100
    
    Args:
        fpr: False Positive Rate as a decimal (e.g., 0.002 for 0.2%)
    
    Returns:
        FPR Minimization score (0-100, higher is better)
    """
    return (1 - fpr) * 100


def get_novel_attack_score(architecture_type: str) -> int:
    """
    Get Novel Attack Adaptability score based on architecture type.
    
    Args:
        architecture_type: One of 'attention', 'hybrid', 'traditional'
    
    Returns:
        Novel Attack Adaptability score (70, 80, or 90)
    """
    scores = {
        'attention': 90,  # Attention-based architectures
        'hybrid': 80,     # Hybrid architectures (non-attention)
        'traditional': 70  # Traditional ML models
    }
    return scores.get(architecture_type.lower(), 70)


def calculate_inference_efficiency(model_inference_time: float, 
                                   fastest_inference_time: float) -> float:
    """
    Calculate Inference Efficiency score.
    Equation: I = (T_f / T_m) × 100
    
    Args:
        model_inference_time: Inference time of the model (seconds)
        fastest_inference_time: Fastest inference time among all models (seconds)
    
    Returns:
        Inference Efficiency score (0-100)
    """
    return (fastest_inference_time / model_inference_time) * 100


def calculate_asc(tpr: float, fpr_min: float, novel_attack: float, 
                  inference_eff: float) -> float:
    """
    Calculate Attack Surface Coverage composite score.
    Equation: ASC = (0.35×TPR) + (0.35×FPR_m) + (0.15×N) + (0.15×I)
    
    Args:
        tpr: True Positive Rate (0-100)
        fpr_min: False Positive Minimization score (0-100)
        novel_attack: Novel Attack Adaptability score (70, 80, or 90)
        inference_eff: Inference Efficiency score (0-100)
    
    Returns:
        ASC composite score
    """
    return (0.35 * tpr) + (0.35 * fpr_min) + (0.15 * novel_attack) + (0.15 * inference_eff)


def main():
    print("=" * 60)
    print("  ATTACK SURFACE COVERAGE (ASC) CALCULATOR")
    print("=" * 60)
    print("\nThis calculator computes the ASC composite score for your IDS model.")
    print("Weights: TPR (35%), FPR_Min (35%), Novel Attack (15%), Inference (15%)\n")
    
    # Get user inputs
    print("-" * 40)
    print("DETECTION COVERAGE (TPR)")
    print("-" * 40)
    input_type = input("Do you have (1) Recall/TPR directly or (2) TP and FN counts? [1/2]: ").strip()
    
    if input_type == '2':
        tp = int(input("Enter True Positives (TP): "))
        fn = int(input("Enter False Negatives (FN): "))
        tpr = calculate_tpr(true_positives=tp, false_negatives=fn)
    else:
        tpr = float(input("Enter Recall/TPR (0-100%): "))
    
    print("\n" + "-" * 40)
    print("FALSE POSITIVE MINIMIZATION")
    print("-" * 40)
    fpr_input = input("Enter FPR as percentage (e.g., 0.002 for 0.002%) or decimal (e.g., 0.00002): ")
    fpr_value = float(fpr_input)
    
    # Determine if input is percentage or decimal
    if fpr_value > 1:
        fpr = fpr_value / 100  # Convert percentage to decimal
    else:
        fpr = fpr_value
    
    fpr_min = calculate_fpr_min(fpr)
    
    print("\n" + "-" * 40)
    print("NOVEL ATTACK ADAPTABILITY")
    print("-" * 40)
    print("Architecture types and their scores:")
    print("  1. Attention-based (LSTM-CNN-Attention, Transformers): 90")
    print("  2. Hybrid (CNN-GRU-LSTM, CNN-LSTM, etc.): 80")
    print("  3. Traditional ML (Decision Trees, Random Forest, etc.): 70")
    
    arch_choice = input("\nSelect architecture type [1/2/3]: ").strip()
    arch_map = {'1': 'attention', '2': 'hybrid', '3': 'traditional'}
    architecture = arch_map.get(arch_choice, 'traditional')
    novel_attack = get_novel_attack_score(architecture)
    
    print("\n" + "-" * 40)
    print("INFERENCE EFFICIENCY")
    print("-" * 40)
    model_infer_time = float(input("Enter your model's inference time (seconds): "))
    fastest_infer_time = float(input("Enter fastest inference time among compared models (seconds): "))
    
    inference_eff = calculate_inference_efficiency(model_infer_time, fastest_infer_time)
    
    # Calculate ASC
    asc_score = calculate_asc(tpr, fpr_min, novel_attack, inference_eff)
    
    # Display results
    print("\n" + "=" * 60)
    print("  COMPONENT SCORES")
    print("=" * 60)
    print(f"  True Positive Rate (TPR):           {tpr:.2f}")
    print(f"  False Positive Rate (FPR):          {fpr:.6f}")
    print(f"  FPR Minimization (FPR_m):           {fpr_min:.4f}")
    print(f"  Novel Attack Adaptability:          {novel_attack}")
    print(f"  Inference Efficiency:               {inference_eff:.2f}")
    
    print("\n" + "=" * 60)
    print("  WEIGHTED CONTRIBUTIONS")
    print("=" * 60)
    print(f"  TPR × 0.35:            {tpr:.2f} × 0.35 = {tpr * 0.35:.2f}")
    print(f"  FPR_m × 0.35:          {fpr_min:.2f} × 0.35 = {fpr_min * 0.35:.2f}")
    print(f"  Novel Attack × 0.15:   {novel_attack} × 0.15 = {novel_attack * 0.15:.2f}")
    print(f"  Inference × 0.15:      {inference_eff:.2f} × 0.15 = {inference_eff * 0.15:.2f}")
    
    print("\n" + "=" * 60)
    print("  ATTACK SURFACE COVERAGE SCORE")
    print("=" * 60)
    print(f"\n  ★ ASC SCORE: {asc_score:.2f}")
    
    print("\n  Formula: ASC = (0.35×TPR) + (0.35×FPR_m) + (0.15×N) + (0.15×I)")
    print(f"         = (0.35×{tpr:.2f}) + (0.35×{fpr_min:.2f}) + (0.15×{novel_attack}) + (0.15×{inference_eff:.2f})")
    print(f"         = {asc_score:.2f}")
    
    # Interpretation
    print("\n" + "-" * 40)
    print("INTERPRETATION")
    print("-" * 40)
    if asc_score >= 97:
        print("  Excellent security coverage - suitable for high-security IIoT environments")
    elif asc_score >= 95:
        print("  Very good security coverage - suitable for most industrial deployments")
    elif asc_score >= 90:
        print("  Good security coverage - adequate for standard IIoT applications")
    else:
        print("  Moderate security coverage - consider improvements for critical infrastructure")
    


if __name__ == "__main__":
    main()

