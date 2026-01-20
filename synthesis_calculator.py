"""
Synthesis Engine Calculator
===========================
This script calculates the final composite score by combining all evaluation dimensions:
- Detection Performance: 30% weight
- Attack Surface Coverage (ASC): 25% weight
- Total Cost of Ownership (TCO): 20% weight (lower is better)
- Deployment Capability: 15% weight
- Computational Efficiency: 10% weight

Usage:
    python synthesis_calculator.py
    
Then enter your model's metrics when prompted.
"""


# Default weights (from Table framework_weights)
WEIGHTS = {
    'detection': 0.30,
    'asc': 0.25,
    'tco': 0.20,
    'deployment': 0.15,
    'efficiency': 0.10
}


def normalize_score(score: float, min_val: float, max_val: float, 
                    inverse: bool = False) -> float:
    """
    Normalize score to 0-100 range using min-max normalization.
    
    Args:
        score: Raw score to normalize
        min_val: Minimum value in the dataset
        max_val: Maximum value in the dataset
        inverse: If True, lower raw scores get higher normalized scores (for TCO)
    
    Returns:
        Normalized score (0-100 range)
    """
    if max_val == min_val:
        return 100.0 if inverse else 0.0
    
    if inverse:
        # For TCO: lower cost = higher score
        return ((max_val - score) / (max_val - min_val)) * 100
    else:
        return ((score - min_val) / (max_val - min_val)) * 100


def calculate_final_score(detection_norm: float, asc_norm: float, tco_norm: float,
                          deployment_norm: float, efficiency_norm: float,
                          weights: dict = None) -> float:
    """
    Calculate final composite score using weighted sum.
    
    Equation:
    Final = (0.30×Detection) + (0.25×ASC) + (0.20×TCO) + (0.15×Deployment) + (0.10×Efficiency)
    
    Args:
        detection_norm: Normalized Detection score (0-100)
        asc_norm: Normalized ASC score (0-100)
        tco_norm: Normalized TCO score (0-100, lower cost = higher score)
        deployment_norm: Normalized Deployment score (0-100)
        efficiency_norm: Normalized Efficiency score (0-100)
        weights: Optional custom weights dictionary
    
    Returns:
        Final composite score
    """
    w = weights or WEIGHTS
    
    return (w['detection'] * detection_norm +
            w['asc'] * asc_norm +
            w['tco'] * tco_norm +
            w['deployment'] * deployment_norm +
            w['efficiency'] * efficiency_norm)


def main():
    print("=" * 70)
    print("  SYNTHESIS ENGINE - FINAL MODEL RANKING CALCULATOR")
    print("=" * 70)
    print("\nThis calculator combines all evaluation dimensions into a final ranking.")
    print("Default weights: Detection(30%), ASC(25%), TCO(20%), Deployment(15%), Efficiency(10%)\n")
    
    # Ask about custom weights
    custom_weights = input("Use default weights? (yes/no): ").strip().lower()
    weights = WEIGHTS.copy()
    
    if custom_weights in ['no', 'n']:
        print("\n" + "-" * 40)
        print("CUSTOM WEIGHTS (must sum to 1.0)")
        print("-" * 40)
        weights['detection'] = float(input(f"Detection weight [{weights['detection']}]: ") or weights['detection'])
        weights['asc'] = float(input(f"ASC weight [{weights['asc']}]: ") or weights['asc'])
        weights['tco'] = float(input(f"TCO weight [{weights['tco']}]: ") or weights['tco'])
        weights['deployment'] = float(input(f"Deployment weight [{weights['deployment']}]: ") or weights['deployment'])
        weights['efficiency'] = float(input(f"Efficiency weight [{weights['efficiency']}]: ") or weights['efficiency'])
        
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            print(f"\n⚠️  Warning: Weights sum to {total_weight:.2f}, not 1.0. Normalizing...")
            for key in weights:
                weights[key] /= total_weight
    
    # Determine mode: single model or comparison
    mode = input("\nEvaluate (1) Single model or (2) Compare multiple models? [1/2]: ").strip()
    
    if mode == '2':
        # Multiple model comparison
        num_models = int(input("How many models to compare? "))
        models = []
        
        for i in range(num_models):
            print(f"\n" + "-" * 40)
            print(f"MODEL {i+1} METRICS")
            print("-" * 40)
            name = input(f"Model name: ")
            detection = float(input("  Detection/Accuracy (0-100): "))
            asc = float(input("  ASC Score (0-100): "))
            tco = float(input("  TCO (total $): "))
            deployment = float(input("  Deployment Score (raw): "))
            efficiency = float(input("  Efficiency Score (raw): "))
            
            models.append({
                'name': name,
                'detection': detection,
                'asc': asc,
                'tco': tco,
                'deployment': deployment,
                'efficiency': efficiency
            })
        
        # Calculate min/max for normalization
        tco_min = min(m['tco'] for m in models)
        tco_max = max(m['tco'] for m in models)
        dep_min = min(m['deployment'] for m in models)
        dep_max = max(m['deployment'] for m in models)
        eff_min = min(m['efficiency'] for m in models)
        eff_max = max(m['efficiency'] for m in models)
        
        # Normalize and calculate final scores
        results = []
        for m in models:
            det_norm = m['detection']  # Already in 0-100
            asc_norm = m['asc']        # Already in 0-100
            tco_norm = normalize_score(m['tco'], tco_min, tco_max, inverse=True)
            dep_norm = normalize_score(m['deployment'], dep_min, dep_max)
            eff_norm = normalize_score(m['efficiency'], eff_min, eff_max)
            
            final = calculate_final_score(det_norm, asc_norm, tco_norm, dep_norm, eff_norm, weights)
            
            results.append({
                'name': m['name'],
                'detection_norm': det_norm,
                'asc_norm': asc_norm,
                'tco_norm': tco_norm,
                'deployment_norm': dep_norm,
                'efficiency_norm': eff_norm,
                'final_score': final
            })
        
        # Sort by final score
        results.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Display results
        print("\n" + "=" * 70)
        print("  NORMALIZED SCORES (0-100 Scale)")
        print("=" * 70)
        print(f"{'Model':<25} | {'Det.':<7} | {'ASC':<7} | {'TCO':<7} | {'Dep.':<7} | {'Eff.':<7}")
        print("-" * 70)
        for r in results:
            print(f"{r['name']:<25} | {r['detection_norm']:>6.2f} | {r['asc_norm']:>6.2f} | "
                  f"{r['tco_norm']:>6.2f} | {r['deployment_norm']:>6.2f} | {r['efficiency_norm']:>6.2f}")
        
        print("\n" + "=" * 70)
        print("  WEIGHTED CONTRIBUTIONS")
        print("=" * 70)
        for r in results:
            det_w = r['detection_norm'] * weights['detection']
            asc_w = r['asc_norm'] * weights['asc']
            tco_w = r['tco_norm'] * weights['tco']
            dep_w = r['deployment_norm'] * weights['deployment']
            eff_w = r['efficiency_norm'] * weights['efficiency']
            
            print(f"\n{r['name']}:")
            print(f"  Detection × {weights['detection']:.2f}:    {r['detection_norm']:.2f} × {weights['detection']:.2f} = {det_w:.2f}")
            print(f"  ASC × {weights['asc']:.2f}:         {r['asc_norm']:.2f} × {weights['asc']:.2f} = {asc_w:.2f}")
            print(f"  TCO × {weights['tco']:.2f}:         {r['tco_norm']:.2f} × {weights['tco']:.2f} = {tco_w:.2f}")
            print(f"  Deployment × {weights['deployment']:.2f}:  {r['deployment_norm']:.2f} × {weights['deployment']:.2f} = {dep_w:.2f}")
            print(f"  Efficiency × {weights['efficiency']:.2f}:  {r['efficiency_norm']:.2f} × {weights['efficiency']:.2f} = {eff_w:.2f}")
        
        print("\n" + "=" * 70)
        print("  FINAL RANKINGS")
        print("=" * 70)
        print(f"{'Rank':<6} | {'Model':<25} | {'Composite Score':<15}")
        print("-" * 55)
        for i, r in enumerate(results, 1):
            star = " ★" if i == 1 else ""
            print(f"{i:<6} | {r['name']:<25} | {r['final_score']:>12.2f}{star}")
        
    else:
        # Single model evaluation
        print("\n" + "-" * 40)
        print("MODEL METRICS (Already Normalized)")
        print("-" * 40)
        print("Note: For single model, enter pre-normalized scores (0-100 range)")
        
        detection = float(input("Detection score (0-100): "))
        asc = float(input("ASC score (0-100): "))
        tco = float(input("TCO normalized score (0-100, where 100=lowest cost): "))
        deployment = float(input("Deployment normalized score (0-100): "))
        efficiency = float(input("Efficiency normalized score (0-100): "))
        
        final = calculate_final_score(detection, asc, tco, deployment, efficiency, weights)
        
        print("\n" + "=" * 70)
        print("  WEIGHTED CONTRIBUTIONS")
        print("=" * 70)
        det_w = detection * weights['detection']
        asc_w = asc * weights['asc']
        tco_w = tco * weights['tco']
        dep_w = deployment * weights['deployment']
        eff_w = efficiency * weights['efficiency']
        
        print(f"  Detection × {weights['detection']:.2f}:    {detection:.2f} × {weights['detection']:.2f} = {det_w:.2f}")
        print(f"  ASC × {weights['asc']:.2f}:         {asc:.2f} × {weights['asc']:.2f} = {asc_w:.2f}")
        print(f"  TCO × {weights['tco']:.2f}:         {tco:.2f} × {weights['tco']:.2f} = {tco_w:.2f}")
        print(f"  Deployment × {weights['deployment']:.2f}:  {deployment:.2f} × {weights['deployment']:.2f} = {dep_w:.2f}")
        print(f"  Efficiency × {weights['efficiency']:.2f}:  {efficiency:.2f} × {weights['efficiency']:.2f} = {eff_w:.2f}")
        
        print("\n" + "=" * 70)
        print("  FINAL COMPOSITE SCORE")
        print("=" * 70)
        print(f"\n  ★ FINAL SCORE: {final:.2f}")
        
        # Interpretation
        print("\n" + "-" * 40)
        print("INTERPRETATION")
        print("-" * 40)
        if final >= 78:
            print("  Excellent - Top-tier model for balanced IIoT deployment")
        elif final >= 72:
            print("  Very Good - Suitable for most deployment scenarios")
        elif final >= 65:
            print("  Good - Adequate performance with some trade-offs")
        else:
            print("  Moderate - Consider optimizing specific dimensions")
    

    print("\n  Formula: Final = (0.30×Det) + (0.25×ASC) + (0.20×TCO) + (0.15×Dep) + (0.10×Eff)")


if __name__ == "__main__":
    main()

