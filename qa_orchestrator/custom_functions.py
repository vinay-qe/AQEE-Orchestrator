def validate_phase_output(phase_name: str, output_data: str) -> dict:
    """
    Validates the quality and completeness of an agent's phase output.
    Args:
        phase_name: The name of the phase being validated (e.g., 'Architect').
        output_data: The text or JSON output from the agent.
    Returns:
        A dictionary containing 'status' (success/error) and 'feedback'.
    """
    # Simple validation example: Check if output is too short or missing key terms
    if not output_data or len(output_data) < 50:
        return {
            "status": "error",
            "feedback": f"Phase {phase_name} failed: Output is too brief or empty."
        }
    
    if "User Story" not in output_data and phase_name == "Architect":
         return {
            "status": "error",
            "feedback": "Architect failed: No 'User Story' keywords found in output."
        }

    return {
        "status": "success",
        "feedback": f"Phase {phase_name} validated successfully."
    }