"""
Total Cost of Ownership (TCO) Calculator
========================================
This script calculates the 5-year TCO for IDS models based on:
- Deployment Cost (DEP): Infrastructure, Hardware, Network, Integration
- Operational Cost (OP): Training, Inference, Energy
- Incident Response Cost (IR): False positive investigation costs
- Scalability Cost (SC): Expansion fees
- Compliance Cost (CC): Audit and certification fees

Usage:
    python tco_calculator.py
    
Then enter your model's metrics when prompted.
"""

# Default cost parameters (can be customized)
DEFAULT_PARAMS = {
    # System parameters
    'num_devices': 1000,
    'evaluation_years': 5,
    'flows_per_device_per_day': 10000,
    
    # Deployment costs
    'base_infrastructure': 50000,
    'hardware_cost_per_mb': 350,
    'network_cost_edge': 10000,
    'network_cost_centralized': 50000,
    'integration_cost_edge': 20000,
    'integration_cost_dl': 100000,
    
    # Operational costs
    'retraining_frequency_per_year': 1,
    'training_compute_rate_per_hour': 2,
    'inference_compute_rate_per_hour': 0.5,
    'energy_cost_per_device_5year': 90,
    
    # Incident response
    'alert_investigation_time_min': 10,
    'soc_analyst_rate_per_hour': 75,
    
    # Scalability
    'expansion_fee_edge': 80000,
    'expansion_fee_non_edge': 50000,
    
    # Compliance
    'base_audit_fee': 120000,
    'interpretability_high': 1.0,
    'interpretability_medium': 0.5,
    'interpretability_low': 0.2
}


def calculate_deployment_cost(model_size_mb: float, is_edge_compatible: bool, 
                              params: dict = None) -> dict:
    """
    Calculate Deployment Cost (DEP).
    Equation: DEP = C_infra + C_hw + C_net + C_int
    
    Args:
        model_size_mb: Model size in megabytes
        is_edge_compatible: Whether model can be deployed on edge devices
        params: Cost parameters dictionary
    
    Returns:
        Dictionary with cost breakdown and total
    """
    p = params or DEFAULT_PARAMS
    
    c_infra = p['base_infrastructure']
    c_hw = p['hardware_cost_per_mb'] * model_size_mb
    c_net = p['network_cost_edge'] if is_edge_compatible else p['network_cost_centralized']
    c_int = p['integration_cost_edge'] if is_edge_compatible else p['integration_cost_dl']
    
    total = c_infra + c_hw + c_net + c_int
    
    return {
        'infrastructure': c_infra,
        'hardware': c_hw,
        'network': c_net,
        'integration': c_int,
        'total': total
    }


def calculate_operational_cost(training_time_s: float, inference_time_s: float,
                               params: dict = None) -> dict:
    """
    Calculate Operational Cost (OP).
    Equation: OP = C_train + C_infer + C_energy
    
    Args:
        training_time_s: Training time in seconds
        inference_time_s: Inference time in seconds per sample
        params: Cost parameters dictionary
    
    Returns:
        Dictionary with cost breakdown and total
    """
    p = params or DEFAULT_PARAMS
    
    N = p['num_devices']
    Y = p['evaluation_years']
    F = p['flows_per_device_per_day']
    R = p['retraining_frequency_per_year']
    
    # Training cost
    training_hours = training_time_s / 3600
    c_train = training_hours * N * R * Y * p['training_compute_rate_per_hour']
    
    # Inference cost
    total_flows = F * N * 365 * Y
    inference_hours = (total_flows * inference_time_s) / 3600
    c_infer = inference_hours * p['inference_compute_rate_per_hour']
    
    # Energy cost
    c_energy = p['energy_cost_per_device_5year'] * N * Y
    
    total = c_train + c_infer + c_energy
    
    return {
        'training': c_train,
        'inference': c_infer,
        'energy': c_energy,
        'total': total
    }


def calculate_incident_response_cost(fpr: float, params: dict = None) -> dict:
    """
    Calculate Incident Response Cost (IR).
    Equation: IR = Total_False_Alerts × Cost_per_Alert
    
    Args:
        fpr: False Positive Rate as decimal
        params: Cost parameters dictionary
    
    Returns:
        Dictionary with cost breakdown and total
    """
    p = params or DEFAULT_PARAMS
    
    N = p['num_devices']
    Y = p['evaluation_years']
    F = p['flows_per_device_per_day']
    
    total_flows = F * N * 365 * Y
    false_alerts = fpr * total_flows
    
    alert_investigation_hours = p['alert_investigation_time_min'] / 60
    cost_per_alert = alert_investigation_hours * p['soc_analyst_rate_per_hour']
    
    total = false_alerts * cost_per_alert
    
    return {
        'total_flows': total_flows,
        'false_alerts': false_alerts,
        'cost_per_alert': cost_per_alert,
        'total': total
    }


def calculate_scalability_cost(is_edge_compatible: bool, edge_compatibility_score: float,
                               params: dict = None) -> dict:
    """
    Calculate Scalability Cost (SC).
    Equation: SC = Base_Expansion_Fee × Compatibility_Factor
    
    Args:
        is_edge_compatible: Whether model can be deployed on edge devices
        edge_compatibility_score: Edge compatibility score (0.2-1.0)
        params: Cost parameters dictionary
    
    Returns:
        Dictionary with cost breakdown and total
    """
    p = params or DEFAULT_PARAMS
    
    if is_edge_compatible:
        base_fee = p['expansion_fee_edge']
        total = base_fee * edge_compatibility_score
    else:
        total = p['expansion_fee_non_edge']
        base_fee = total
    
    return {
        'base_fee': base_fee,
        'compatibility_factor': edge_compatibility_score if is_edge_compatible else 1.0,
        'total': total
    }


def calculate_compliance_cost(interpretability: str, params: dict = None) -> dict:
    """
    Calculate Compliance Cost (CC).
    Equation: CC = Audit_Fee × Opacity_Factor
    
    Args:
        interpretability: 'high', 'medium', or 'low'
        params: Cost parameters dictionary
    
    Returns:
        Dictionary with cost breakdown and total
    """
    p = params or DEFAULT_PARAMS
    
    interp_scores = {
        'high': p['interpretability_high'],
        'medium': p['interpretability_medium'],
        'low': p['interpretability_low']
    }
    
    interp_score = interp_scores.get(interpretability.lower(), p['interpretability_low'])
    opacity_factor = 1 / interp_score
    
    total = p['base_audit_fee'] * opacity_factor
    
    return {
        'audit_fee': p['base_audit_fee'],
        'interpretability_score': interp_score,
        'opacity_factor': opacity_factor,
        'total': total
    }


def calculate_total_tco(dep: float, op: float, ir: float, sc: float, cc: float) -> float:
    """
    Calculate Total Cost of Ownership.
    Equation: TCO = DEP + OP + IR + SC + CC
    
    Returns:
        Total 5-year TCO
    """
    return dep + op + ir + sc + cc


def format_currency(amount: float) -> str:
    """Format number as currency string."""
    if amount >= 1000000:
        return f"${amount/1000000:.2f}M"
    elif amount >= 1000:
        return f"${amount/1000:.1f}K"
    else:
        return f"${amount:.2f}"


def main():
    print("=" * 70)
    print("  TOTAL COST OF OWNERSHIP (TCO) CALCULATOR")
    print("=" * 70)
    print("\nThis calculator computes the 5-year TCO for your IDS model deployment.")
    print("Cost components: DEP + OP + IR + SC + CC\n")
    
    # Ask if user wants to customize parameters
    customize = input("Use default cost parameters? (yes/no): ").strip().lower()
    params = DEFAULT_PARAMS.copy()
    
    if customize in ['no', 'n']:
        print("\n" + "-" * 40)
        print("CUSTOM SYSTEM PARAMETERS")
        print("-" * 40)
        params['num_devices'] = int(input(f"Number of devices [{params['num_devices']}]: ") or params['num_devices'])
        params['evaluation_years'] = int(input(f"Evaluation period in years [{params['evaluation_years']}]: ") or params['evaluation_years'])
        params['flows_per_device_per_day'] = int(input(f"Flows per device per day [{params['flows_per_device_per_day']}]: ") or params['flows_per_device_per_day'])
    
    # Get model-specific inputs
    print("\n" + "-" * 40)
    print("MODEL SPECIFICATIONS")
    print("-" * 40)
    model_size = float(input("Enter Model Size (MB): "))
    training_time = float(input("Enter Training Time (seconds): "))
    inference_time = float(input("Enter Inference Time per sample (seconds): "))
    
    fpr_input = input("Enter False Positive Rate (e.g., 0.0012 for 0.12%): ")
    fpr = float(fpr_input)
    
    edge_input = input("Is the model edge-compatible? (yes/no): ").strip().lower()
    is_edge = edge_input in ['yes', 'y', 'true', '1']
    
    if is_edge:
        edge_score = float(input("Enter Edge Compatibility Score (0.2-1.0): "))
    else:
        edge_score = 0.2
    
    print("\nInterpretability levels:")
    print("  1. High (e.g., Decision Trees, Rule-based)")
    print("  2. Medium (e.g., Hybrid models with some explainability)")
    print("  3. Low (e.g., Deep neural networks, black-box models)")
    interp_choice = input("Select interpretability level [1/2/3]: ").strip()
    interp_map = {'1': 'high', '2': 'medium', '3': 'low'}
    interpretability = interp_map.get(interp_choice, 'low')
    
    # Calculate all cost components
    dep_result = calculate_deployment_cost(model_size, is_edge, params)
    op_result = calculate_operational_cost(training_time, inference_time, params)
    ir_result = calculate_incident_response_cost(fpr, params)
    sc_result = calculate_scalability_cost(is_edge, edge_score, params)
    cc_result = calculate_compliance_cost(interpretability, params)
    
    total_tco = calculate_total_tco(
        dep_result['total'], op_result['total'], ir_result['total'],
        sc_result['total'], cc_result['total']
    )
    
    # Display detailed results
    print("\n" + "=" * 70)
    print("  DEPLOYMENT COST (DEP) BREAKDOWN")
    print("=" * 70)
    print(f"  Infrastructure (C_infra):    {format_currency(dep_result['infrastructure'])}")
    print(f"  Hardware (C_hw):             {format_currency(dep_result['hardware'])}")
    print(f"  Network (C_net):             {format_currency(dep_result['network'])}")
    print(f"  Integration (C_int):         {format_currency(dep_result['integration'])}")
    print(f"  ─────────────────────────────────────")
    print(f"  DEPLOYMENT TOTAL:            {format_currency(dep_result['total'])}")
    
    print("\n" + "=" * 70)
    print("  OPERATIONAL COST (OP) BREAKDOWN")
    print("=" * 70)
    print(f"  Training (C_train):          {format_currency(op_result['training'])}")
    print(f"  Inference (C_infer):         {format_currency(op_result['inference'])}")
    print(f"  Energy (C_energy):           {format_currency(op_result['energy'])}")
    print(f"  ─────────────────────────────────────")
    print(f"  OPERATIONAL TOTAL:           {format_currency(op_result['total'])}")
    
    print("\n" + "=" * 70)
    print("  INCIDENT RESPONSE COST (IR) BREAKDOWN")
    print("=" * 70)
    print(f"  Total flows over {params['evaluation_years']} years:   {ir_result['total_flows']:,.0f}")
    print(f"  False alerts (FPR={fpr}):    {ir_result['false_alerts']:,.0f}")
    print(f"  Cost per alert:              {format_currency(ir_result['cost_per_alert'])}")
    print(f"  ─────────────────────────────────────")
    print(f"  INCIDENT RESPONSE TOTAL:     {format_currency(ir_result['total'])}")
    
    print("\n" + "=" * 70)
    print("  SCALABILITY COST (SC) BREAKDOWN")
    print("=" * 70)
    print(f"  Base expansion fee:          {format_currency(sc_result['base_fee'])}")
    print(f"  Compatibility factor:        {sc_result['compatibility_factor']}")
    print(f"  ─────────────────────────────────────")
    print(f"  SCALABILITY TOTAL:           {format_currency(sc_result['total'])}")
    
    print("\n" + "=" * 70)
    print("  COMPLIANCE COST (CC) BREAKDOWN")
    print("=" * 70)
    print(f"  Base audit fee:              {format_currency(cc_result['audit_fee'])}")
    print(f"  Interpretability ({interpretability}):    {cc_result['interpretability_score']}")
    print(f"  Opacity factor (1/interp):   {cc_result['opacity_factor']:.1f}")
    print(f"  ─────────────────────────────────────")
    print(f"  COMPLIANCE TOTAL:            {format_currency(cc_result['total'])}")
    
    print("\n" + "=" * 70)
    print("  TOTAL COST OF OWNERSHIP SUMMARY")
    print("=" * 70)
    print(f"  Deployment (DEP):            {format_currency(dep_result['total']):>15}")
    print(f"  Operational (OP):            {format_currency(op_result['total']):>15}")
    print(f"  Incident Response (IR):      {format_currency(ir_result['total']):>15}")
    print(f"  Scalability (SC):            {format_currency(sc_result['total']):>15}")
    print(f"  Compliance (CC):             {format_currency(cc_result['total']):>15}")
    print(f"  ═══════════════════════════════════════════════════")
    print(f"\n  ★ {params['evaluation_years']}-YEAR TCO: {format_currency(total_tco)}")
    print(f"     (${total_tco:,.2f})")
    


if __name__ == "__main__":
    main()

