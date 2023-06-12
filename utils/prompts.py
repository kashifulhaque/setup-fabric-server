def prompt_confirmation(prompt):
    ans = input(prompt).strip().lower()
    return ans == "y"