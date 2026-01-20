"""
Pareto Frontier Optimization (PFO) Calculator
=============================================
This script calculates the PFO composite score for IDS models based on:
- Detection Performance (Accuracy × F1-Score)
- Computational Efficiency (Training Time, Inference Time)
- Deployment Feasibility (Model Size, Edge Compatibility)

Usage:
    python pfo_calculator.py
    
Then enter your model's metrics when prompted.
"""


def calculate_detection_score(accuracy: float, f1_score: float) -> float:
    """
    Calculate Detection Score using Equation: D = (Acc × F1) / 10000
    
    Args:
        accuracy: Accuracy percentage (0-100)
        f1_score: F1-Score percentage (0-100)
    
    Returns:
        Detection Score (0-1 range)
    """
    return (accuracy * f1_score) / 10000


def calculate_efficiency_score(training_time: float, inference_time: float) -> float:
    """
    Calculate Efficiency Score using Equation: E = (1/T_t) × (1/T_i)
    
    Args:
        training_time: Training time in seconds
        inference_time: Inference time in seconds
    
    Returns:
        Efficiency Score
    """
    return (1 / training_time) * (1 / inference_time)


def get_edge_compatibility(is_edge_deployable: bool, model_size_mb: float) -> float:
    """
    Get Edge Compatibility factor (α) based on model characteristics.
    
    Args:
        is_edge_deployable: Whether model is validated for edge deployment
        model_size_mb: Model size in megabytes
    
    Returns:
        Edge Compatibility factor (0.2, 0.8, or 1.0)
    """
    if is_edge_deployable:
        return 1.0
    elif model_size_mb < 10:
        return 0.8
    else:
        return 0.2


def calculate_deployment_score(model_size_mb: float, edge_compatibility: float) -> float:
    """
    Calculate Deployment Score using Equation: P = (1/S_m) × α
    
    Args:
        model_size_mb: Model size in megabytes
        edge_compatibility: Edge compatibility factor (α)
    
    Returns:
        Deployment Score
    """
    return (1 / model_size_mb) * edge_compatibility


def normalize_score(score: float, min_val: float, max_val: float) -> float:
    """
    Normalize score to 0-1 range using min-max normalization.
    Equation: S_n = (S - S_min) / (S_max - S_min)
    
    Args:
        score: Raw score to normalize
        min_val: Minimum value in the dataset
        max_val: Maximum value in the dataset
    
    Returns:
        Normalized score (0-1 range)
    """
    if max_val == min_val:
        return 0.0
    return (score - min_val) / (max_val - min_val)


def calculate_composite_pfo(detection: float, efficiency_norm: float, deployment_norm: float) -> float:
    """
    Calculate Composite PFO Score using Equation: C = (1/3)×D + (1/3)×E_n + (1/3)×P_n
    
    Args:
        detection: Detection Score (already 0-1 range)
        efficiency_norm: Normalized Efficiency Score (0-1 range)
        deployment_norm: Normalized Deployment Score (0-1 range)
    
    Returns:
        Composite PFO Score
    """
    return (1/3) * detection + (1/3) * efficiency_norm + (1/3) * deployment_norm


def main():
    print("=" * 60)
    print("  PARETO FRONTIER OPTIMIZATION (PFO) CALCULATOR")
    print("=" * 60)
    print("\nThis calculator computes the PFO composite score for your IDS model.")
    print("Equal weights (33.33% each) are applied to Detection, Efficiency, and Deployment.\n")
    
    # Get user inputs
    print("-" * 40)
    print("DETECTION PERFORMANCE METRICS")
    print("-" * 40)
    accuracy = float(input("Enter Accuracy (0-100%): "))
    f1_score = float(input("Enter F1-Score (0-100%): "))
    
    print("\n" + "-" * 40)
    print("COMPUTATIONAL EFFICIENCY METRICS")
    print("-" * 40)
    training_time = float(input("Enter Training Time (seconds): "))
    inference_time = float(input("Enter Inference Time (seconds): "))
    
    print("\n" + "-" * 40)
    print("DEPLOYMENT FEASIBILITY METRICS")
    print("-" * 40)
    model_size = float(input("Enter Model Size (MB): "))
    edge_input = input("Is the model edge-deployable? (yes/no): ").strip().lower()
    is_edge_deployable = edge_input in ['yes', 'y', 'true', '1']
    
    # Calculate scores
    detection_score = calculate_detection_score(accuracy, f1_score)
    efficiency_score = calculate_efficiency_score(training_time, inference_time)
    edge_compatibility = get_edge_compatibility(is_edge_deployable, model_size)
    deployment_score = calculate_deployment_score(model_size, edge_compatibility)
    
    print("\n" + "=" * 60)
    print("  RAW SCORES")
    print("=" * 60)
    print(f"  Detection Score (D):     {detection_score:.6f}")
    print(f"  Efficiency Score (E):    {efficiency_score:.6f}")
    print(f"  Deployment Score (P):    {deployment_score:.6f}")
    print(f"  Edge Compatibility (α):  {edge_compatibility}")
    
    # For single model, show unnormalized composite
    # In practice, normalization requires comparison with other models
    print("\n" + "-" * 40)
    print("NORMALIZATION (For comparison with other models)")
    print("-" * 40)
    
    compare = input("\nDo you want to compare with baseline models? (yes/no): ").strip().lower()
    
    if compare in ['yes', 'y']:
        print("\nEnter min/max values from your model set:")
        eff_min = float(input("  Efficiency Score MIN: "))
        eff_max = float(input("  Efficiency Score MAX: "))
        dep_min = float(input("  Deployment Score MIN: "))
        dep_max = float(input("  Deployment Score MAX: "))
        
        efficiency_norm = normalize_score(efficiency_score, eff_min, eff_max)
        deployment_norm = normalize_score(deployment_score, dep_min, dep_max)
        
        composite_pfo = calculate_composite_pfo(detection_score, efficiency_norm, deployment_norm)
        
        print("\n" + "=" * 60)
        print("  NORMALIZED SCORES")
        print("=" * 60)
        print(f"  Efficiency Normalized (E_n):  {efficiency_norm:.6f}")
        print(f"  Deployment Normalized (P_n):  {deployment_norm:.6f}")
        
        print("\n" + "=" * 60)
        print("  COMPOSITE PFO SCORE")
        print("=" * 60)
        print(f"\n  ★ COMPOSITE PFO SCORE: {composite_pfo:.4f}")
        print(f"\n  Formula: C = (1/3)×{detection_score:.4f} + (1/3)×{efficiency_norm:.4f} + (1/3)×{deployment_norm:.4f}")
    else:
        print("\n" + "=" * 60)
        print("  STANDALONE COMPOSITE (Using raw scores)")
        print("=" * 60)
        # Use raw scores scaled to 0-1 for standalone evaluation
        composite_raw = (detection_score + min(efficiency_score/1000, 1) + min(deployment_score, 1)) / 3
        print(f"\n  ★ APPROXIMATE COMPOSITE SCORE: {composite_raw:.4f}")
        print("\n  Note: For accurate comparison, normalize with other models in your dataset.")
    


if __name__ == "__main__":
    main()

